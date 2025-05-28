#!/usr/bin/env python3
"""
Gemini API修复器 - 针对GitHub Actions环境优化
支持新旧API版本，解决安全过滤器问题
特别支持gemini-2.5-pro-preview-05-06模型
"""

import asyncio
import logging
import os
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAPIFixer:
    """
    Gemini API修复器
    - 自动检测并使用最佳可用API版本
    - 智能安全设置，避免过滤器拦截
    - 专门优化GitHub Actions环境
    - 支持gemini-2.5-pro-preview-05-06等最新模型
    """
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-pro-preview-05-06", 
                 retry_times: int = 3, delay: int = 2):
        self.api_key = api_key
        self.model = model
        self.retry_times = retry_times
        self.delay = delay
        self.api_version = None
        self.client = None
        
        # 初始化API客户端
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化最佳可用的API客户端"""
        # 尝试新版API (google-genai)
        try:
            import google.genai as genai
            from google.genai import types
            
            self.client = genai.Client(api_key=self.api_key)
            self.api_version = "new"
            self.genai = genai
            self.types = types
            
            logger.info(f"✅ 使用新版Google GenAI SDK - 模型: {self.model}")
            return
            
        except ImportError as e:
            logger.warning(f"⚠️ 新版API不可用: {e}")
        
        # 回退到旧版API (google-generativeai)
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            self.client = genai
            self.api_version = "legacy"
            self.genai = genai
            
            logger.info(f"✅ 使用旧版google-generativeai库 - 模型: {self.model}")
            return
            
        except ImportError:
            logger.error("❌ 没有可用的Gemini API库！")
            raise ImportError("请安装 google-genai 或 google-generativeai")
    
    def _get_safety_settings(self) -> Any:
        """获取最宽松的安全设置，针对不同API版本"""
        
        if self.api_version == "new":
            # 新版API安全设置 - 支持gemini-2.5系列
            return [
                self.types.SafetySetting(
                    category=self.types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=self.types.HarmBlockThreshold.BLOCK_NONE
                ),
                self.types.SafetySetting(
                    category=self.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, 
                    threshold=self.types.HarmBlockThreshold.BLOCK_NONE
                ),
                self.types.SafetySetting(
                    category=self.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=self.types.HarmBlockThreshold.BLOCK_NONE
                ),
                self.types.SafetySetting(
                    category=self.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=self.types.HarmBlockThreshold.BLOCK_NONE
                )
            ]
        else:
            # 旧版API安全设置
            return [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
    
    def _create_academic_prompt(self, paper, analysis_type: str = "comprehensive") -> str:
        """创建学术化提示，避免触发安全过滤器"""
        
        # 基础学术分析提示
        base_prompt = f"""作为专业的学术研究分析师，请对以下arXiv论文进行客观、严谨的学术分析：

论文标题：{paper.title}

论文摘要：{paper.summary}

作者：{', '.join(paper.authors) if hasattr(paper, 'authors') and paper.authors else '未知'}

发表时间：{paper.published.strftime('%Y-%m-%d') if hasattr(paper, 'published') else '未知'}

分类：{', '.join(paper.categories) if hasattr(paper, 'categories') and paper.categories else '未知'}"""

        if analysis_type == "comprehensive":
            analysis_prompt = """

请提供全面的学术分析，包括：

1. **研究背景与动机**
   - 研究问题的重要性和现实意义
   - 填补的学术空白

2. **技术创新点**
   - 关键技术贡献
   - 方法论创新
   - 算法或架构改进

3. **实验设计与结果**
   - 实验方法的科学性
   - 关键性能指标
   - 与现有方法的比较

4. **学术价值评估**
   - 理论贡献的重要性
   - 对相关领域的影响
   - 潜在应用价值

5. **不足与展望**
   - 存在的局限性
   - 未来研究方向

请保持客观、专业的学术语调，基于论文内容进行分析。"""

        elif analysis_type == "summary":
            analysis_prompt = """

请提供简洁的学术总结，包括：
1. 核心研究内容
2. 主要技术贡献  
3. 关键实验结果
4. 学术意义

请用专业、客观的语言进行分析。"""

        else:  # basic
            analysis_prompt = """

请简要分析这篇论文的：
1. 研究目标
2. 技术方法
3. 主要贡献

请保持学术客观性。"""

        return base_prompt + analysis_prompt
    
    async def analyze_paper(self, paper, analysis_type: str = "comprehensive") -> Optional[Dict[str, Any]]:
        """
        分析论文，支持重试机制
        
        Args:
            paper: 论文对象，包含title, summary等属性
            analysis_type: 分析类型 ("comprehensive", "summary", "basic")
        
        Returns:
            分析结果字典或None
        """
        
        prompt = self._create_academic_prompt(paper, analysis_type)
        
        for attempt in range(self.retry_times):
            try:
                logger.info(f"🔍 尝试分析论文 (第{attempt+1}次): {paper.title[:50]}...")
                
                if self.api_version == "new":
                    result = await self._analyze_with_new_api(prompt)
                else:
                    result = await self._analyze_with_legacy_api(prompt)
                
                if result:
                    logger.info(f"✅ 论文分析成功！长度: {len(result)} 字符")
                    return {
                        'analysis': result,
                        'model': self.model,
                        'api_version': self.api_version,
                        'provider': 'google_gemini',
                        'timestamp': datetime.now().isoformat(),
                        'analysis_type': analysis_type
                    }
                else:
                    logger.warning(f"⚠️ 第{attempt+1}次尝试返回空结果")
                    
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"⚠️ 第{attempt+1}次尝试失败: {error_msg}")
                
                # 特定错误处理
                if "location is not supported" in error_msg.lower():
                    logger.error("❌ 地理位置限制错误 - 但在GitHub Actions中不应出现此错误")
                    break
                elif "safety" in error_msg.lower() or "blocked" in error_msg.lower():
                    logger.warning("🛡️ 安全过滤器触发，调整提示...")
                elif "not found" in error_msg.lower():
                    logger.error(f"❌ 模型 {self.model} 未找到")
                    break
                
                if attempt < self.retry_times - 1:
                    await asyncio.sleep(self.delay)
        
        logger.error(f"❌ 论文分析失败，已重试{self.retry_times}次")
        return None
    
    async def _analyze_with_new_api(self, prompt: str) -> Optional[str]:
        """使用新版API进行分析"""
        safety_settings = self._get_safety_settings()
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=self.types.GenerateContentConfig(
                max_output_tokens=2000,
                temperature=0.7,
                safety_settings=safety_settings,
                top_p=0.95,
                top_k=40
            )
        )
        
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        return None
    
    async def _analyze_with_legacy_api(self, prompt: str) -> Optional[str]:
        """使用旧版API进行分析"""
        safety_settings = self._get_safety_settings()
        
        # 确保模型名称格式正确
        model_name = self.model
        if not model_name.startswith('models/'):
            model_name = f'models/{model_name}'
        
        model = self.genai.GenerativeModel(model_name)
        
        response = model.generate_content(
            prompt,
            generation_config=self.genai.types.GenerationConfig(
                max_output_tokens=2000,
                temperature=0.7,
                top_p=0.95,
                top_k=40,
            ),
            safety_settings=safety_settings
        )
        
        if response.text:
            return response.text.strip()
        return None
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            test_prompt = "请简要介绍人工智能的发展历史。"
            
            if self.api_version == "new":
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=test_prompt,
                    config=self.types.GenerateContentConfig(
                        max_output_tokens=100,
                        temperature=0.5
                    )
                )
                return hasattr(response, 'text') and bool(response.text)
            else:
                model_name = self.model
                if not model_name.startswith('models/'):
                    model_name = f'models/{model_name}'
                    
                model = self.genai.GenerativeModel(model_name)
                response = model.generate_content(
                    test_prompt,
                    generation_config=self.genai.types.GenerationConfig(
                        max_output_tokens=100,
                        temperature=0.5
                    )
                )
                return bool(response.text)
                
        except Exception as e:
            logger.error(f"❌ 连接测试失败: {str(e)}")
            return False

# 便捷函数，用于GitHub Actions环境
def create_gemini_analyzer(api_key: Optional[str] = None, 
                          model: str = "gemini-2.5-pro-preview-05-06") -> GeminiAPIFixer:
    """
    创建Gemini分析器实例 - 专为GitHub Actions优化
    
    Args:
        api_key: API密钥，如果未提供则从环境变量获取
        model: 模型名称，默认使用最新的2.5 Pro Preview
    
    Returns:
        GeminiAPIFixer实例
    """
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("未设置GEMINI_API_KEY环境变量")
    
    return GeminiAPIFixer(api_key=api_key, model=model) 