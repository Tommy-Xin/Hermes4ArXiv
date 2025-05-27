#!/usr/bin/env python3
"""
并行分析性能基准测试
比较串行和并行分析的性能差异，帮助优化GitHub Actions运行时间
"""

import sys
import time
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_analyzer import AnalyzerFactory
from arxiv_client import ArxivClient
from config import Config
from parallel_analyzer import ParallelPaperAnalyzer
from utils.logger import logger


class PerformanceBenchmark:
    """性能基准测试类"""

    def __init__(self, test_paper_count: int = 10):
        """
        初始化基准测试

        Args:
            test_paper_count: 测试论文数量
        """
        self.test_paper_count = test_paper_count
        self.config = Config()
        
        # 初始化组件
        self.arxiv_client = ArxivClient(
            categories=["cs.AI"],  # 只测试AI类别
            max_papers=test_paper_count,
            search_days=7  # 扩大搜索范围确保有足够论文
        )
        
        self.ai_analyzer = AnalyzerFactory.create_analyzer(
            "deepseek",
            api_key=self.config.DEEPSEEK_API_KEY,
            model=self.config.AI_MODEL,
            retry_times=1,  # 减少重试次数加快测试
            delay=1  # 减少延迟加快测试
        )

    def get_test_papers(self):
        """获取测试用论文"""
        logger.info(f"获取 {self.test_paper_count} 篇测试论文...")
        papers = self.arxiv_client.get_recent_papers()
        
        if len(papers) < self.test_paper_count:
            logger.warning(f"只找到 {len(papers)} 篇论文，少于预期的 {self.test_paper_count} 篇")
        
        return papers[:self.test_paper_count]

    def benchmark_serial(self, papers):
        """基准测试：串行分析"""
        logger.info("开始串行分析基准测试...")
        
        start_time = time.time()
        results = []
        
        for i, paper in enumerate(papers, 1):
            logger.info(f"串行处理 {i}/{len(papers)}: {paper.title[:50]}...")
            
            try:
                analysis = self.ai_analyzer.analyze_paper(paper)
                results.append((paper, analysis))
            except Exception as e:
                logger.error(f"串行分析失败: {e}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"串行分析完成: {len(results)}/{len(papers)} 篇成功")
        logger.info(f"串行总时间: {duration:.2f}秒")
        
        return {
            "mode": "串行",
            "total_time": duration,
            "success_count": len(results),
            "total_papers": len(papers),
            "avg_time_per_paper": duration / len(papers) if papers else 0,
            "success_rate": len(results) / len(papers) if papers else 0
        }

    def benchmark_parallel(self, papers, max_workers: int = None):
        """基准测试：并行分析"""
        if max_workers is None:
            max_workers = ParallelPaperAnalyzer.calculate_optimal_workers(
                len(papers), 1
            )
        
        logger.info(f"开始并行分析基准测试（{max_workers} 个工作线程）...")
        
        parallel_analyzer = ParallelPaperAnalyzer(
            ai_analyzer=self.ai_analyzer,
            arxiv_client=self.arxiv_client,
            papers_dir=self.config.PAPERS_DIR,
            max_workers=max_workers,
            batch_size=len(papers)  # 单批处理
        )
        
        start_time = time.time()
        results = parallel_analyzer.analyze_papers_parallel(papers)
        end_time = time.time()
        
        duration = end_time - start_time
        
        logger.info(f"并行分析完成: {len(results)}/{len(papers)} 篇成功")
        logger.info(f"并行总时间: {duration:.2f}秒")
        
        return {
            "mode": f"并行({max_workers}线程)",
            "total_time": duration,
            "success_count": len(results),
            "total_papers": len(papers),
            "avg_time_per_paper": duration / len(papers) if papers else 0,
            "success_rate": len(results) / len(papers) if papers else 0,
            "max_workers": max_workers
        }

    def run_comprehensive_benchmark(self):
        """运行综合基准测试"""
        logger.info("=" * 60)
        logger.info("ArXiv 论文分析性能基准测试")
        logger.info("=" * 60)
        
        # 获取测试论文
        papers = self.get_test_papers()
        
        if not papers:
            logger.error("没有找到测试论文，无法进行基准测试")
            return
        
        logger.info(f"使用 {len(papers)} 篇论文进行测试")
        logger.info("-" * 60)
        
        results = []
        
        # 1. 串行基准测试
        serial_result = self.benchmark_serial(papers)
        results.append(serial_result)
        
        logger.info("-" * 60)
        
        # 2. 不同并行度的基准测试
        worker_counts = [2, 3, 5, 8]
        
        for workers in worker_counts:
            if workers <= len(papers):  # 只测试合理的工作线程数
                parallel_result = self.benchmark_parallel(papers, workers)
                results.append(parallel_result)
                logger.info("-" * 60)
        
        # 3. 生成性能报告
        self.generate_performance_report(results)

    def generate_performance_report(self, results):
        """生成性能报告"""
        logger.info("性能测试报告")
        logger.info("=" * 80)
        
        # 表头
        print(f"{'模式':<15} {'总时间(秒)':<12} {'成功率':<8} {'平均时间/篇':<12} {'性能提升':<10}")
        print("-" * 80)
        
        serial_time = None
        
        for result in results:
            mode = result["mode"]
            total_time = result["total_time"]
            success_rate = f"{result['success_rate']:.1%}"
            avg_time = f"{result['avg_time_per_paper']:.2f}s"
            
            # 计算性能提升
            if "串行" in mode:
                serial_time = total_time
                improvement = "基准"
            else:
                if serial_time:
                    speedup = serial_time / total_time
                    improvement = f"{speedup:.1f}x"
                else:
                    improvement = "N/A"
            
            print(f"{mode:<15} {total_time:<12.2f} {success_rate:<8} {avg_time:<12} {improvement:<10}")
        
        print("-" * 80)
        
        # 推荐配置
        if len(results) > 1:
            best_parallel = max(
                [r for r in results if "并行" in r["mode"]], 
                key=lambda x: x["success_count"] / x["total_time"]
            )
            
            logger.info("推荐配置:")
            logger.info(f"  - 模式: {best_parallel['mode']}")
            logger.info(f"  - 工作线程数: {best_parallel.get('max_workers', 'N/A')}")
            logger.info(f"  - 预期性能提升: {serial_time / best_parallel['total_time']:.1f}x")
            
            # GitHub Actions 成本估算
            if serial_time:
                serial_minutes = serial_time / 60
                parallel_minutes = best_parallel['total_time'] / 60
                cost_saving = (serial_minutes - parallel_minutes) / serial_minutes * 100
                
                logger.info(f"  - GitHub Actions 时间节省: {cost_saving:.1f}%")
                logger.info(f"  - 串行模式: {serial_minutes:.2f} 分钟")
                logger.info(f"  - 并行模式: {parallel_minutes:.2f} 分钟")

    def quick_test(self, paper_count: int = 3):
        """快速测试（用于验证功能）"""
        logger.info(f"快速性能测试（{paper_count} 篇论文）")
        logger.info("-" * 40)
        
        papers = self.get_test_papers()[:paper_count]
        
        if not papers:
            logger.error("没有找到测试论文")
            return
        
        # 串行测试
        serial_result = self.benchmark_serial(papers)
        
        # 并行测试
        parallel_result = self.benchmark_parallel(papers, 3)
        
        # 简单对比
        speedup = serial_result["total_time"] / parallel_result["total_time"]
        
        logger.info(f"快速测试结果:")
        logger.info(f"  串行时间: {serial_result['total_time']:.2f}秒")
        logger.info(f"  并行时间: {parallel_result['total_time']:.2f}秒")
        logger.info(f"  性能提升: {speedup:.1f}x")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ArXiv论文分析性能基准测试")
    parser.add_argument("--papers", type=int, default=10, help="测试论文数量")
    parser.add_argument("--quick", action="store_true", help="快速测试模式")
    
    args = parser.parse_args()
    
    try:
        benchmark = PerformanceBenchmark(args.papers)
        
        if args.quick:
            benchmark.quick_test(3)
        else:
            benchmark.run_comprehensive_benchmark()
            
    except Exception as e:
        logger.error(f"基准测试失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 