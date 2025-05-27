#!/usr/bin/env python3
"""
多AI分析器模块
支持多个AI提供商的降级策略和并行分析
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import arxiv

from ai.prompts import PromptManager

logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """AI提供商枚举"""
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"
    ZHIPU = "zhipu"  # 智谱AI


class AnalysisStrategy(Enum):
    """分析策略枚举"""
    FALLBACK = "fallback"      # 降级策略：按顺序尝试
    PARALLEL = "parallel"      # 并行策略：同时调用多个
    CONSENSUS = "consensus"    # 共识策略：多个AI达成共识
    BEST_EFFORT = "best_effort"  # 尽力而为：尝试所有可用的


class BaseAIAnalyzer(ABC):
    """AI分析器基类"""
    
    def __init__(self, api_key: str, model: str = None, **kwargs):
        self.api_key = api_key
        self.model = model
        self.is_available_flag = bool(api_key and len(api_key) > 10)
        self.retry_times = kwargs.get('retry_times', 3)
        self.delay = kwargs.get('delay', 2)
        self.timeout = kwargs.get('timeout', 30)
    
    @abstractmethod
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        pass
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.is_available_flag
    
    @abstractmethod
    def get_provider_info(self) -> Dict[str, str]:
        """获取提供商信息"""
        pass
    
    def _format_analysis_result(self, analysis_text: str, provider: str, model: str) -> Dict[str, Any]:
        """格式化分析结果"""
        return {
            'analysis': analysis_text,
            'provider': provider,
            'model': model,
            'timestamp': time.time(),
            'html_analysis': PromptManager.format_analysis_for_html(analysis_text)
        }


class DeepSeekAnalyzer(BaseAIAnalyzer):
    """DeepSeek分析器"""
    
    def __init__(self, api_key: str, model: str = "deepseek-r1", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = "https://api.deepseek.com/v1"
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        import openai
        
        # 配置OpenAI客户端（DeepSeek兼容OpenAI API）
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
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
                logger.info(f"DeepSeek分析完成: {paper.title[:50]}...")
                
                # 添加延迟避免API限制
                await asyncio.sleep(self.delay)
                
                return self._format_analysis_result(analysis, "deepseek", self.model)
                
            except Exception as e:
                logger.warning(f"DeepSeek分析失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt < self.retry_times - 1:
                    await asyncio.sleep(self.delay * (attempt + 1))
                else:
                    raise e
    
    def get_provider_info(self) -> Dict[str, str]:
        return {
            "name": "DeepSeek",
            "provider": "deepseek",
            "model": self.model,
            "description": "DeepSeek AI - 高性价比的中文AI模型"
        }


class OpenAIAnalyzer(BaseAIAnalyzer):
    """OpenAI分析器"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = "https://api.openai.com/v1"
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        import openai
        
        client = openai.OpenAI(api_key=self.api_key)
        
        system_prompt = PromptManager.get_system_prompt(analysis_type)
        user_prompt = PromptManager.get_user_prompt(paper, analysis_type)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"OpenAI分析论文: {paper.title[:50]}... (尝试 {attempt + 1}/{self.retry_times})")
                
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
                logger.info(f"OpenAI分析完成: {paper.title[:50]}...")
                
                await asyncio.sleep(self.delay)
                
                return self._format_analysis_result(analysis, "openai", self.model)
                
            except Exception as e:
                logger.warning(f"OpenAI分析失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt < self.retry_times - 1:
                    await asyncio.sleep(self.delay * (attempt + 1))
                else:
                    raise e
    
    def get_provider_info(self) -> Dict[str, str]:
        return {
            "name": "OpenAI",
            "provider": "openai",
            "model": self.model,
            "description": "OpenAI GPT - 业界领先的AI模型"
        }


class ClaudeAnalyzer(BaseAIAnalyzer):
    """Claude分析器"""
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307", **kwargs):
        super().__init__(api_key, model, **kwargs)
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        try:
            import anthropic
        except ImportError:
            raise ImportError("需要安装 anthropic 库: pip install anthropic")
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        system_prompt = PromptManager.get_system_prompt(analysis_type)
        user_prompt = PromptManager.get_user_prompt(paper, analysis_type)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"Claude分析论文: {paper.title[:50]}... (尝试 {attempt + 1}/{self.retry_times})")
                
                response = client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ],
                    timeout=self.timeout
                )
                
                analysis = response.content[0].text
                logger.info(f"Claude分析完成: {paper.title[:50]}...")
                
                await asyncio.sleep(self.delay)
                
                return self._format_analysis_result(analysis, "claude", self.model)
                
            except Exception as e:
                logger.warning(f"Claude分析失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt < self.retry_times - 1:
                    await asyncio.sleep(self.delay * (attempt + 1))
                else:
                    raise e
    
    def get_provider_info(self) -> Dict[str, str]:
        return {
            "name": "Claude",
            "provider": "claude",
            "model": self.model,
            "description": "Anthropic Claude - 安全可靠的AI助手"
        }


class GeminiAnalyzer(BaseAIAnalyzer):
    """Gemini分析器"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        super().__init__(api_key, model, **kwargs)
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("需要安装 google-generativeai 库: pip install google-generativeai")
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        
        system_prompt = PromptManager.get_system_prompt(analysis_type)
        user_prompt = PromptManager.get_user_prompt(paper, analysis_type)
        
        # 合并系统提示和用户提示
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"Gemini分析论文: {paper.title[:50]}... (尝试 {attempt + 1}/{self.retry_times})")
                
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=1500,
                        temperature=0.7,
                    )
                )
                
                analysis = response.text
                logger.info(f"Gemini分析完成: {paper.title[:50]}...")
                
                await asyncio.sleep(self.delay)
                
                return self._format_analysis_result(analysis, "gemini", self.model)
                
            except Exception as e:
                logger.warning(f"Gemini分析失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt < self.retry_times - 1:
                    await asyncio.sleep(self.delay * (attempt + 1))
                else:
                    raise e
    
    def get_provider_info(self) -> Dict[str, str]:
        return {
            "name": "Gemini",
            "provider": "gemini",
            "model": self.model,
            "description": "Google Gemini - 多模态AI模型"
        }


class MultiAIAnalyzer:
    """多AI分析器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.analyzers: Dict[AIProvider, BaseAIAnalyzer] = {}
        self.strategy = self._parse_strategy()
        self.fallback_order = self._parse_fallback_order()
        self._initialize_analyzers()
    
    def _parse_strategy(self) -> AnalysisStrategy:
        """解析分析策略"""
        strategy_str = self.config.get('ANALYSIS_STRATEGY', 'fallback').lower()
        try:
            return AnalysisStrategy(strategy_str)
        except ValueError:
            logger.warning(f"未知的分析策略: {strategy_str}，使用默认策略: fallback")
            return AnalysisStrategy.FALLBACK
    
    def _parse_fallback_order(self) -> List[AIProvider]:
        """解析使用顺序 - 自动选择配置的模型"""
        # SOTA模型优先级顺序（2025年5月最新）
        sota_priority = ['claude', 'gemini', 'openai', 'deepseek']
        
        # 检查用户配置的API密钥，按SOTA优先级排序
        available_providers = []
        for provider_name in sota_priority:
            if self.config.get(f'{provider_name.upper()}_API_KEY'):
                try:
                    provider = AIProvider(provider_name)
                    available_providers.append(provider)
                except ValueError:
                    logger.warning(f"未知的AI提供商: {provider_name}")
        
        # 如果用户明确设置了降级顺序，尊重用户设置
        if self.config.get('AI_FALLBACK_ORDER'):
            order_str = self.config.get('AI_FALLBACK_ORDER')
            user_order = []
            for provider_name in order_str.split(','):
                provider_name = provider_name.strip().lower()
                try:
                    provider = AIProvider(provider_name)
                    if provider in available_providers:
                        user_order.append(provider)
                except ValueError:
                    logger.warning(f"未知的AI提供商: {provider_name}")
            if user_order:
                return user_order
        
        # 返回可用的提供商（按SOTA优先级）
        return available_providers if available_providers else [AIProvider.DEEPSEEK]
    
    def _initialize_analyzers(self):
        """初始化分析器"""
        # DeepSeek
        if self.config.get('DEEPSEEK_API_KEY'):
            self.analyzers[AIProvider.DEEPSEEK] = DeepSeekAnalyzer(
                api_key=self.config['DEEPSEEK_API_KEY'],
                model=self.config.get('DEEPSEEK_MODEL', 'deepseek-chat'),
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        # OpenAI - 默认使用o3（2025年SOTA推理模型）
        if self.config.get('OPENAI_API_KEY'):
            self.analyzers[AIProvider.OPENAI] = OpenAIAnalyzer(
                api_key=self.config['OPENAI_API_KEY'],
                model=self.config.get('OPENAI_MODEL', 'o3-2025-04-16'),  # 使用最新的o3推理模型
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        # Claude - 默认使用Claude Opus 4（2025年最强模型）
        if self.config.get('CLAUDE_API_KEY'):
            self.analyzers[AIProvider.CLAUDE] = ClaudeAnalyzer(
                api_key=self.config['CLAUDE_API_KEY'],
                model=self.config.get('CLAUDE_MODEL', 'claude-opus-4-20250514'),  # 最新的Claude Opus 4模型
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        # Gemini - 默认使用Gemini 2.5 Pro Preview（2025年最新SOTA）
        if self.config.get('GEMINI_API_KEY'):
            self.analyzers[AIProvider.GEMINI] = GeminiAnalyzer(
                api_key=self.config['GEMINI_API_KEY'],
                model=self.config.get('GEMINI_MODEL', 'gemini-2.5-pro-preview-05-06'),  # 最新的Gemini 2.5 Pro Preview
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        logger.info(f"初始化了 {len(self.analyzers)} 个AI分析器: {list(self.analyzers.keys())}")
    
    def get_available_analyzers(self) -> List[AIProvider]:
        """获取可用的分析器列表"""
        return [provider for provider, analyzer in self.analyzers.items() if analyzer.is_available()]
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        分析论文
        
        Args:
            paper: 论文对象
            analysis_type: 分析类型
        
        Returns:
            分析结果
        """
        if self.strategy == AnalysisStrategy.FALLBACK:
            return await self._analyze_with_fallback(paper, analysis_type)
        elif self.strategy == AnalysisStrategy.PARALLEL:
            return await self._analyze_with_parallel(paper, analysis_type)
        elif self.strategy == AnalysisStrategy.CONSENSUS:
            return await self._analyze_with_consensus(paper, analysis_type)
        elif self.strategy == AnalysisStrategy.BEST_EFFORT:
            return await self._analyze_with_best_effort(paper, analysis_type)
        else:
            return await self._analyze_with_fallback(paper, analysis_type)
    
    async def _analyze_with_fallback(self, paper: arxiv.Result, analysis_type: str) -> Dict[str, Any]:
        """使用降级策略分析论文"""
        last_error = None
        
        for provider in self.fallback_order:
            analyzer = self.analyzers.get(provider)
            if not analyzer or not analyzer.is_available():
                logger.debug(f"跳过不可用的分析器: {provider}")
                continue
            
            try:
                logger.info(f"使用 {provider.value} 分析论文: {paper.title[:50]}...")
                result = await analyzer.analyze_paper(paper, analysis_type)
                logger.info(f"✅ {provider.value} 分析成功")
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"❌ {provider.value} 分析失败: {e}")
                continue
        
        # 所有分析器都失败了
        error_msg = f"所有AI提供商都不可用。最后错误: {last_error}"
        logger.error(error_msg)
        
        return {
            'analysis': PromptManager.get_error_analysis(str(last_error)),
            'provider': 'error',
            'model': 'none',
            'timestamp': time.time(),
            'html_analysis': PromptManager.format_analysis_for_html(PromptManager.get_error_analysis(str(last_error))),
            'error': str(last_error)
        }
    
    async def _analyze_with_parallel(self, paper: arxiv.Result, analysis_type: str) -> Dict[str, Any]:
        """使用并行策略分析论文"""
        available_analyzers = [(provider, analyzer) for provider, analyzer in self.analyzers.items() 
                              if analyzer.is_available()]
        
        if not available_analyzers:
            error_msg = "没有可用的AI分析器"
            return {
                'analysis': PromptManager.get_error_analysis(error_msg),
                'provider': 'error',
                'model': 'none',
                'timestamp': time.time(),
                'html_analysis': PromptManager.format_analysis_for_html(PromptManager.get_error_analysis(error_msg)),
                'error': error_msg
            }
        
        # 并行调用所有可用的分析器
        tasks = []
        for provider, analyzer in available_analyzers:
            task = asyncio.create_task(analyzer.analyze_paper(paper, analysis_type))
            tasks.append((provider, task))
        
        # 等待第一个成功的结果
        for provider, task in tasks:
            try:
                result = await task
                logger.info(f"✅ 并行分析成功，使用 {provider.value} 的结果")
                
                # 取消其他任务
                for other_provider, other_task in tasks:
                    if other_provider != provider and not other_task.done():
                        other_task.cancel()
                
                return result
                
            except Exception as e:
                logger.warning(f"❌ {provider.value} 并行分析失败: {e}")
                continue
        
        # 所有并行任务都失败了
        error_msg = "所有并行分析任务都失败了"
        return {
            'analysis': PromptManager.get_error_analysis(error_msg),
            'provider': 'error',
            'model': 'none',
            'timestamp': time.time(),
            'html_analysis': PromptManager.format_analysis_for_html(PromptManager.get_error_analysis(error_msg)),
            'error': error_msg
        }
    
    async def _analyze_with_consensus(self, paper: arxiv.Result, analysis_type: str, min_consensus: int = 2) -> Dict[str, Any]:
        """使用共识策略分析论文"""
        available_analyzers = [(provider, analyzer) for provider, analyzer in self.analyzers.items() 
                              if analyzer.is_available()]
        
        if len(available_analyzers) < min_consensus:
            logger.warning(f"可用分析器数量({len(available_analyzers)})少于最小共识数量({min_consensus})，降级为fallback策略")
            return await self._analyze_with_fallback(paper, analysis_type)
        
        # 并行调用多个分析器
        tasks = []
        for provider, analyzer in available_analyzers[:3]:  # 最多使用前3个
            task = asyncio.create_task(analyzer.analyze_paper(paper, analysis_type))
            tasks.append((provider, task))
        
        # 收集结果
        results = []
        for provider, task in tasks:
            try:
                result = await task
                results.append(result)
                logger.info(f"✅ {provider.value} 共识分析完成")
            except Exception as e:
                logger.warning(f"❌ {provider.value} 共识分析失败: {e}")
        
        if len(results) < min_consensus:
            error_msg = f"无法达成共识，只有 {len(results)} 个成功结果，需要至少 {min_consensus} 个"
            return {
                'analysis': PromptManager.get_error_analysis(error_msg),
                'provider': 'error',
                'model': 'none',
                'timestamp': time.time(),
                'html_analysis': PromptManager.format_analysis_for_html(PromptManager.get_error_analysis(error_msg)),
                'error': error_msg
            }
        
        # 合并结果（简化版本：使用第一个结果，但记录所有提供商）
        merged_result = results[0].copy()
        merged_result['providers'] = [r['provider'] for r in results]
        merged_result['consensus_count'] = len(results)
        merged_result['provider'] = f"consensus({len(results)})"
        
        logger.info(f"✅ 共识分析成功，使用了 {len(results)} 个分析器的结果")
        return merged_result
    
    async def _analyze_with_best_effort(self, paper: arxiv.Result, analysis_type: str) -> Dict[str, Any]:
        """使用尽力而为策略分析论文"""
        # 先尝试降级策略
        try:
            result = await self._analyze_with_fallback(paper, analysis_type)
            if result.get('provider') != 'error':
                return result
        except Exception:
            pass
        
        # 如果降级策略失败，尝试并行策略
        try:
            result = await self._analyze_with_parallel(paper, analysis_type)
            if result.get('provider') != 'error':
                return result
        except Exception:
            pass
        
        # 最后的降级方案
        error_msg = "所有分析策略都失败了"
        return {
            'analysis': PromptManager.get_error_analysis(error_msg),
            'provider': 'error',
            'model': 'none',
            'timestamp': time.time(),
            'html_analysis': PromptManager.format_analysis_for_html(PromptManager.get_error_analysis(error_msg)),
            'error': error_msg
        }
    
    def get_analyzer_status(self) -> Dict[str, Any]:
        """获取分析器状态"""
        status = {
            'strategy': self.strategy.value,
            'fallback_order': [p.value for p in self.fallback_order],
            'analyzers': {}
        }
        
        for provider, analyzer in self.analyzers.items():
            info = analyzer.get_provider_info()
            info['available'] = analyzer.is_available()
            status['analyzers'][provider.value] = info
        
        return status 