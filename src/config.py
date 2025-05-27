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

    def __init__(self):
        """初始化配置，从环境变量读取"""
        # API配置
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        self.DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

        # 邮件配置
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT", "587").strip()
        self.SMTP_PORT = int(smtp_port) if smtp_port else 587
        self.SMTP_USERNAME = os.getenv("SMTP_USERNAME")
        self.SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        self.EMAIL_FROM = os.getenv("EMAIL_FROM")
        self.EMAIL_TO = [
            email.strip() for email in os.getenv("EMAIL_TO", "").split(",") if email.strip()
        ]

        # 文件路径配置
        self.BASE_DIR = Path(__file__).parent
        self.PAPERS_DIR = self.BASE_DIR / "papers"
        self.CONCLUSION_FILE = self.BASE_DIR / "conclusion.md"
        self.TEMPLATES_DIR = self.BASE_DIR / "templates"

        # ArXiv搜索配置
        self.CATEGORIES = ["cs.AI", "cs.LG", "cs.CL"]  # 默认类别
        self.MAX_PAPERS = 50  # 最大论文数量
        self.SEARCH_DAYS = 2  # 搜索最近几天的论文

        # AI分析配置
        self.AI_MODEL = "deepseek-chat"
        self.API_RETRY_TIMES = 3  # API重试次数
        self.API_DELAY = 2  # API调用间隔（秒）

        # 输出配置
        self.OUTPUT_FORMAT = "markdown"  # 输出格式：markdown, html
        self.EMAIL_FORMAT = "html"  # 邮件格式：html, text

    def validate(self) -> bool:
        """验证配置是否完整"""
        required_configs = [
            self.DEEPSEEK_API_KEY,
            self.SMTP_SERVER,
            self.SMTP_USERNAME,
            self.SMTP_PASSWORD,
            self.EMAIL_FROM,
        ]

        missing_configs = [config for config in required_configs if not config]

        if missing_configs:
            print(f"缺少必要配置: {missing_configs}")
            return False

        if not self.EMAIL_TO:
            print("缺少收件人邮箱配置")
            return False

        return True

    def create_directories(self):
        """创建必要的目录"""
        self.PAPERS_DIR.mkdir(exist_ok=True)
        self.TEMPLATES_DIR.mkdir(exist_ok=True)
