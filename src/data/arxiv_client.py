#!/usr/bin/env python3
"""
ArXiv客户端模块
负责论文搜索和下载功能，不再进行质量筛选，改为在AI分析阶段进行质量评估
"""

import datetime
from pathlib import Path
from typing import List, Optional

import arxiv

from utils.logger import logger


class ArxivClient:
    """ArXiv客户端类"""

    def __init__(self, categories: List[str], max_papers: int = 50, search_days: int = 2):
        """
        初始化ArXiv客户端

        Args:
            categories: 论文类别列表
            max_papers: 最大论文数量
            search_days: 搜索最近几天的论文
        """
        self.categories = categories
        self.max_papers = max_papers
        self.search_days = search_days

    def get_recent_papers(self) -> List[arxiv.Result]:
        """
        获取最近几天内发布的指定类别的论文

        Returns:
            论文列表，按发布时间倒序排列
        """
        # 计算日期范围
        today = datetime.datetime.now()
        start_date = today - datetime.timedelta(days=self.search_days)

        # 格式化ArXiv查询的日期
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = today.strftime("%Y%m%d")

        # 创建查询字符串
        category_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        date_range = f"submittedDate:[{start_date_str}000000 TO {end_date_str}235959]"
        query = f"({category_query}) AND {date_range}"

        logger.info(f"正在搜索论文，查询条件: {query}")

        # 搜索ArXiv
        search = arxiv.Search(
            query=query,
            max_results=self.max_papers,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        results = list(search.results())
        logger.info(f"找到{len(results)}篇符合条件的论文，将进行AI质量评估")
        
        return results

    def download_paper(self, paper: arxiv.Result, output_dir: Path) -> Optional[Path]:
        """
        下载论文PDF到指定目录

        Args:
            paper: 论文对象
            output_dir: 输出目录

        Returns:
            PDF文件路径，下载失败返回None
        """
        pdf_path = output_dir / f"{paper.get_short_id().replace('/', '_')}.pdf"

        # 如果已下载则跳过
        if pdf_path.exists():
            logger.info(f"论文已下载: {pdf_path}")
            return pdf_path

        try:
            logger.info(f"正在下载: {paper.title}")
            paper.download_pdf(filename=str(pdf_path))
            logger.info(f"已下载到 {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.error(f"下载论文失败 {paper.title}: {str(e)}")
            return None

    def delete_pdf(self, pdf_path: Path) -> None:
        """
        删除PDF文件

        Args:
            pdf_path: PDF文件路径
        """
        try:
            if pdf_path and pdf_path.exists():
                pdf_path.unlink()
                logger.info(f"已删除PDF文件: {pdf_path}")
            else:
                logger.info(f"PDF文件不存在，无需删除: {pdf_path}")
        except Exception as e:
            logger.error(f"删除PDF文件失败 {pdf_path}: {str(e)}")

    def filter_papers_by_keywords(
        self, papers: List[arxiv.Result], keywords: List[str] = None
    ) -> List[arxiv.Result]:
        """
        根据关键词过滤论文

        Args:
            papers: 论文列表
            keywords: 关键词列表

        Returns:
            过滤后的论文列表
        """
        if not keywords:
            return papers

        filtered_papers = []
        keywords_lower = [kw.lower() for kw in keywords]

        for paper in papers:
            title_lower = paper.title.lower()
            summary_lower = paper.summary.lower()

            # 检查标题或摘要中是否包含关键词
            if any(kw in title_lower or kw in summary_lower for kw in keywords_lower):
                filtered_papers.append(paper)

        logger.info(f"关键词过滤后剩余{len(filtered_papers)}篇论文")
        return filtered_papers 