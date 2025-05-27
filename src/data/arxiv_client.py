#!/usr/bin/env python3
"""
ArXiv客户端模块
负责论文搜索和下载功能，支持AI质量筛选
"""

import datetime
import asyncio
from pathlib import Path
from typing import List, Optional, Tuple
import re

import arxiv

from utils.logger import logger


class PaperQualityFilter:
    """论文质量评估筛选器"""
    
    def __init__(self, ai_analyzer=None):
        """
        初始化质量筛选器
        
        Args:
            ai_analyzer: AI分析器实例，用于质量评估
        """
        self.ai_analyzer = ai_analyzer
        
        # 高质量指标关键词
        self.quality_keywords = {
            'method_innovation': [
                'novel', 'new', 'innovative', 'breakthrough', 'first', 
                'pioneer', 'introduce', 'propose', 'advance', 'improve'
            ],
            'performance': [
                'state-of-the-art', 'sota', 'outperform', 'achieve', 
                'surpass', 'best', 'superior', 'excellent', 'significant'
            ],
            'evaluation': [
                'benchmark', 'evaluation', 'experiment', 'ablation',
                'comprehensive', 'extensive', 'thorough', 'rigorous'
            ],
            'impact': [
                'practical', 'real-world', 'application', 'deployment',
                'scale', 'efficient', 'robust', 'generalizable'
            ]
        }
        
        # 低质量指标
        self.low_quality_indicators = [
            'survey', 'review', 'tutorial', 'position paper',
            'work in progress', 'preliminary', 'draft'
        ]
    
    def calculate_paper_score(self, paper: arxiv.Result) -> float:
        """
        计算论文质量分数
        
        Args:
            paper: 论文对象
            
        Returns:
            质量分数 (0-100)
        """
        score = 0.0
        title_lower = paper.title.lower()
        summary_lower = paper.summary.lower()
        text = f"{title_lower} {summary_lower}"
        
        # 1. 创新性评估 (30分)
        innovation_score = 0
        for keyword in self.quality_keywords['method_innovation']:
            if keyword in text:
                innovation_score += 3
        score += min(innovation_score, 30)
        
        # 2. 性能表现评估 (25分)
        performance_score = 0
        for keyword in self.quality_keywords['performance']:
            if keyword in text:
                performance_score += 5
        score += min(performance_score, 25)
        
        # 3. 评估完整性 (20分)
        evaluation_score = 0
        for keyword in self.quality_keywords['evaluation']:
            if keyword in text:
                evaluation_score += 4
        score += min(evaluation_score, 20)
        
        # 4. 实用性影响 (15分)
        impact_score = 0
        for keyword in self.quality_keywords['impact']:
            if keyword in text:
                impact_score += 3
        score += min(impact_score, 15)
        
        # 5. 作者声誉 (10分) - 基于作者数量和机构
        author_score = min(len(paper.authors) * 2, 10)
        score += author_score
        
        # 6. 负面指标扣分
        for indicator in self.low_quality_indicators:
            if indicator in text:
                score -= 10
        
        # 7. 论文长度指标（摘要长度作为参考）
        if len(paper.summary) > 800:  # 详细摘要通常质量较高
            score += 5
        elif len(paper.summary) < 300:  # 过短摘要可能质量较低
            score -= 5
        
        return max(0, min(score, 100))
    
    async def ai_quality_assessment(self, paper: arxiv.Result) -> Tuple[float, str]:
        """
        使用AI进行深度质量评估
        
        Args:
            paper: 论文对象
            
        Returns:
            (AI评分, 评估理由)
        """
        if not self.ai_analyzer:
            return 50.0, "未配置AI分析器"
        
        try:
            # 构建质量评估提示词
            assessment_prompt = f"""
请评估这篇学术论文的质量和重要性，从以下几个维度进行评分：

**论文信息：**
标题: {paper.title}
摘要: {paper.summary[:500]}...
作者: {', '.join([author.name for author in paper.authors[:5]])}
主要类别: {paper.primary_category}

**评估维度：**
1. 创新性 (20分)：方法或思路是否新颖
2. 技术质量 (20分)：技术方案是否严谨可靠
3. 实验评估 (20分)：实验设计是否完整充分
4. 实用价值 (20分)：是否有实际应用价值
5. 学术影响 (20分)：是否可能产生学术影响

请给出：
1. 总分（0-100分）
2. 简要评估理由（50字以内）

格式：分数|理由
例如：85|创新的多模态方法，实验全面，实用性强
"""
            
            # 调用AI分析器进行评估
            if hasattr(self.ai_analyzer, 'analyze_paper_async'):
                result = await self.ai_analyzer.analyze_paper_async(paper)
                ai_response = result.get('analysis', '')
            else:
                ai_response = self.ai_analyzer.analyze_paper(paper)
            
            # 解析AI评估结果
            if '|' in ai_response[:100]:  # 查看前100字符
                parts = ai_response.split('|', 1)
                try:
                    ai_score = float(re.findall(r'\d+', parts[0])[0])
                    ai_reason = parts[1].strip()[:100]  # 限制理由长度
                    return ai_score, ai_reason
                except (IndexError, ValueError):
                    pass
            
            # 如果解析失败，使用默认评分
            return 70.0, "AI评估完成但格式解析失败"
            
        except Exception as e:
            logger.warning(f"AI质量评估失败: {e}")
            return 50.0, f"AI评估失败: {str(e)[:50]}"


class ArxivClient:
    """ArXiv客户端类"""

    def __init__(
        self, categories: List[str], max_papers: int = 50, search_days: int = 2,
        enable_quality_filter: bool = False, quality_threshold: float = 60.0,
        ai_analyzer=None
    ):
        """
        初始化ArXiv客户端

        Args:
            categories: 论文类别列表
            max_papers: 最大论文数量
            search_days: 搜索最近几天的论文
            enable_quality_filter: 是否启用质量筛选
            quality_threshold: 质量筛选阈值
            ai_analyzer: AI分析器实例
        """
        self.categories = categories
        self.max_papers = max_papers
        self.search_days = search_days
        self.enable_quality_filter = enable_quality_filter
        self.quality_threshold = quality_threshold
        
        # 初始化质量筛选器
        self.quality_filter = PaperQualityFilter(ai_analyzer) if enable_quality_filter else None

    def get_recent_papers(self) -> List[arxiv.Result]:
        """
        获取最近几天内发布的指定类别的论文

        Returns:
            论文列表
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
        
        # 如果启用质量筛选，获取更多论文用于筛选
        search_limit = self.max_papers * 3 if self.enable_quality_filter else self.max_papers

        # 搜索ArXiv
        search = arxiv.Search(
            query=query,
            max_results=search_limit,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        results = list(search.results())
        logger.info(f"找到{len(results)}篇符合条件的论文")
        
        # 应用质量筛选
        if self.enable_quality_filter and self.quality_filter:
            results = self._apply_quality_filter(results)
        
        # 限制最终返回数量
        return results[:self.max_papers]
    
    def _apply_quality_filter(self, papers: List[arxiv.Result]) -> List[arxiv.Result]:
        """
        应用质量筛选
        
        Args:
            papers: 原始论文列表
            
        Returns:
            筛选后的论文列表
        """
        logger.info(f"开始质量筛选，原始论文数量: {len(papers)}")
        
        # 计算每篇论文的质量分数
        papers_with_scores = []
        for paper in papers:
            score = self.quality_filter.calculate_paper_score(paper)
            papers_with_scores.append((paper, score))
            logger.debug(f"论文质量评分: {score:.1f} - {paper.title[:50]}...")
        
        # 按分数排序并筛选
        papers_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 应用阈值筛选
        filtered_papers = [
            paper for paper, score in papers_with_scores 
            if score >= self.quality_threshold
        ]
        
        # 记录筛选结果
        logger.info(f"质量筛选完成:")
        logger.info(f"  - 筛选前: {len(papers)} 篇")
        logger.info(f"  - 质量阈值: {self.quality_threshold}")
        logger.info(f"  - 筛选后: {len(filtered_papers)} 篇")
        
        if filtered_papers and len(papers_with_scores) > 0:
            top_scores = [score for _, score in papers_with_scores[:5]]
            logger.info(f"  - 前5名分数: {top_scores}")
        
        return filtered_papers

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
