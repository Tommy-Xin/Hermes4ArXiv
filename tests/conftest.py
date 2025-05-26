"""
pytest 配置文件和共享夹具
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import arxiv
import pytest

from src.config import Config


@pytest.fixture
def temp_dir():
    """创建临时目录夹具"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_config(temp_dir):
    """创建模拟配置夹具"""
    with patch.object(Config, "BASE_DIR", temp_dir):
        config = Config()
        config.PAPERS_DIR = temp_dir / "papers"
        config.CONCLUSION_FILE = temp_dir / "conclusion.md"
        config.TEMPLATES_DIR = temp_dir / "templates"

        # 创建必要目录
        config.create_directories()

        # 创建模板文件
        template_content = """
        <html>
        <body>
            <h1>Test Template</h1>
            <p>Papers: {{ paper_count }}</p>
        </body>
        </html>
        """
        (config.TEMPLATES_DIR / "email_template.html").write_text(template_content)

        yield config


@pytest.fixture
def mock_paper():
    """创建模拟论文对象"""
    paper = Mock(spec=arxiv.Result)
    paper.title = "Test Paper: A Novel Approach to Testing"
    paper.authors = [Mock(name="John Doe"), Mock(name="Jane Smith")]
    paper.categories = ["cs.AI", "cs.LG"]
    paper.published = Mock()
    paper.published.strftime.return_value = "2024-01-01"
    paper.published.date.return_value = Mock()
    paper.entry_id = "https://arxiv.org/abs/2401.0001"
    paper.summary = "This is a test paper summary for testing purposes."
    paper.get_short_id.return_value = "2401.0001"
    return paper


@pytest.fixture
def mock_papers(mock_paper):
    """创建多个模拟论文"""
    papers = []
    for i in range(3):
        paper = Mock(spec=arxiv.Result)
        paper.title = f"Test Paper {i+1}: Advanced Testing Methods"
        paper.authors = [Mock(name=f"Author {i+1}")]
        paper.categories = ["cs.AI"]
        paper.published = Mock()
        paper.published.strftime.return_value = f"2024-01-0{i+1}"
        paper.published.date.return_value = Mock()
        paper.entry_id = f"https://arxiv.org/abs/2401.000{i+1}"
        paper.summary = f"This is test paper {i+1} summary."
        paper.get_short_id.return_value = f"2401.000{i+1}"
        papers.append(paper)
    return papers


@pytest.fixture
def mock_analysis():
    """创建模拟分析结果"""
    return """
    **核心贡献**: 这是一个测试分析结果。

    **技术方法**: 使用了先进的测试方法。

    **实验验证**: 在测试数据集上进行了验证。

    **影响意义**: 对测试领域有重要影响。

    **局限展望**: 未来可以进一步改进测试方法。
    """


@pytest.fixture
def mock_env_vars():
    """模拟环境变量"""
    env_vars = {
        "DEEPSEEK_API_KEY": "test_api_key",
        "SMTP_SERVER": "smtp.test.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "test@test.com",
        "SMTP_PASSWORD": "test_password",
        "EMAIL_FROM": "test@test.com",
        "EMAIL_TO": "recipient@test.com",
    }

    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture(autouse=True)
def reset_config():
    """每个测试后重置配置"""
    yield
    # 清理可能的配置缓存
    if hasattr(Config, "_instance"):
        delattr(Config, "_instance")
