#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "arxiv>=1.4.8",
#     "psutil>=5.9.0",
#     "memory-profiler>=0.61.0",
#     "jinja2>=3.1.2",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
性能基准测试脚本
测试不同组件的性能表现
"""

import time
import psutil
import sys
from pathlib import Path
from memory_profiler import profile

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from arxiv_client import ArxivClient
from output_formatter import OutputFormatter


def benchmark_arxiv_search():
    """基准测试 ArXiv 搜索性能"""
    print("🔍 基准测试 ArXiv 搜索性能...")
    
    client = ArxivClient(["cs.AI"], max_papers=10, search_days=7)
    
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    papers = client.get_recent_papers()
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    print(f"⏱️  搜索时间: {end_time - start_time:.2f} 秒")
    print(f"📊 找到论文: {len(papers)} 篇")
    print(f"💾 内存使用: {end_memory - start_memory:.2f} MB")
    
    return papers


@profile
def benchmark_formatting(papers):
    """基准测试格式化性能"""
    print("\n📝 基准测试格式化性能...")
    
    # 创建模拟分析结果
    papers_analyses = []
    for paper in papers:
        analysis = f"模拟分析结果: {paper.title}"
        papers_analyses.append((paper, analysis))
    
    formatter = OutputFormatter(Path(__file__).parent.parent / "src" / "templates")
    
    start_time = time.time()
    
    # 测试 Markdown 格式化
    markdown_content = formatter.format_markdown(papers_analyses)
    
    # 测试 HTML 格式化
    try:
        html_content = formatter.format_html_email(papers_analyses)
    except Exception as e:
        print(f"HTML 格式化失败: {e}")
        html_content = ""
    
    end_time = time.time()
    
    print(f"⏱️  格式化时间: {end_time - start_time:.2f} 秒")
    print(f"📄 Markdown 长度: {len(markdown_content)} 字符")
    print(f"🌐 HTML 长度: {len(html_content)} 字符")


def system_info():
    """显示系统信息"""
    print("💻 系统信息:")
    print(f"   - CPU 核心数: {psutil.cpu_count()}")
    print(f"   - 内存总量: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
    print(f"   - Python 版本: {sys.version}")
    print(f"   - 平台: {sys.platform}")


def main():
    print("🚀 ArXiv 论文追踪器性能基准测试\n")
    
    system_info()
    print()
    
    # 基准测试
    papers = benchmark_arxiv_search()
    
    if papers:
        benchmark_formatting(papers[:5])  # 只测试前5篇论文
    
    print("\n✅ 基准测试完成!")


if __name__ == "__main__":
    main() 