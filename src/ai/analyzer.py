#!/usr/bin/env python3
"""
AI 分析器模块
使用 DeepSeek API 进行所有分析。
"""

import logging
import time
import json
from typing import Dict, Any, List

import openai
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Config
from .prompts import PromptManager

logger = logging.getLogger(__name__)


class DeepSeekAnalyzer:
    """
    使用 DeepSeek API 进行论文分析的主分析器。
    支持完整的两阶段分析流程。
    """

    def __init__(self, config: Config):
        """
        初始化分析器，从配置中加载设置。
        """
        self.config = config
        self.timeout = config.API_TIMEOUT
        self.model = config.DEEPSEEK_MODEL
        
        if not config.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY not found in config.")

        self.client = openai.OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def rank_papers_in_batch(self, papers: list[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        对一小批论文进行强制排名和评分 (Stage 1).
        返回一个包含评分结果的列表。
        """
        logger.info(f"Executing Stage 1: Ranking a batch of {len(papers)} papers using DeepSeek.")
        if not papers:
            return []

        response_text = ""
        try:
            system_prompt = PromptManager.get_stage1_ranking_system_prompt()
            user_prompt = PromptManager.format_stage1_ranking_prompt(papers)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                max_tokens=2048,
                temperature=0.2,
                response_format={"type": "json_object"},
                timeout=self.timeout
            )
            
            response_text = response.choices[0].message.content
            logger.debug(f"Raw Stage 1 ranking response from AI: {response_text}")
            
            parsed_json = json.loads(response_text)
            
            if isinstance(parsed_json, dict):
                ranking_list = next((v for v in parsed_json.values() if isinstance(v, list)), None)
                if ranking_list is None:
                    logger.error("AI returned a JSON object for ranking, but no list was found inside.")
                    return []
            elif isinstance(parsed_json, list):
                ranking_list = parsed_json
            else:
                logger.error(f"AI ranking response was not a JSON list or a dict containing a list. Type: {type(parsed_json)}")
                return []

            if not all('paper_id' in item and 'score' in item for item in ranking_list):
                logger.error("AI ranking response list has malformed items.")
                return []
                
            return ranking_list

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from AI ranking response: {e}\nProblematic text: {response_text}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred during paper ranking: {e}", exc_info=True)
            return []

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_papers_batch(self, papers: list[Dict[str, Any]]) -> str:
        """
        对一批论文进行深入的批量分析 (Stage 2).
        返回一个包含所有分析的长字符串。
        """
        logger.info(f"Executing Stage 2: Performing deep analysis on a batch of {len(papers)} papers using DeepSeek.")
        if not papers:
            return ""

        system_prompt = PromptManager.get_system_prompt()
        user_prompt = PromptManager.format_batch_analysis_prompt(papers)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            max_tokens=8000,
            temperature=0.5,
            stream=False,
            timeout=self.timeout * 2
        )
        analysis_text = response.choices[0].message.content
        logger.info(f"Successfully completed deep analysis for {len(papers)} papers.")
        return analysis_text

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def analyze_paper(self, paper: Dict[str, Any]) -> str:
        """
        对单篇论文进行深入分析 (用于后备或单次运行).
        返回包含分析结果的字符串。
        """
        logger.info(f"Performing single paper analysis for: {paper.get('title', 'N/A')} using DeepSeek.")
        system_prompt = PromptManager.get_system_prompt()
        
        # 直接从字典构建Prompt，以适应数据库记录的格式
        user_prompt = f"""请分析以下ArXiv论文：
📄 **论文标题**：{paper.get('title', '未知标题')}
👥 **作者信息**：{paper.get('authors', '未知作者')}
🏷️ **研究领域**：{paper.get('categories', '未知领域')}
📅 **发布时间**：{paper.get('published_date', '未知日期')}
📝 **论文摘要**：{paper.get('abstract', '摘要不可用')}
🔗 **论文链接**：https://arxiv.org/abs/{paper.get('paper_id', '')}
---
请基于以上信息，按照系统提示的结构进行深度分析。"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            max_tokens=2000,
            temperature=0.7,
            timeout=self.timeout
        )
        
        return response.choices[0].message.content 