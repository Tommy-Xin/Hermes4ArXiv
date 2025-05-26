#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "arxiv>=1.4.8",
#     "openai>=0.28.0,<1.0.0",
#     "requests>=2.31.0",
#     "jinja2>=3.1.2",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
独立的论文分析脚本
使用 uv 的脚本功能，可以直接运行：uv run scripts/analyze_papers.py
"""

import argparse
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config
from arxiv_client import ArxivClient
from ai_analyzer import AnalyzerFactory
from output_formatter import OutputFormatter


def main():
    parser = argparse.ArgumentParser(description="分析 ArXiv 论文")
    parser.add_argument("--categories", nargs="+", default=["cs.AI"], 
                       help="论文类别")
    parser.add_argument("--max-papers", type=int, default=5, 
                       help="最大论文数量")
    parser.add_argument("--search-days", type=int, default=7, 
                       help="搜索天数")
    parser.add_argument("--output", type=str, default="analysis_output.md", 
                       help="输出文件")
    
    args = parser.parse_args()
    
    print(f"🔍 搜索类别: {args.categories}")
    print(f"📊 最大论文数: {args.max_papers}")
    print(f"📅 搜索天数: {args.search_days}")
    
    # 初始化客户端
    client = ArxivClient(
        categories=args.categories,
        max_papers=args.max_papers,
        search_days=args.search_days
    )
    
    # 获取论文
    papers = client.get_recent_papers()
    print(f"📚 找到 {len(papers)} 篇论文")
    
    if not papers:
        print("❌ 没有找到论文")
        return
    
    # 简单分析（不使用AI）
    papers_analyses = []
    for paper in papers:
        # 创建简单的分析
        analysis = f"""
**核心贡献**: {paper.title}

**技术方法**: 基于论文摘要的初步分析

**摘要**: {paper.summary[:200]}...

**类别**: {', '.join(paper.categories)}
        """
        papers_analyses.append((paper, analysis))
    
    # 格式化输出
    formatter = OutputFormatter(Path(__file__).parent.parent / "src" / "templates")
    markdown_content = formatter.format_markdown(papers_analyses, "快速论文分析")
    
    # 保存到文件
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ 分析结果已保存到: {output_path}")


if __name__ == "__main__":
    main() 