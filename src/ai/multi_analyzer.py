#!/usr/bin/env python3
"""
智能AI回退系统模块
支持单AI使用 + 智能回退策略，确保论文分析的高可靠性
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import arxiv
from collections import defaultdict

from .prompts import PromptManager

logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """AI提供商枚举"""
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"
    ZHIPU = "zhipu"  # 智谱AI


class FailureTracker:
    """失败跟踪器 - 跟踪API连续失败情况"""
    
    def __init__(self, max_consecutive_failures: int = 3, reset_time: int = 300):
        """
        初始化失败跟踪器
        
        Args:
            max_consecutive_failures: 最大连续失败次数
            reset_time: 失败计数重置时间（秒）
        """
        self.max_consecutive_failures = max_consecutive_failures
        self.reset_time = reset_time
        self.failure_counts = defaultdict(int)  # 每个provider的连续失败次数
        self.last_failure_time = defaultdict(float)  # 最后失败时间
        self.disabled_providers = set()  # 被禁用的provider
    
    def record_failure(self, provider: AIProvider) -> bool:
        """
        记录失败
        
        Args:
            provider: AI提供商
            
        Returns:
            是否应该禁用该provider
        """
        current_time = time.time()
        
        # 检查是否需要重置计数
        if (provider in self.last_failure_time and 
            current_time - self.last_failure_time[provider] > self.reset_time):
            self.failure_counts[provider] = 0
        
        self.failure_counts[provider] += 1
        self.last_failure_time[provider] = current_time
        
        # 检查是否达到最大失败次数
        if self.failure_counts[provider] >= self.max_consecutive_failures:
            self.disabled_providers.add(provider)
            logger.warning(f"🚫 {provider.value} 连续失败 {self.failure_counts[provider]} 次，暂时禁用")
            return True
        
        return False
    
    def record_success(self, provider: AIProvider):
        """记录成功，重置失败计数"""
        self.failure_counts[provider] = 0
        if provider in self.disabled_providers:
            self.disabled_providers.remove(provider)
            logger.info(f"✅ {provider.value} 恢复正常")
    
    def is_disabled(self, provider: AIProvider) -> bool:
        """检查provider是否被禁用"""
        return provider in self.disabled_providers
    
    def get_failure_info(self, provider: AIProvider) -> Dict[str, Any]:
        """获取失败信息"""
        return {
            'consecutive_failures': self.failure_counts.get(provider, 0),
            'is_disabled': self.is_disabled(provider),
            'last_failure_time': self.last_failure_time.get(provider, 0)
        }


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
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = "https://api.deepseek.com/v1"
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        import openai
        
        # 兼容不同版本的OpenAI库
        try:
            # 新版本 OpenAI (>=1.0.0)
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
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
            "description": "DeepSeek - 高性价比AI模型"
        }


class OpenAIAnalyzer(BaseAIAnalyzer):
    """OpenAI分析器"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.base_url = "https://api.openai.com/v1"
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        import openai
        
        # 兼容不同版本的OpenAI库
        try:
            # 新版本 OpenAI (>=1.0.0)
            client = openai.OpenAI(api_key=self.api_key)
            use_new_api = True
        except AttributeError:
            # 老版本 OpenAI (<1.0.0)
            openai.api_key = self.api_key
            use_new_api = False
        
        system_prompt = PromptManager.get_system_prompt(analysis_type)
        user_prompt = PromptManager.get_user_prompt(paper, analysis_type)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"OpenAI分析论文: {paper.title[:50]}... (尝试 {attempt + 1}/{self.retry_times})")
                
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
            "description": "OpenAI GPT - 业界领先AI模型"
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
                
                message = client.messages.create(
                    model=self.model,
                    max_tokens=1500,
                    temperature=0.7,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                
                analysis = message.content[0].text
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
            "description": "Anthropic Claude - 安全可靠AI助手"
        }


class GeminiAnalyzer(BaseAIAnalyzer):
    """Gemini分析器 - 使用增强版修复器，解决安全过滤器问题"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-pro-preview-05-06", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.fixer = None
        self._initialize_fixer()
    
    def _initialize_fixer(self):
        """初始化Gemini修复器"""
        try:
            # 导入我们的修复器
            from ai.gemini_fix import GeminiAPIFixer
            
            self.fixer = GeminiAPIFixer(
                api_key=self.api_key,
                model=self.model,
                retry_times=self.retry_times,
                delay=self.delay
            )
            logger.info(f"✅ Gemini修复器初始化成功，模型: {self.model}")
        except Exception as e:
            logger.error(f"❌ Gemini修复器初始化失败: {e}")
            self.fixer = None
            self.is_available_flag = False
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """分析论文"""
        if not self.fixer:
            raise Exception("Gemini修复器未初始化")
        
        try:
            logger.info(f"Gemini修复器分析论文: {paper.title[:50]}...")
            
            # 使用我们的修复器进行分析
            result = await self.fixer.analyze_paper(paper, analysis_type)
            
            if result:
                logger.info(f"✅ Gemini修复器分析完成: {paper.title[:50]}...")
                
                # 确保返回正确的格式
                return {
                    'analysis': result['analysis'],
                    'provider': 'gemini',
                    'model': result['model'],
                    'timestamp': result['timestamp'],
                    'html_analysis': PromptManager.format_analysis_for_html(result['analysis']),
                    'api_version': result.get('api_version', 'unknown'),
                    'analysis_type': result.get('analysis_type', analysis_type)
                }
            else:
                raise Exception("Gemini修复器返回空结果，可能是地理位置限制或其他问题")
                
        except Exception as e:
            logger.error(f"❌ Gemini修复器分析失败: {str(e)}")
            # 检查是否是地理位置限制
            if "location is not supported" in str(e).lower():
                logger.error("🌍 Gemini API地理位置限制 - 在GitHub Actions中不应出现此错误")
            raise e
    
    def get_provider_info(self) -> Dict[str, str]:
        return {
            "name": "Gemini Enhanced",
            "provider": "gemini",
            "model": self.model,
            "description": "Google Gemini with Enhanced Safety Filter Fix",
            "api_version": getattr(self.fixer, 'api_version', 'unknown') if self.fixer else 'unavailable'
        }


class MultiAIAnalyzer:
    """
    智能AI回退系统 - 主AI + 备用AI降级策略
    
    工作原理：
    1. 优先使用您配置的主要AI（如Gemini 2.5 Pro Preview）
    2. 当主AI失败时，自动切换到备用AI（如DeepSeek）
    3. 每篇论文只使用一个AI分析，确保成本可控
    4. 支持智能失败检测和临时禁用机制
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.analyzers: Dict[AIProvider, BaseAIAnalyzer] = {}
        self.fallback_order = self._parse_fallback_order()
        self.failure_tracker = FailureTracker(
            max_consecutive_failures=config.get('MAX_CONSECUTIVE_FAILURES', 3),
            reset_time=config.get('FAILURE_RESET_TIME', 300)
        )
        self._initialize_analyzers()
    
    def _parse_fallback_order(self) -> List[AIProvider]:
        """解析使用顺序 - 支持用户指定优先模型"""
        
        # 🎯 优先检查用户指定的模型
        preferred_model = self.config.get('PREFERRED_AI_MODEL', '').lower().strip()
        if preferred_model:
            try:
                preferred_provider = AIProvider(preferred_model)
                # 检查该模型是否可用
                if self.config.get(f'{preferred_model.upper()}_API_KEY'):
                    logger.info(f"🎯 使用用户指定的AI模型: {preferred_model}")
                    return [preferred_provider]  # 只使用用户指定的模型
                else:
                    logger.warning(f"⚠️ 用户指定的模型 {preferred_model} 没有配置API密钥，使用自动选择")
            except ValueError:
                logger.warning(f"⚠️ 用户指定的模型 {preferred_model} 不支持，使用自动选择")
        
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
                model=self.config.get('OPENAI_MODEL', 'o3-2025-04-16'),
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        # Claude - 默认使用Claude Opus 4（2025年最强模型）
        if self.config.get('CLAUDE_API_KEY'):
            self.analyzers[AIProvider.CLAUDE] = ClaudeAnalyzer(
                api_key=self.config['CLAUDE_API_KEY'],
                model=self.config.get('CLAUDE_MODEL', 'claude-opus-4-20250514'),
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        # Gemini - 默认使用Gemini 2.5 Pro Preview（2025年最新SOTA）
        if self.config.get('GEMINI_API_KEY'):
            self.analyzers[AIProvider.GEMINI] = GeminiAnalyzer(
                api_key=self.config['GEMINI_API_KEY'],
                model=self.config.get('GEMINI_MODEL', 'gemini-2.5-pro-preview-05-06'),
                retry_times=self.config.get('API_RETRY_TIMES', 3),
                delay=self.config.get('API_DELAY', 2)
            )
        
        logger.info(f"初始化了 {len(self.analyzers)} 个AI分析器: {list(self.analyzers.keys())}")
    
    def get_available_analyzers(self) -> List[AIProvider]:
        """获取可用的分析器列表（排除被禁用的）"""
        return [
            provider for provider, analyzer in self.analyzers.items() 
            if analyzer.is_available() and not self.failure_tracker.is_disabled(provider)
        ]
    
    async def analyze_paper(self, paper: arxiv.Result, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        分析论文 - 使用降级策略
        
        Args:
            paper: 论文对象
            analysis_type: 分析类型
        
        Returns:
            分析结果
        """
        return await self._analyze_with_fallback(paper, analysis_type)
    
    async def _analyze_with_fallback(self, paper: arxiv.Result, analysis_type: str) -> Dict[str, Any]:
        """使用降级策略分析论文 - 增强版本，支持智能跳过失败的AI"""
        last_error = None
        attempted_providers = []
        
        # 获取可用的provider列表（排除被禁用的）
        available_providers = [
            provider for provider in self.fallback_order
            if (provider in self.analyzers and 
                self.analyzers[provider].is_available() and
                not self.failure_tracker.is_disabled(provider))
        ]
        
        if not available_providers:
            # 所有provider都被禁用，尝试重置一些失败计数
            logger.warning("所有AI提供商都被禁用，尝试重置部分失败计数")
            self._reset_some_failures()
            available_providers = [
                provider for provider in self.fallback_order
                if (provider in self.analyzers and 
                    self.analyzers[provider].is_available() and
                    not self.failure_tracker.is_disabled(provider))
            ]
        
        for provider in available_providers:
            analyzer = self.analyzers.get(provider)
            attempted_providers.append(provider)
            
            try:
                logger.info(f"使用 {provider.value} 分析论文: {paper.title[:50]}...")
                result = await analyzer.analyze_paper(paper, analysis_type)
                
                # 记录成功
                self.failure_tracker.record_success(provider)
                logger.info(f"✅ {provider.value} 分析成功")
                return result
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # 记录失败
                should_disable = self.failure_tracker.record_failure(provider)
                
                # 特殊处理Gemini安全过滤器问题
                if provider == AIProvider.GEMINI and "GEMINI_SAFETY_FILTER_REPEATEDLY_TRIGGERED" in error_msg:
                    logger.error(f"❌ {provider.value} 多次触发安全过滤器，建议使用其他AI模型")
                elif should_disable:
                    logger.warning(f"⚠️ {provider.value} 被暂时禁用，将尝试其他AI")
                else:
                    logger.warning(f"❌ {provider.value} 分析失败: {error_msg[:100]}...")
                
                continue
        
        # 所有分析器都失败了，返回None表示完全失败
        error_msg = f"所有可用的AI提供商都失败了。尝试过的提供商: {[p.value for p in attempted_providers]}。最后错误: {last_error}"
        logger.error(error_msg)
        
        # 生成失败统计用于日志记录
        failure_stats = self._get_failure_stats()
        logger.info(f"失败统计: {failure_stats}")
        
        # 返回None表示彻底失败，需要发送邮件通知
        return None
    
    def _reset_some_failures(self):
        """重置一些失败计数，给AI一次重新尝试的机会"""
        for provider in self.failure_tracker.disabled_providers.copy():
            if provider != AIProvider.GEMINI:  # Gemini安全过滤器问题通常是持续性的
                self.failure_tracker.failure_counts[provider] = max(0, self.failure_tracker.failure_counts[provider] - 1)
                if self.failure_tracker.failure_counts[provider] < self.failure_tracker.max_consecutive_failures:
                    self.failure_tracker.disabled_providers.remove(provider)
                    logger.info(f"🔄 重置 {provider.value} 失败计数，给予重试机会")
    
    def _get_failure_stats(self) -> Dict[str, Any]:
        """获取失败统计信息"""
        stats = {}
        for provider in self.analyzers.keys():
            stats[provider.value] = self.failure_tracker.get_failure_info(provider)
        return stats
    
    def get_analyzer_status(self) -> Dict[str, Any]:
        """获取分析器状态"""
        status = {
            'strategy': 'fallback',  # 简化：只使用fallback策略
            'fallback_order': [p.value for p in self.fallback_order],
            'analyzers': {},
            'failure_stats': self._get_failure_stats()
        }
        
        for provider, analyzer in self.analyzers.items():
            info = analyzer.get_provider_info()
            info['available'] = analyzer.is_available()
            info['disabled'] = self.failure_tracker.is_disabled(provider)
            info['failure_info'] = self.failure_tracker.get_failure_info(provider)
            status['analyzers'][provider.value] = info
        
        return status 