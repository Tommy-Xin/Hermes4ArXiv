#!/usr/bin/env python3
"""
DeepSeek AI分析器 - 简洁版本
专注于稳定可靠的单AI分析
"""

import asyncio
import logging
import time
from typing import Dict, Any
import arxiv

from .prompts import PromptManager

logger = logging.getLogger(__name__)


class DeepSeekAnalyzer:
    """DeepSeek AI分析器 - 稳定可靠的论文分析"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", timeout: int = 60, retry_times: int = 3, delay: int = 2):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"
        self.timeout = timeout
        self.retry_times = retry_times
        self.delay = delay
        
        if not api_key or len(api_key) < 10:
            raise ValueError("DeepSeek API密钥无效")
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        import openai
        
        # 使用OpenAI兼容的API
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout
        )
        
        system_prompt = PromptManager.get_system_prompt(analysis_type)
        user_prompt = PromptManager.get_user_prompt(paper, analysis_type)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"DeepSeek分析论文: {paper.title[:50]}... (尝试 {attempt + 1}/{self.retry_times})")
                
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500,
                    timeout=self.timeout
                )
                
                analysis = response.choices[0].message.content
                logger.info(f"✅ DeepSeek分析完成: {paper.title[:50]}...")
                
                # 添加延迟避免API限制
                await asyncio.sleep(self.delay)
                
                return {
                    'analysis': analysis,
                    'provider': 'deepseek',
                    'model': self.model,
                    'timestamp': time.time(),
                    'html_analysis': PromptManager.format_analysis_for_html(analysis)
                }
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"❌ DeepSeek分析失败 (尝试 {attempt + 1}): {error_msg}")
                
                if attempt < self.retry_times - 1:
                    # 网络错误时使用指数退避
                    if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                        wait_time = self.delay * (attempt + 2) * 2
                        logger.info(f"网络错误，等待 {wait_time} 秒后重试...")
                        await asyncio.sleep(wait_time)
                    else:
                        await asyncio.sleep(self.delay * (attempt + 1))
                
                if attempt == self.retry_times - 1:
                    raise e
    
    def get_info(self) -> Dict[str, str]:
        """获取分析器信息"""
        return {
            "name": "DeepSeek",
            "model": self.model,
            "description": "DeepSeek - 高性价比稳定AI模型"
        } 