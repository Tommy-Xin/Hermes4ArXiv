#!/usr/bin/env python3
"""
AI分析器模块 - 简化版本
使用DeepSeek作为唯一AI分析器，确保稳定可靠
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Tuple, Any
import arxiv

from .prompts import PromptManager

logger = logging.getLogger(__name__)


class DeepSeekAnalyzer:
    """DeepSeek分析器 - 唯一AI分析器"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", **kwargs):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"
        self.retry_times = kwargs.get('retry_times', 3)
        self.delay = kwargs.get('delay', 2)
        self.timeout = kwargs.get('timeout', 60)
        self.is_available_flag = bool(api_key and len(api_key) > 10)
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        import openai
        
        # 兼容不同版本的OpenAI库
        try:
            # 新版本 OpenAI (>=1.0.0)
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout
            )
            use_new_api = True
        except AttributeError:
            # 老版本 OpenAI (<1.0.0)
            openai.api_key = self.api_key
            openai.api_base = self.base_url
            use_new_api = False
        
        system_prompt = PromptManager.get_system_prompt(analysis_type)
        user_prompt = PromptManager.get_user_prompt(paper, analysis_type)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"DeepSeek分析论文: {paper.title[:50]}... (尝试 {attempt + 1}/{self.retry_times})")
                
                if use_new_api:
                    # 新版本API
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
                else:
                    # 老版本API
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1500,
                        request_timeout=self.timeout
                    )
                    analysis = response.choices[0].message.content
                
                logger.info(f"DeepSeek分析完成: {paper.title[:50]}...")
                
                # 添加延迟避免API限制
                await asyncio.sleep(self.delay)
                
                return self._format_analysis_result(analysis, "deepseek", self.model)
                
            except Exception as e:
                error_msg = str(e)
                # 特别处理网络相关错误
                if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                    logger.warning(f"DeepSeek网络错误 (尝试 {attempt + 1}): {error_msg}")
                    # 网络错误时增加等待时间
                    if attempt < self.retry_times - 1:
                        wait_time = self.delay * (attempt + 2) * 2  # 指数退避
                        logger.info(f"网络错误，等待 {wait_time} 秒后重试...")
                        await asyncio.sleep(wait_time)
                else:
                    logger.warning(f"DeepSeek分析失败 (尝试 {attempt + 1}): {error_msg}")
                    if attempt < self.retry_times - 1:
                        await asyncio.sleep(self.delay * (attempt + 1))
                
                if attempt == self.retry_times - 1:
                    raise e
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.is_available_flag
    
    def _format_analysis_result(self, analysis_text: str, provider: str, model: str) -> Dict[str, Any]:
        """格式化分析结果"""
        return {
            'analysis': analysis_text,
            'provider': provider,
            'model': model,
            'timestamp': time.time(),
            'html_analysis': PromptManager.format_analysis_for_html(analysis_text)
        }
    
    def get_provider_info(self) -> Dict[str, str]:
        return {
            "name": "DeepSeek",
            "provider": "deepseek",
            "model": self.model,
            "description": "DeepSeek - 高性价比稳定AI模型"
        }


class AIAnalyzer:
    """
    简化版AI分析器 - 只使用DeepSeek
    稳定可靠，成本可控
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.analyzer = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """初始化DeepSeek分析器"""
        if not self.config.get('DEEPSEEK_API_KEY'):
            logger.error("❌ 未配置DEEPSEEK_API_KEY，无法进行论文分析")
            return
        
        self.analyzer = DeepSeekAnalyzer(
            api_key=self.config['DEEPSEEK_API_KEY'],
            model=self.config.get('DEEPSEEK_MODEL', 'deepseek-chat'),
            retry_times=self.config.get('API_RETRY_TIMES', 3),
            delay=self.config.get('API_DELAY', 2),
            timeout=self.config.get('API_TIMEOUT', 60)
        )
        
        logger.info(f"✅ 初始化DeepSeek分析器: {self.analyzer.model}")
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        if not self.analyzer or not self.analyzer.is_available():
            logger.error("❌ DeepSeek分析器不可用")
            return None
        
        try:
            result = await self.analyzer.analyze_paper(paper, analysis_type)
            logger.info(f"✅ 论文分析完成: {paper.title[:50]}...")
            return result
        except Exception as e:
            logger.error(f"❌ 论文分析失败: {str(e)}")
            return None
    
    def get_analyzer_status(self) -> Dict[str, Any]:
        """获取分析器状态"""
        if not self.analyzer:
            return {
                'strategy': 'single',
                'analyzer': None,
                'available': False,
                'error': 'DeepSeek分析器未初始化'
            }
        
        info = self.analyzer.get_provider_info()
        return {
            'strategy': 'single',
            'analyzer': info,
            'available': self.analyzer.is_available(),
            'model': self.analyzer.model
        } 