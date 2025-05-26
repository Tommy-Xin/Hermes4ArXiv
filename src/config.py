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

    # API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

    # 邮件配置
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_TO = [
        email.strip() for email in os.getenv("EMAIL_TO", "").split(",") if email.strip()
    ]

    # 文件路径配置
    BASE_DIR = Path(__file__).parent
    PAPERS_DIR = BASE_DIR / "papers"
    CONCLUSION_FILE = BASE_DIR / "conclusion.md"
    TEMPLATES_DIR = BASE_DIR / "templates"

    # ArXiv搜索配置
    CATEGORIES = ["cs.AI", "cs.LG", "cs.CL"]  # 默认类别
    MAX_PAPERS = 50  # 最大论文数量
    SEARCH_DAYS = 2  # 搜索最近几天的论文

    # AI分析配置
    AI_MODEL = "deepseek-chat"
    API_RETRY_TIMES = 3  # API重试次数
    API_DELAY = 2  # API调用间隔（秒）

    # 输出配置
    OUTPUT_FORMAT = "markdown"  # 输出格式：markdown, html
    EMAIL_FORMAT = "html"  # 邮件格式：html, text

    @classmethod
    def validate(cls) -> bool:
        """验证配置是否完整"""
        required_configs = [
            cls.DEEPSEEK_API_KEY,
            cls.SMTP_SERVER,
            cls.SMTP_USERNAME,
            cls.SMTP_PASSWORD,
            cls.EMAIL_FROM,
        ]

        missing_configs = [config for config in required_configs if not config]

        if missing_configs:
            print(f"缺少必要配置: {missing_configs}")
            return False

        if not cls.EMAIL_TO:
            print("缺少收件人邮箱配置")
            return False

        return True

    @classmethod
    def create_directories(cls):
        """创建必要的目录"""
        cls.PAPERS_DIR.mkdir(exist_ok=True)
        cls.TEMPLATES_DIR.mkdir(exist_ok=True)
