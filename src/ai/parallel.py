#!/usr/bin/env python3
"""
并行论文分析器 - 简化版本
使用多线程并行处理论文分析，专门优化DeepSeek分析
"""

import concurrent.futures
import threading
import time
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import os

import arxiv

from src.utils.logger import logger


class ParallelPaperAnalyzer:
    """并行论文分析器 - 专门为DeepSeek优化"""

    def __init__(
        self,
        ai_analyzer,  # DeepSeekAnalyzer实例
        arxiv_client,
        papers_dir: Path,
        max_workers: int = 4, # AI workers
        batch_size: int = 20, # Used by analyze_papers_batch, not directly by analyze_papers_parallel worker count
        max_io_workers_factor: int = 2 # Factor for IO workers relative to AI workers
    ):
        """
        初始化并行分析器

        Args:
            ai_analyzer: DeepSeek分析器实例
            arxiv_client: ArXiv客户端
            papers_dir: PDF存储目录
            max_workers: AI分析任务的最大并行工作线程数
            batch_size: `analyze_papers_batch` 方法中每个子批次的大小
            max_io_workers_factor: I/O工作线程相对于AI工作线程的乘数因子
        """
        self.ai_analyzer = ai_analyzer
        self.arxiv_client = arxiv_client
        self.papers_dir = papers_dir
        self.max_workers = max_workers # For AI tasks
        self.batch_size = batch_size
        
        # Calculate I/O workers
        if self.max_workers <= 0: # auto mode for AI workers (e.g., ThreadPoolExecutor default)
            # If AI workers are auto, set a reasonable default for I/O, e.g. 8, or derive differently if possible
            # For now, let's assume if max_workers is 0, it means use default Python thread pool size for AI (often cores * 5)
            # This part might need more sophisticated handling if max_workers=0 is a common use case for auto-sizing AI pool.
            # For simplicity, let's base it on a sensible default if max_workers is not explicitly positive.
            effective_ai_workers = os.cpu_count() or 4 # Fallback if cpu_count is None
            self.max_io_workers = effective_ai_workers * max_io_workers_factor
        else:
            self.max_io_workers = self.max_workers * max_io_workers_factor
        
        self.io_executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_io_workers)
        logger.info(f"ParallelPaperAnalyzer initialized with {self.max_workers} AI worker(s) and {self.max_io_workers} I/O worker(s).")

        self._lock = threading.Lock()
        self._processed_count = 0
        self._total_count = 0
        self.successful_analyses = 0
        self.failed_analyses = 0
        self.start_time = 0.0
        self.end_time = 0.0

    def _download_pdf_task(self, paper: arxiv.Result) -> Optional[Path]:
        """下载单个PDF的任务，在I/O线程池中运行。"""
        io_thread_id = threading.current_thread().name
        logger.debug(f"[IO Worker {io_thread_id}] Attempting to download PDF for: {paper.title[:40]}...")
        try:
            pdf_path = self.arxiv_client.download_paper(paper, self.papers_dir)
            logger.debug(f"[IO Worker {io_thread_id}] PDF downloaded for '{paper.title[:40]}...' to {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.warning(f"[IO Worker {io_thread_id}] Failed to download PDF for '{paper.title[:40]}...': {e}")
            return None

    def _delete_pdf_task(self, pdf_path: Optional[Path]):
        """删除单个PDF的任务，在I/O线程池中运行。"""
        if not pdf_path:
            return
        io_thread_id = threading.current_thread().name
        logger.debug(f"[IO Worker {io_thread_id}] Attempting to delete PDF: {pdf_path}")
        try:
            self.arxiv_client.delete_pdf(pdf_path)
            logger.debug(f"[IO Worker {io_thread_id}] PDF deleted: {pdf_path}")
        except Exception as e:
            logger.warning(f"[IO Worker {io_thread_id}] Failed to delete PDF {pdf_path}: {e}")

    def _perform_core_ai_analysis(self, paper: arxiv.Result, ai_worker_id: str) -> Optional[Dict[str, Any]]:
        """执行核心AI分析任务，在AI工作线程中运行。"""
        logger.debug(f"[AI Worker {ai_worker_id}] Performing AI analysis for: {paper.title[:40]}...")
        try:
            analysis = self.ai_analyzer.analyze_paper(paper)
            if analysis is None:
                logger.warning(f"[AI Worker {ai_worker_id}] AI analysis returned None for: {paper.title[:40]}...")
                return None
            logger.info(f"[AI Worker {ai_worker_id}] AI analysis successful for: {paper.title[:40]}...")
            return analysis
        except Exception as e:
            logger.error(f"[AI Worker {ai_worker_id}] AI analysis failed for '{paper.title[:40]}...': {e}", exc_info=True)
            return None

    def _process_paper_lifecycle(self, paper: arxiv.Result) -> Optional[Tuple[arxiv.Result, Dict[str, Any]]]:
        """处理单篇论文的完整生命周期：下载、分析、删除。在AI线程池中运行。"""
        ai_worker_id = threading.current_thread().name
        logger.debug(f"[AI Worker {ai_worker_id}] Starting lifecycle for: {paper.title[:40]}...")
        
        pdf_path: Optional[Path] = None
        analysis_result: Optional[Dict[str, Any]] = None

        try:
            # 步骤 1: 下载 PDF (提交到 I/O 线程池并等待结果)
            if self.papers_dir: # Only download if papers_dir is configured
                download_future = self.io_executor.submit(self._download_pdf_task, paper)
                pdf_path = download_future.result() # Wait for download
            else:
                logger.debug(f"[AI Worker {ai_worker_id}] papers_dir not configured, skipping PDF download for {paper.title[:40]}...")

            # 步骤 2: AI分析 (在当前AI工作线程中直接执行)
            analysis_result = self._perform_core_ai_analysis(paper, ai_worker_id)

            if analysis_result is None:
                logger.warning(f"[AI Worker {ai_worker_id}] Analysis failed for '{paper.title[:40]}...', lifecycle terminated for this paper.")
                self.failed_analyses += 1 # Ensure this is thread-safe or updated in main loop
                return None
            
            self.successful_analyses += 1 # Ensure this is thread-safe or updated in main loop
            return (paper, analysis_result)

        except Exception as e:
            logger.error(f"[AI Worker {ai_worker_id}] Unhandled exception in paper lifecycle for '{paper.title[:40]}...': {e}", exc_info=True)
            self.failed_analyses += 1 # Ensure this is thread-safe or updated in main loop
            return None
        finally:
            # 步骤 3: 删除 PDF (提交到 I/O 线程池，发射后不管)
            if pdf_path: # Only attempt to delete if a path was obtained
                self.io_executor.submit(self._delete_pdf_task, pdf_path)
            logger.debug(f"[AI Worker {ai_worker_id}] Finished lifecycle for: {paper.title[:40]}...")

    def analyze_papers_parallel(
        self, papers: List[arxiv.Result]
    ) -> List[Tuple[arxiv.Result, Dict[str, Any]]]: # Return type changed to reflect analysis dict
        """
        并行分析论文列表
        Args:
            papers: 论文列表
        Returns:
            (论文, 分析结果字典) 的列表
        """
        if not papers:
            return []

        self._total_count = len(papers)
        self._processed_count = 0
        self.successful_analyses = 0 # Reset for this run
        self.failed_analyses = 0     # Reset for this run
        
        logger.info(f"Starting parallel analysis of {self._total_count} papers using {self.max_workers} AI worker(s) and {self.max_io_workers} I/O worker(s).")
        
        self.start_time = time.time()
        results = []

        # AI分析线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as ai_executor:
            future_to_paper = {
                ai_executor.submit(self._process_paper_lifecycle, paper): paper
                for paper in papers
            }

            for future in concurrent.futures.as_completed(future_to_paper):
                paper_obj = future_to_paper[future]
                try:
                    result_tuple = future.result()
                    if result_tuple:
                        results.append(result_tuple)
                        # successful_analyses is incremented in _process_paper_lifecycle
                    # else: failed_analyses is incremented in _process_paper_lifecycle
                    
                except Exception as e:
                    logger.error(f"[Main AI Loop] Error collecting result for '{paper_obj.title[:40]}...': {e}", exc_info=True)
                    # This specific paper failed at the future.result() stage, likely an unhandled exception from _process_paper_lifecycle
                    # We need a way to count this as a failure if not already counted.
                    # For simplicity, assume _process_paper_lifecycle handles its own failure counting via self.failed_analyses
                    # However, if future.result() itself raises, it means the task submitted to ai_executor had an issue not caught by the try-except within _process_paper_lifecycle.
                    # This shouldn't happen if _process_paper_lifecycle is robust. Let's assume for now it is.
                    pass # Error already logged by _process_paper_lifecycle if it returned None or raised internally.
                
                with self._lock:
                    self._processed_count += 1
                    progress = (self._processed_count / self._total_count) * 100 if self._total_count > 0 else 0
                    logger.info(f"Progress: {self._processed_count}/{self._total_count} ({progress:.1f}%) paper lifecycles completed (Current: '{paper_obj.title[:40]}...').")

        self.end_time = time.time()
        duration = self.end_time - self.start_time
        avg_time_per_paper = duration / self._total_count if self._total_count > 0 else 0
        
        logger.info(f"Parallel analysis finished in {duration:.2f}s.")
        logger.info(f"Successfully analyzed: {self.successful_analyses}/{self._total_count} papers.")
        if self.failed_analyses > 0:
            logger.warning(f"Failed to analyze: {self.failed_analyses}/{self._total_count} papers.")
        logger.info(f"Average time per paper: {avg_time_per_paper:.2f}s.")
        
        return results

    def shutdown_io_executor(self):
        """关闭I/O线程池。应该在所有分析完成后调用。"""
        logger.info("Shutting down I/O executor...")
        self.io_executor.shutdown(wait=True)
        logger.info("I/O executor shut down successfully.")

    def analyze_papers_batch(
        self, papers: List[arxiv.Result]
    ) -> List[Tuple[arxiv.Result, Dict[str, Any]]]: # Return type changed
        """
        批量分析论文（适合大量论文）
        Args:
            papers: 论文列表
        Returns:
            (论文, 分析结果字典) 的列表
        """
        if not papers:
            return []

        logger.info(f"Starting batch analysis of {len(papers)} papers, with sub-batch size: {self.batch_size}")
        all_results = []
        for i in range(0, len(papers), self.batch_size):
            batch = papers[i:i + self.batch_size]
            batch_num = i // self.batch_size + 1
            total_batches = (len(papers) + self.batch_size - 1) // self.batch_size
            logger.info(f"Processing sub-batch {batch_num}/{total_batches} ({len(batch)} papers) using parallel analyzer.")
            
            batch_results = self.analyze_papers_parallel(batch) # This will use the class's max_workers for AI and IO
            all_results.extend(batch_results)
            
            if i + self.batch_size < len(papers):
                logger.info("Resting for 2 seconds between sub-batches...")
                time.sleep(2)
        return all_results

    @staticmethod
    def calculate_optimal_workers(paper_count: int, api_delay: int = 2) -> int:
        """根据论文数量和API延迟计算最优AI工作线程数 (I/O workers will be derived from this)"""
        # This calculation remains for AI workers. I/O workers are derived via factor.
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
        duration = self.end_time - self.start_time if self.end_time > self.start_time else 0
        avg_time = duration / self._total_count if self._total_count > 0 else 0
        return {
            "max_ai_workers": self.max_workers,
            "max_io_workers": self.max_io_workers,
            "batch_size_for_analyze_papers_batch": self.batch_size, 
            "total_papers_submitted_to_parallel_run": self._total_count,
            "papers_lifecycle_completed_in_parallel_run": self._processed_count,
            "successful_analyses_in_parallel_run": self.successful_analyses,
            "failed_analyses_in_parallel_run": self.failed_analyses,
            "total_duration_seconds_parallel_run": round(duration, 2),
            "avg_time_per_paper_seconds_parallel_run": round(avg_time, 2)
        } 