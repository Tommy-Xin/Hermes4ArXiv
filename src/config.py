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
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o3-2025-04-16")
        
        self.CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
        self.CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-20250514")
        
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-preview-05-06")
        
        # AI分析配置（使用智能降级策略）
        self.AI_FALLBACK_ORDER = os.getenv("AI_FALLBACK_ORDER", "deepseek,openai,claude,gemini")
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
