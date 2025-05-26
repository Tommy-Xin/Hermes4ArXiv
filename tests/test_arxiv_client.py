"""
测试 ArXiv 客户端模块
"""

from unittest.mock import Mock, patch

import arxiv
import pytest

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from arxiv_client import ArxivClient


class TestArxivClient:
    """ArXiv客户端测试"""

    def test_initialization(self):
        """测试客户端初始化"""
        categories = ["cs.AI", "cs.LG"]
        max_papers = 10
        search_days = 3

        client = ArxivClient(categories, max_papers, search_days)

        assert client.categories == categories
        assert client.max_papers == max_papers
        assert client.search_days == search_days

    @patch("arxiv_client.arxiv.Search")
    def test_get_recent_papers(self, mock_search, mock_papers):
        """测试获取最近论文"""
        # 设置模拟
        mock_search_instance = Mock()
        mock_search.return_value = mock_search_instance
        mock_search_instance.results.return_value = iter(mock_papers)

        client = ArxivClient(["cs.AI"], max_papers=5, search_days=2)
        papers = client.get_recent_papers()

        assert len(papers) == 3
        assert papers[0].title == "Test Paper 1: Advanced Testing Methods"

        # 验证搜索参数
        mock_search.assert_called_once()

    def test_download_paper_success(self, mock_paper, temp_dir):
        """测试成功下载论文"""
        client = ArxivClient(["cs.AI"])

        # 模拟下载成功
        with patch.object(mock_paper, "download_pdf") as mock_download:
            pdf_path = client.download_paper(mock_paper, temp_dir)

            expected_path = temp_dir / "2401.0001.pdf"
            assert pdf_path == expected_path
            mock_download.assert_called_once()

    def test_delete_pdf_success(self, temp_dir):
        """测试成功删除PDF"""
        client = ArxivClient(["cs.AI"])

        # 创建测试文件
        test_file = temp_dir / "test.pdf"
        test_file.touch()
        assert test_file.exists()

        client.delete_pdf(test_file)
        assert not test_file.exists()

    def test_filter_papers_by_keywords(self, mock_papers):
        """测试根据关键词过滤论文"""
        client = ArxivClient(["cs.AI"])

        # 设置论文内容
        mock_papers[0].title = "Machine Learning for Computer Vision"
        mock_papers[0].summary = "This paper discusses deep learning methods."

        # 测试关键词过滤
        keywords = ["machine learning"]
        filtered_papers = client.filter_papers_by_keywords(mock_papers, keywords)

        assert len(filtered_papers) == 1
