#!/usr/bin/env python3
"""
配置管理模块
集中管理所有配置项，便于维护和扩展
"""

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """配置类，管理所有配置项"""

    def _clean_string(self, value: str) -> str:
        """清理字符串中的特殊字符"""
        if not value:
            return value
        # 移除不间断空格和其他不可见字符
        return value.replace('\xa0', ' ').strip()

    def _safe_int(self, value: str, default: str) -> int:
        """安全的整数转换，处理空字符串和None"""
        if not value or not value.strip():
            return int(default)
        return int(value.strip())

    def __init__(self):
        """初始化配置，从环境变量读取"""
        # AI API配置
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        self.DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
        self.DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        # 多AI支持
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o3")
        
        self.CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
        self.CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-4-opus-20250514")
        
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-preview-05-06")
        
        # 🎯 用户自定义模型配置 - 支持各AI提供商的精确模型选择
        self.CUSTOM_MODEL_CONFIG = self._parse_custom_models()
        
        # AI分析配置（使用智能降级策略）
        self.AI_FALLBACK_ORDER = os.getenv("AI_FALLBACK_ORDER", "gemini,claude,openai,deepseek")  # SOTA优先
        self.ANALYSIS_TYPE = os.getenv("ANALYSIS_TYPE", "comprehensive")
        
        # 🎯 用户指定使用的AI模型 (优先级最高)
        self.PREFERRED_AI_MODEL = os.getenv("PREFERRED_AI_MODEL", "").lower().strip()  # deepseek, openai, claude, gemini
        
        # 失败检测和处理配置
        self.MAX_CONSECUTIVE_FAILURES = self._safe_int(os.getenv("MAX_CONSECUTIVE_FAILURES"), "3")  # 最大连续失败次数
        self.FAILURE_RESET_TIME = self._safe_int(os.getenv("FAILURE_RESET_TIME"), "300")  # 失败计数重置时间（秒）

        # 邮件配置
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = self._safe_int(os.getenv("SMTP_PORT"), "587")
        self.SMTP_USERNAME = self._clean_string(os.getenv("SMTP_USERNAME"))
        self.SMTP_PASSWORD = self._clean_string(os.getenv("SMTP_PASSWORD"))
        self.EMAIL_FROM = os.getenv("EMAIL_FROM")
        self.EMAIL_TO = [
            email.strip() for email in os.getenv("EMAIL_TO", "").split(",") if email.strip()
        ]

        # 文件路径配置
        self.BASE_DIR = Path(__file__).parent
        self.PAPERS_DIR = self.BASE_DIR / "storage" / "papers"
        self.CONCLUSION_FILE = self.BASE_DIR / "storage" / "conclusion.md"
        self.TEMPLATES_DIR = self.BASE_DIR / "output" / "templates"

        # ArXiv搜索配置
        categories_str = os.getenv("CATEGORIES", "cs.AI,cs.LG,cs.CL")
        self.CATEGORIES = [cat.strip() for cat in categories_str.split(",") if cat.strip()]
        self.MAX_PAPERS = self._safe_int(os.getenv("MAX_PAPERS"), "50")
        self.SEARCH_DAYS = self._safe_int(os.getenv("SEARCH_DAYS"), "2")

        # AI分析配置
        self.AI_MODEL = "deepseek-chat"
        self.API_RETRY_TIMES = 3  # API重试次数
        self.API_DELAY = 2  # API调用间隔（秒）

        # 并行处理配置
        self.ENABLE_PARALLEL = os.getenv("ENABLE_PARALLEL", "true").lower() == "true"
        self.MAX_WORKERS = self._safe_int(os.getenv("MAX_WORKERS"), "0")  # 0表示自动计算
        self.BATCH_SIZE = self._safe_int(os.getenv("BATCH_SIZE"), "20")

        # 输出配置
        self.OUTPUT_FORMAT = "markdown"  # 输出格式：markdown, html
        self.EMAIL_FORMAT = "html"  # 邮件格式：html, text
        
        # GitHub仓库配置
        self.GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/your-username/hermes4arxiv")

    def validate(self) -> bool:
        """验证配置是否完整"""
        # 检查至少有一个AI API密钥
        ai_apis = [
            self.DEEPSEEK_API_KEY,
            self.OPENAI_API_KEY,
            self.CLAUDE_API_KEY,
            self.GEMINI_API_KEY
        ]
        
        if not any(ai_apis):
            print("❌ 至少需要配置一个AI API密钥：DEEPSEEK_API_KEY, OPENAI_API_KEY, CLAUDE_API_KEY, 或 GEMINI_API_KEY")
            return False
        
        # 检查邮件配置
        required_email_configs = [
            self.SMTP_SERVER,
            self.SMTP_USERNAME,
            self.SMTP_PASSWORD,
            self.EMAIL_FROM,
        ]

        missing_email_configs = [config for config in required_email_configs if not config]

        if missing_email_configs:
            print(f"❌ 缺少必要的邮件配置: {missing_email_configs}")
            return False

        if not self.EMAIL_TO:
            print("❌ 缺少收件人邮箱配置 (EMAIL_TO)")
            return False

        # 显示配置的AI模型
        configured_ais = []
        if self.DEEPSEEK_API_KEY:
            configured_ais.append("DeepSeek")
        if self.OPENAI_API_KEY:
            configured_ais.append("OpenAI")
        if self.CLAUDE_API_KEY:
            configured_ais.append("Claude")
        if self.GEMINI_API_KEY:
            configured_ais.append("Gemini")
        
        print(f"✅ 配置验证通过！已配置的AI模型: {', '.join(configured_ais)}")
        
        if self.PREFERRED_AI_MODEL:
            print(f"🎯 用户指定使用: {self.PREFERRED_AI_MODEL.upper()}")

        return True

    def create_directories(self):
        """创建必要的目录"""
        self.PAPERS_DIR.mkdir(parents=True, exist_ok=True)
        self.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        # 创建日志目录
        (self.BASE_DIR / "storage" / "logs").mkdir(parents=True, exist_ok=True)

    def _parse_custom_models(self) -> dict:
        """
        解析用户自定义模型配置
        
        支持的环境变量格式：
        CUSTOM_OPENAI_MODELS="o4-mini,o3,o3-mini,o1-preview,gpt-4-turbo"
        CUSTOM_CLAUDE_MODELS="claude-4-opus-20250514,claude-4-sonnet-20250514,claude-3-5-sonnet-20241022"
        CUSTOM_GEMINI_MODELS="gemini-2.5-pro-preview-05-06,gemini-2.0-flash-exp,gemini-1.5-pro"
        CUSTOM_DEEPSEEK_MODELS="deepseek-chat,deepseek-coder"
        
        或者单个模型覆盖：
        PREFERRED_OPENAI_MODEL="o4-mini"
        PREFERRED_CLAUDE_MODEL="claude-4-opus-20250514"
        
        Returns:
            dict: 包含各AI提供商可用模型列表的字典
        """
        config = {
            'openai': {
                'available_models': self._parse_model_list(
                    os.getenv("CUSTOM_OPENAI_MODELS", ""), 
                    ["o4-mini", "o3", "o3-mini", "o1-preview", "gpt-4-turbo", "gpt-4o"]
                ),
                'preferred_model': os.getenv("PREFERRED_OPENAI_MODEL", "").strip(),
                'default_model': "o3"
            },
            'claude': {
                'available_models': self._parse_model_list(
                    os.getenv("CUSTOM_CLAUDE_MODELS", ""),
                    ["claude-4-opus-20250514", "claude-4-sonnet-20250514", "claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"]
                ),
                'preferred_model': os.getenv("PREFERRED_CLAUDE_MODEL", "").strip(),
                'default_model': "claude-4-opus-20250514"
            },
            'gemini': {
                'available_models': self._parse_model_list(
                    os.getenv("CUSTOM_GEMINI_MODELS", ""),
                    ["gemini-2.5-pro-preview-05-06", "gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"]
                ),
                'preferred_model': os.getenv("PREFERRED_GEMINI_MODEL", "").strip(),
                'default_model': "gemini-2.5-pro-preview-05-06"
            },
            'deepseek': {
                'available_models': self._parse_model_list(
                    os.getenv("CUSTOM_DEEPSEEK_MODELS", ""),
                    ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"]
                ),
                'preferred_model': os.getenv("PREFERRED_DEEPSEEK_MODEL", "").strip(),
                'default_model': "deepseek-chat"
            }
        }
        
        return config
    
    def _parse_model_list(self, env_value: str, default_models: List[str]) -> List[str]:
        """解析模型列表字符串"""
        if env_value and env_value.strip():
            return [model.strip() for model in env_value.split(",") if model.strip()]
        return default_models
    
    def get_model_for_provider(self, provider: str) -> str:
        """
        获取指定AI提供商的模型
        
        优先级：
        1. 用户指定的首选模型 (PREFERRED_XXX_MODEL)
        2. 环境变量配置的模型 (XXX_MODEL)
        3. 默认SOTA模型
        
        Args:
            provider: AI提供商名称 (openai, claude, gemini, deepseek)
            
        Returns:
            str: 模型名称
        """
        provider = provider.lower()
        
        if provider not in self.CUSTOM_MODEL_CONFIG:
            return getattr(self, f"{provider.upper()}_MODEL", "")
        
        config = self.CUSTOM_MODEL_CONFIG[provider]
        
        # 1. 检查用户首选模型
        if config['preferred_model']:
            return config['preferred_model']
        
        # 2. 检查环境变量配置
        env_model = getattr(self, f"{provider.upper()}_MODEL", "")
        if env_model:
            return env_model
            
        # 3. 返回默认模型
        return config['default_model']
    
    def get_available_models_for_provider(self, provider: str) -> List[str]:
        """获取指定AI提供商的可用模型列表"""
        provider = provider.lower()
        if provider in self.CUSTOM_MODEL_CONFIG:
            return self.CUSTOM_MODEL_CONFIG[provider]['available_models']
        return []
