#!/usr/bin/env python3
"""
输出格式化模块
支持多种输出格式和美化显示
"""

import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import arxiv
from jinja2 import Environment, FileSystemLoader, Template

from utils.logger import logger


class OutputFormatter:
    """输出格式化器"""

    def __init__(self, templates_dir: Path):
        """
        初始化格式化器

        Args:
            templates_dir: 模板目录路径
        """
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(str(templates_dir)))

    def format_markdown(
        self, papers_analyses: List[Tuple[arxiv.Result, str]], title: str = None
    ) -> str:
        """
        格式化为Markdown格式

        Args:
            papers_analyses: 论文分析结果列表
            title: 标题

        Returns:
            Markdown格式的内容
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        if title is None:
            title = f"ArXiv论文分析报告 ({today})"

        content = f"# {title}\n\n"
        content += f"**生成时间**: {today}\n"
        content += f"**论文数量**: {len(papers_analyses)}\n\n"

        for i, (paper, analysis) in enumerate(papers_analyses, 1):
            author_names = [author.name for author in paper.authors]

            content += f"## {i}. {paper.title}\n\n"
            content += f"**👥 作者**: {', '.join(author_names)}\n\n"
            content += f"**🏷️ 类别**: {', '.join(paper.categories)}\n\n"
            content += f"**📅 发布日期**: {paper.published.strftime('%Y-%m-%d')}\n\n"
            content += f"**🔗 链接**: [{paper.entry_id}]({paper.entry_id})\n\n"
            content += f"### 📝 分析结果\n\n{analysis}\n\n"
            content += "---\n\n"

        return content

    def format_html_email(self, papers_analyses: List[Tuple[arxiv.Result, str]]) -> str:
        """
        格式化为HTML邮件格式

        Args:
            papers_analyses: 论文分析结果列表

        Returns:
            HTML格式的邮件内容
        """
        try:
            template = self.env.get_template("email_template.html")
        except Exception as e:
            logger.error(f"加载邮件模板失败: {e}")
            return self._fallback_html_format(papers_analyses)

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        # 准备模板数据
        papers_data = []
        categories_set = set()

        for paper, analysis in papers_analyses:
            author_names = [author.name for author in paper.authors]
            categories_set.update(paper.categories)

            # 处理分析内容，转换为HTML格式
            analysis_html = self._convert_analysis_to_html(analysis)

            papers_data.append(
                {
                    "title": paper.title,
                    "authors": ", ".join(author_names),
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "categories": paper.categories,
                    "url": paper.entry_id,
                    "analysis": analysis_html,
                }
            )

        template_data = {
            "date": today,
            "paper_count": len(papers_analyses),
            "categories": ", ".join(sorted(categories_set)),
            "papers": papers_data,
        }

        return template.render(**template_data)

    def _convert_analysis_to_html(self, analysis: str) -> str:
        """
        将分析内容转换为HTML格式

        Args:
            analysis: 分析内容

        Returns:
            HTML格式的分析内容
        """
        # 简单的Markdown到HTML转换
        html = analysis

        # 处理粗体
        html = html.replace("**", "<strong>").replace("**", "</strong>")

        # 处理段落
        paragraphs = html.split("\n\n")
        html_paragraphs = []

        for para in paragraphs:
            if para.strip():
                # 检查是否是标题（以数字开头）
                if para.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                    html_paragraphs.append(
                        f'<div class="analysis-section"><h4>{para.strip()}</h4></div>'
                    )
                else:
                    html_paragraphs.append(f"<p>{para.strip()}</p>")

        return "\n".join(html_paragraphs)

    def _fallback_html_format(
        self, papers_analyses: List[Tuple[arxiv.Result, str]]
    ) -> str:
        """
        备用HTML格式化方法

        Args:
            papers_analyses: 论文分析结果列表

        Returns:
            简单的HTML格式内容
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ArXiv论文分析报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .paper {{ border: 1px solid #ddd; margin-bottom: 20px; padding: 20px; border-radius: 8px; }}
                .paper-title {{ color: #2c3e50; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
                .paper-meta {{ color: #666; margin-bottom: 15px; }}
                .analysis {{ margin-top: 15px; }}
            </style>
        </head>
        <body>
            <h1>📚 ArXiv论文分析报告</h1>
            <p><strong>生成时间</strong>: {today}</p>
            <p><strong>论文数量</strong>: {len(papers_analyses)}</p>
        """

        for paper, analysis in papers_analyses:
            author_names = [author.name for author in paper.authors]

            html += f"""
            <div class="paper">
                <div class="paper-title">{paper.title}</div>
                <div class="paper-meta">
                    <strong>作者</strong>: {', '.join(author_names)}<br>
                    <strong>类别</strong>: {', '.join(paper.categories)}<br>
                    <strong>发布日期</strong>: {paper.published.strftime('%Y-%m-%d')}<br>
                    <strong>链接</strong>: <a href="{paper.entry_id}">{paper.entry_id}</a>
                </div>
                <div class="analysis">{analysis.replace(chr(10), '<br>')}</div>
            </div>
            """

        html += """
        </body>
        </html>
        """

        return html

    def save_to_file(self, content: str, file_path: Path, mode: str = "a") -> None:
        """
        保存内容到文件

        Args:
            content: 要保存的内容
            file_path: 文件路径
            mode: 文件打开模式
        """
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(content)
            logger.info(f"内容已保存到 {file_path}")
        except Exception as e:
            logger.error(f"保存文件失败 {file_path}: {e}")

    def create_summary_stats(
        self, papers_analyses: List[Tuple[arxiv.Result, str]]
    ) -> Dict[str, Any]:
        """
        创建统计摘要

        Args:
            papers_analyses: 论文分析结果列表

        Returns:
            统计信息字典
        """
        if not papers_analyses:
            return {}

        categories = {}
        authors = set()
        dates = []

        for paper, _ in papers_analyses:
            # 统计类别
            for cat in paper.categories:
                categories[cat] = categories.get(cat, 0) + 1

            # 统计作者
            for author in paper.authors:
                authors.add(author.name)

            # 统计日期
            dates.append(paper.published.date())

        return {
            "total_papers": len(papers_analyses),
            "categories": categories,
            "unique_authors": len(authors),
            "date_range": {
                "earliest": min(dates) if dates else None,
                "latest": max(dates) if dates else None,
            },
        }
