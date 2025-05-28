#!/usr/bin/env python3
"""
并行论文分析器 - 简化版本
使用多线程并行处理论文分析，专门优化DeepSeek分析
"""

import concurrent.futures
import threading
import time
from typing import List, Tuple, Optional

import arxiv

from utils.logger import logger


class ParallelPaperAnalyzer:
    """并行论文分析器 - 专门为DeepSeek优化"""

    def __init__(
        self,
        ai_analyzer,  # DeepSeekAnalyzer实例
        arxiv_client,
        papers_dir,
        max_workers: int = 5,
        batch_size: int = 10
    ):
        """
        初始化并行分析器

        Args:
            ai_analyzer: DeepSeek分析器实例
            arxiv_client: ArXiv客户端
            papers_dir: PDF存储目录
            max_workers: 最大并行工作线程数
            batch_size: 批处理大小
        """
        self.ai_analyzer = ai_analyzer
        self.arxiv_client = arxiv_client
        self.papers_dir = papers_dir
        self.max_workers = max_workers
        self.batch_size = batch_size
        
        # 线程安全的计数器
        self._lock = threading.Lock()
        self._processed_count = 0
        self._total_count = 0

    def analyze_papers_parallel(
        self, papers: List[arxiv.Result]
    ) -> List[Tuple[arxiv.Result, str]]:
        """
        并行分析论文列表

        Args:
            papers: 论文列表

        Returns:
            (论文, 分析结果) 的列表
        """
        if not papers:
            return []

        self._total_count = len(papers)
        self._processed_count = 0
        
        logger.info(f"开始并行分析 {len(papers)} 篇论文，使用 {self.max_workers} 个工作线程")
        
        start_time = time.time()
        results = []

        # 使用ThreadPoolExecutor进行并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_paper = {
                executor.submit(self._analyze_single_paper, paper): paper
                for paper in papers
            }

            # 收集结果
            for future in concurrent.futures.as_completed(future_to_paper):
                paper = future_to_paper[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                    
                    # 更新进度
                    with self._lock:
                        self._processed_count += 1
                        progress = (self._processed_count / self._total_count) * 100
                        logger.info(f"进度: {self._processed_count}/{self._total_count} ({progress:.1f}%)")
                        
                except Exception as e:
                    logger.error(f"分析论文失败 {paper.title}: {e}")

        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"并行分析完成！")
        logger.info(f"总时间: {duration:.2f}秒")
        logger.info(f"成功分析: {len(results)}/{len(papers)} 篇论文")
        logger.info(f"平均每篇: {duration/len(papers):.2f}秒")
        
        return results

    def _analyze_single_paper(
        self, paper: arxiv.Result
    ) -> Optional[Tuple[arxiv.Result, str]]:
        """
        分析单篇论文（线程安全）

        Args:
            paper: 论文对象

        Returns:
            (论文, 分析结果) 或 None（如果失败）
        """
        thread_id = threading.current_thread().name
        logger.debug(f"[{thread_id}] 开始分析: {paper.title}")

        try:
            # 下载论文（如果需要）
            pdf_path = None
            try:
                pdf_path = self.arxiv_client.download_paper(paper, self.papers_dir)
            except Exception as e:
                logger.warning(f"[{thread_id}] 下载PDF失败，继续分析: {e}")

            # 分析论文
            analysis = self.ai_analyzer.analyze_paper(paper)
            
            # 检查AI分析是否成功
            if analysis is None:
                logger.warning(f"[{thread_id}] AI分析失败，所有模型都无法处理: {paper.title}")
                return None
            
            # 清理PDF文件
            if pdf_path:
                try:
                    self.arxiv_client.delete_pdf(pdf_path)
                except Exception as e:
                    logger.warning(f"[{thread_id}] 删除PDF失败: {e}")

            logger.debug(f"[{thread_id}] 分析完成: {paper.title}")
            return (paper, analysis)

        except Exception as e:
            logger.error(f"[{thread_id}] 分析论文失败 {paper.title}: {e}")
            return None

    def analyze_papers_batch(
        self, papers: List[arxiv.Result]
    ) -> List[Tuple[arxiv.Result, str]]:
        """
        批量分析论文（适合大量论文）

        Args:
            papers: 论文列表

        Returns:
            (论文, 分析结果) 的列表
        """
        if not papers:
            return []

        logger.info(f"开始批量分析 {len(papers)} 篇论文，批大小: {self.batch_size}")
        
        all_results = []
        
        # 分批处理
        for i in range(0, len(papers), self.batch_size):
            batch = papers[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            total_batches = (len(papers) + self.batch_size - 1) // self.batch_size
            
            logger.info(f"处理批次 {batch_num}/{total_batches} ({len(batch)} 篇论文)")
            
            batch_results = self.analyze_papers_parallel(batch)
            all_results.extend(batch_results)
            
            # 批次间短暂休息，避免API限制
            if i + self.batch_size < len(papers):
                logger.info("批次间休息 2 秒...")
                time.sleep(2)

        return all_results

    @staticmethod
    def calculate_optimal_workers(paper_count: int, api_delay: int = 2) -> int:
        """
        根据论文数量和API延迟计算最优工作线程数

        Args:
            paper_count: 论文数量
            api_delay: API调用间隔（秒）

        Returns:
            推荐的工作线程数
        """
        # 基于经验的启发式算法
        if paper_count <= 5:
            return min(paper_count, 3)
        elif paper_count <= 20:
            return min(paper_count // 2, 5)
        elif paper_count <= 50:
            return min(paper_count // 5, 8)
        else:
            return min(paper_count // 10, 10)

    def get_performance_stats(self) -> dict:
        """获取性能统计信息"""
        return {
            "max_workers": self.max_workers,
            "batch_size": self.batch_size,
            "processed_count": self._processed_count,
            "total_count": self._total_count
        } 