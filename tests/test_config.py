"""
测试配置模块
"""

import os
from unittest.mock import patch

import pytest

from src.config import Config


class TestConfig:
    """配置类测试"""

    def test_config_initialization(self, mock_env_vars):
        """测试配置初始化"""
        config = Config()

        assert config.DEEPSEEK_API_KEY == "test_api_key"
        assert config.SMTP_SERVER == "smtp.test.com"
        assert config.SMTP_PORT == 587
        assert config.EMAIL_TO == ["recipient@test.com"]

    def test_config_validation_success(self, mock_env_vars):
        """测试配置验证成功"""
        config = Config()
        assert config.validate() is True

    def test_config_validation_missing_api_key(self, mock_env_vars):
        """测试缺少API密钥时的验证失败"""
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": ""}):
            config = Config()
            assert config.validate() is False

    def test_config_validation_missing_email_to(self, mock_env_vars):
        """测试缺少收件人邮箱时的验证失败"""
        with patch.dict(os.environ, {"EMAIL_TO": ""}):
            config = Config()
            assert config.validate() is False

    def test_create_directories(self, temp_dir, mock_env_vars):
        """测试目录创建"""
        with patch.object(Config, "BASE_DIR", temp_dir):
            config = Config()
            config.PAPERS_DIR = temp_dir / "papers"
            config.TEMPLATES_DIR = temp_dir / "templates"

            config.create_directories()

            assert config.PAPERS_DIR.exists()
            assert config.TEMPLATES_DIR.exists()

    def test_multiple_email_recipients(self, mock_env_vars):
        """测试多个邮件收件人"""
        with patch.dict(
            os.environ, {"EMAIL_TO": "user1@test.com, user2@test.com, user3@test.com"}
        ):
            config = Config()
            assert len(config.EMAIL_TO) == 3
            assert "user1@test.com" in config.EMAIL_TO
            assert "user2@test.com" in config.EMAIL_TO
            assert "user3@test.com" in config.EMAIL_TO

    def test_default_values(self, mock_env_vars):
        """测试默认值"""
        config = Config()

        assert config.CATEGORIES == ["cs.AI", "cs.LG", "cs.CL"]
        assert config.MAX_PAPERS == 50
        assert config.SEARCH_DAYS == 2
        assert config.AI_MODEL == "deepseek-chat"
        assert config.API_RETRY_TIMES == 3
        assert config.API_DELAY == 2
