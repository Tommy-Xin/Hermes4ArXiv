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
    
    def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """同步分析论文"""
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
                time.sleep(self.delay)
                
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
                        time.sleep(wait_time)
                    else:
                        time.sleep(self.delay * (attempt + 1))
                
                if attempt == self.retry_times - 1:
                    raise e

    def analyze_papers_batch(self, papers: list, batch_size: int = 4) -> Dict[str, Any]:
        """
        批量比较分析论文
        
        Args:
            papers: 论文列表
            batch_size: 批次大小，默认4篇
            
        Returns:
            批量分析结果字典
        """
        import openai
        
        if len(papers) < 2:
            # 如果论文数量不足，回退到单独分析
            logger.warning("论文数量不足，回退到单独分析模式")
            return None
        
        # 准备论文信息
        papers_info = []
        for paper in papers[:batch_size]:  # 限制批次大小
            # 提取作者信息
            authors_str = '未知'
            if hasattr(paper, 'authors') and paper.authors:
                try:
                    author_names = [author.name for author in paper.authors]
                    authors_str = ', '.join(author_names[:3])  # 最多显示3个作者
                    if len(author_names) > 3:
                        authors_str += f" 等{len(author_names)}人"
                except AttributeError:
                    try:
                        author_names = [str(author) for author in paper.authors[:3]]
                        authors_str = ', '.join(author_names)
                    except:
                        authors_str = f'作者信息异常 ({len(paper.authors)} 位作者)'
            
            # 格式化发布时间
            published_date = '未知'
            if hasattr(paper, 'published') and paper.published:
                try:
                    published_date = paper.published.strftime('%Y年%m月%d日')
                except:
                    published_date = str(paper.published)
            
            # 处理摘要长度
            summary = paper.summary.strip()
            if len(summary) > 800:  # 批量分析时摘要更短
                summary = summary[:800] + "..."
            
            papers_info.append({
                'title': paper.title,
                'authors': authors_str,
                'categories': ', '.join(paper.categories),
                'published': published_date,
                'summary': summary,
                'url': paper.entry_id
            })
        
        # 使用OpenAI兼容的API
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout * 2  # 批量分析需要更长时间
        )
        
        system_prompt = PromptManager.get_batch_comparison_system_prompt()
        user_prompt = PromptManager.get_batch_comparison_user_prompt(papers_info)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"DeepSeek批量分析 {len(papers_info)} 篇论文 (尝试 {attempt + 1}/{self.retry_times})")
                
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,  # 更低的温度确保一致性
                    max_tokens=3000,  # 批量分析需要更多token
                    timeout=self.timeout * 2
                )
                
                batch_analysis = response.choices[0].message.content
                logger.info(f"✅ DeepSeek批量分析完成: {len(papers_info)} 篇论文")
                
                # 延迟避免API限制
                time.sleep(self.delay * 2)
                
                return {
                    'batch_analysis': batch_analysis,
                    'papers_count': len(papers_info),
                    'provider': 'deepseek',
                    'model': self.model,
                    'timestamp': time.time(),
                    'analysis_type': 'batch_comparison'
                }
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"❌ DeepSeek批量分析失败 (尝试 {attempt + 1}): {error_msg}")
                
                if attempt < self.retry_times - 1:
                    if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                        wait_time = self.delay * (attempt + 2) * 3
                        logger.info(f"网络错误，等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    else:
                        time.sleep(self.delay * (attempt + 2))
                
                if attempt == self.retry_times - 1:
                    logger.error(f"批量分析最终失败，回退到单独分析模式")
                    return None

    def get_info(self) -> Dict[str, str]:
        """获取分析器信息"""
        return {
            "name": "DeepSeek",
            "model": self.model,
            "description": "DeepSeek - 高性价比稳定AI模型"
        } 