#!/usr/bin/env python3
"""
AI分析器适配器
提供与现有代码的兼容性，同时支持新的多AI功能
"""

import asyncio
import logging
import time
from typing import Dict, Any
import arxiv

from ai.multi_analyzer import MultiAIAnalyzer
from ai.prompts import PromptManager

logger = logging.getLogger(__name__)


class AIAnalyzerAdapter:
    """AI分析器适配器，兼容现有接口"""
    
    def __init__(self, config):
        """
        初始化适配器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.multi_analyzer = None
        self.analysis_type = getattr(config, 'ANALYSIS_TYPE', 'comprehensive')
        
        # 检查是否启用多AI功能
        self.enable_multi_ai = self._should_enable_multi_ai()
        
        if self.enable_multi_ai:
            self._initialize_multi_ai()
        else:
            self._initialize_legacy_ai()
    
    def _should_enable_multi_ai(self) -> bool:
        """判断是否应该启用多AI功能"""
        # 检查是否有任何AI API密钥配置
        ai_keys = [
            getattr(self.config, 'DEEPSEEK_API_KEY', None),
            getattr(self.config, 'OPENAI_API_KEY', None),
            getattr(self.config, 'CLAUDE_API_KEY', None),
            getattr(self.config, 'GEMINI_API_KEY', None),
        ]
        
        # 统计有效的API密钥数量
        valid_keys = sum(1 for key in ai_keys if key and len(key) > 10)
        
        # 如果有任何一个API密钥，启用多AI（单模型策略）
        return valid_keys > 0
    
    def _initialize_multi_ai(self):
        """初始化多AI分析器"""
        try:
            # 将配置对象转换为字典
            config_dict = {}
            for attr in dir(self.config):
                if not attr.startswith('_'):
                    config_dict[attr] = getattr(self.config, attr)
            
            self.multi_analyzer = MultiAIAnalyzer(config_dict)
            logger.info("✅ 多AI分析器初始化成功")
            
            # 打印分析器状态
            status = self.multi_analyzer.get_analyzer_status()
            available_analyzers = [name for name, info in status['analyzers'].items() if info['available']]
            logger.info(f"🤖 可用的AI分析器: {available_analyzers}")
            logger.info(f"📋 分析策略: {status['strategy']}")
            
        except Exception as e:
            logger.error(f"❌ 多AI分析器初始化失败: {e}")
            logger.info("🔄 降级到传统单AI模式")
            self.enable_multi_ai = False
            self._initialize_legacy_ai()
    
    def _initialize_legacy_ai(self):
        """初始化传统单AI分析器"""
        try:
            from ai.analyzers.legacy import AnalyzerFactory
            
            # 检查是否有DeepSeek API密钥
            if not hasattr(self.config, 'DEEPSEEK_API_KEY') or not self.config.DEEPSEEK_API_KEY:
                logger.error("❌ 未配置DEEPSEEK_API_KEY，无法初始化传统AI分析器")
                self.legacy_analyzer = None
                return
                
            self.legacy_analyzer = AnalyzerFactory.create_analyzer(
                "deepseek",
                api_key=self.config.DEEPSEEK_API_KEY,
                model=getattr(self.config, 'AI_MODEL', 'deepseek-chat'),
                retry_times=getattr(self.config, 'API_RETRY_TIMES', 3),
                delay=getattr(self.config, 'API_DELAY', 2),
            )
            logger.info("✅ 传统AI分析器初始化成功")
        except Exception as e:
            logger.error(f"❌ 传统AI分析器初始化失败: {e}")
            self.legacy_analyzer = None
    
    def analyze_paper(self, paper: arxiv.Result) -> str:
        """
        分析论文（同步接口，兼容现有代码）
        
        Args:
            paper: 论文对象
        
        Returns:
            分析结果文本
        """
        if self.enable_multi_ai:
            return self._analyze_with_multi_ai(paper)
        else:
            return self._analyze_with_legacy_ai(paper)
    
    def _analyze_with_multi_ai(self, paper: arxiv.Result) -> str:
        """使用多AI分析器分析论文"""
        try:
            # 运行异步分析
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.multi_analyzer.analyze_paper(paper, self.analysis_type)
                )
                
                # 检查结果是否为None（所有AI模型都失败）
                if result is None:
                    logger.error("❌ 多AI分析返回None结果 - 所有AI模型都失败")
                    return None  # 返回None表示彻底失败，需要发送邮件通知
                
                # 提取分析文本
                analysis_text = result.get('analysis', '')
                provider = result.get('provider', 'unknown')
                model = result.get('model', 'unknown')
                
                logger.info(f"✅ 多AI分析完成，使用: {provider} ({model})")
                
                # 如果有错误，记录但仍返回结果
                if 'error' in result:
                    logger.warning(f"⚠️ 分析过程中有错误: {result['error']}")
                
                return analysis_text or PromptManager.get_error_analysis("AI分析结果为空")
                
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"❌ 多AI分析失败: {e}")
            # 降级到传统分析器
            logger.info("🔄 降级到传统AI分析器")
            return self._analyze_with_legacy_ai(paper)
    
    def _analyze_with_legacy_ai(self, paper: arxiv.Result) -> str:
        """使用传统AI分析器分析论文"""
        try:
            # 检查传统分析器是否已初始化
            if not hasattr(self, 'legacy_analyzer') or self.legacy_analyzer is None:
                logger.error("❌ 传统AI分析器未初始化")
                return PromptManager.get_error_analysis("传统AI分析器未初始化")
            
            analysis = self.legacy_analyzer.analyze_paper(paper)
            logger.info("✅ 传统AI分析完成")
            return analysis or PromptManager.get_error_analysis("传统AI分析结果为空")
        except Exception as e:
            logger.error(f"❌ 传统AI分析失败: {e}")
            # 返回错误分析
            return PromptManager.get_error_analysis(str(e))
    
    async def analyze_paper_async(self, paper: arxiv.Result) -> Dict[str, Any]:
        """
        异步分析论文（新接口，提供更多信息）
        
        Args:
            paper: 论文对象
        
        Returns:
            详细的分析结果
        """
        if self.enable_multi_ai:
            return await self.multi_analyzer.analyze_paper(paper, self.analysis_type)
        else:
            # 将传统分析器的结果包装成新格式
            try:
                # 检查传统分析器是否已初始化
                if not hasattr(self, 'legacy_analyzer') or self.legacy_analyzer is None:
                    error_analysis = PromptManager.get_error_analysis("传统AI分析器未初始化")
                    return {
                        'analysis': error_analysis,
                        'provider': 'error',
                        'model': 'none',
                        'timestamp': time.time(),
                        'html_analysis': PromptManager.format_analysis_for_html(error_analysis),
                        'error': '传统AI分析器未初始化'
                    }
                    
                analysis = self.legacy_analyzer.analyze_paper(paper)
                return {
                    'analysis': analysis or PromptManager.get_error_analysis("传统AI分析结果为空"),
                    'provider': 'deepseek',
                    'model': getattr(self.config, 'AI_MODEL', 'deepseek-chat'),
                    'timestamp': time.time(),
                    'html_analysis': PromptManager.format_analysis_for_html(analysis or "分析失败")
                }
            except Exception as e:
                error_analysis = PromptManager.get_error_analysis(str(e))
                return {
                    'analysis': error_analysis,
                    'provider': 'error',
                    'model': 'none',
                    'timestamp': time.time(),
                    'html_analysis': PromptManager.format_analysis_for_html(error_analysis),
                    'error': str(e)
                }
    
    def get_analyzer_info(self) -> Dict[str, Any]:
        """获取分析器信息"""
        if self.enable_multi_ai:
            status = self.multi_analyzer.get_analyzer_status()
            return {
                'type': 'multi_ai',
                'status': status,
                'analysis_type': self.analysis_type
            }
        else:
            return {
                'type': 'legacy',
                'provider': 'deepseek',
                'model': getattr(self.config, 'AI_MODEL', 'deepseek-chat'),
                'analysis_type': self.analysis_type
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """测试AI连接"""
        if self.enable_multi_ai:
            available_analyzers = self.multi_analyzer.get_available_analyzers()
            return {
                'multi_ai_enabled': True,
                'available_analyzers': [analyzer.value for analyzer in available_analyzers],
                'total_analyzers': len(self.multi_analyzer.analyzers),
                'strategy': self.multi_analyzer.strategy.value
            }
        else:
            # 测试传统分析器
            try:
                # 这里可以添加简单的连接测试
                return {
                    'multi_ai_enabled': False,
                    'legacy_analyzer': 'deepseek',
                    'status': 'available' if hasattr(self, 'legacy_analyzer') else 'unavailable'
                }
            except Exception as e:
                return {
                    'multi_ai_enabled': False,
                    'legacy_analyzer': 'deepseek',
                    'status': 'error',
                    'error': str(e)
                }


# 工厂函数，用于创建适配器
def create_ai_analyzer(config) -> AIAnalyzerAdapter:
    """
    创建AI分析器适配器
    
    Args:
        config: 配置对象
    
    Returns:
        AI分析器适配器实例
    """
    return AIAnalyzerAdapter(config) 