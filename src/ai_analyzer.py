#!/usr/bin/env python3
"""
AI分析模块
支持多种AI API和论文分析功能
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import arxiv
import openai

from utils.logger import logger


class AIAnalyzer(ABC):
    """AI分析器抽象基类"""

    @abstractmethod
    def analyze_paper(self, paper: arxiv.Result) -> str:
        """分析论文"""
        pass


class DeepSeekAnalyzer(AIAnalyzer):
    """DeepSeek AI分析器"""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        retry_times: int = 3,
        delay: int = 2,
    ):
        """
        初始化DeepSeek分析器

        Args:
            api_key: API密钥
            model: 模型名称
            retry_times: 重试次数
            delay: 调用间隔
        """
        self.api_key = api_key
        self.model = model
        self.retry_times = retry_times
        self.delay = delay

        # 配置OpenAI客户端
        openai.api_key = api_key
        openai.api_base = "https://api.deepseek.com/v1"

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一位专业的学术论文分析专家，具有深厚的AI、机器学习和计算机科学背景。
你的任务是分析ArXiv论文并提供高质量的中文总结。

请按照以下结构分析论文：
1. **核心贡献**：用1-2句话概括论文的主要贡献和创新点
2. **技术方法**：详细描述采用的技术方法、算法或架构
3. **实验验证**：总结实验设置、数据集、评估指标和主要结果
4. **影响意义**：分析对相关领域的潜在影响和应用价值
5. **局限展望**：指出研究局限性和未来发展方向

要求：
- 使用专业但易懂的中文表达
- 突出技术创新点和实际应用价值
- 保持客观和准确性
- 控制总结长度在300-500字之间"""

    def get_user_prompt(self, paper: arxiv.Result) -> str:
        """获取用户提示词"""
        author_names = [author.name for author in paper.authors]

        return f"""请分析以下论文：

**标题**: {paper.title}
**作者**: {', '.join(author_names)}
**类别**: {', '.join(paper.categories)}
**发布时间**: {paper.published.strftime('%Y-%m-%d')}
**摘要**: {paper.summary}

请按照系统提示的结构进行分析。"""

    def analyze_paper(self, paper: arxiv.Result) -> str:
        """
        分析论文

        Args:
            paper: 论文对象

        Returns:
            分析结果
        """
        for attempt in range(self.retry_times):
            try:
                logger.info(
                    f"正在分析论文: {paper.title} (尝试 {attempt + 1}/{self.retry_times})"
                )

                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": self.get_user_prompt(paper)},
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

                analysis = response.choices[0].message.content
                logger.info(f"论文分析完成: {paper.title}")

                # 添加延迟避免API限制
                time.sleep(self.delay)
                return analysis

            except Exception as e:
                logger.error(
                    f"分析论文失败 {paper.title} (尝试 {attempt + 1}): {str(e)}"
                )
                if attempt < self.retry_times - 1:
                    time.sleep(self.delay * (attempt + 1))  # 递增延迟
                else:
                    return f"**论文分析失败**: {str(e)}"


class OpenAIAnalyzer(AIAnalyzer):
    """OpenAI GPT分析器（预留接口）"""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        # TODO: 实现OpenAI API调用

    def analyze_paper(self, paper: arxiv.Result) -> str:
        # TODO: 实现OpenAI分析逻辑
        return "OpenAI分析器暂未实现"


class ClaudeAnalyzer(AIAnalyzer):
    """Claude分析器（预留接口）"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        # TODO: 实现Claude API调用

    def analyze_paper(self, paper: arxiv.Result) -> str:
        # TODO: 实现Claude分析逻辑
        return "Claude分析器暂未实现"


class AnalyzerFactory:
    """分析器工厂类"""

    @staticmethod
    def create_analyzer(analyzer_type: str, **kwargs) -> AIAnalyzer:
        """
        创建分析器实例

        Args:
            analyzer_type: 分析器类型
            **kwargs: 分析器参数

        Returns:
            分析器实例
        """
        if analyzer_type.lower() == "deepseek":
            return DeepSeekAnalyzer(**kwargs)
        elif analyzer_type.lower() == "openai":
            return OpenAIAnalyzer(**kwargs)
        elif analyzer_type.lower() == "claude":
            return ClaudeAnalyzer(**kwargs)
        else:
            raise ValueError(f"不支持的分析器类型: {analyzer_type}")

    @staticmethod
    def get_available_analyzers() -> list:
        """获取可用的分析器列表"""
        return ["deepseek", "openai", "claude"]
