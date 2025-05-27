#!/usr/bin/env python3
"""
组件测试脚本
用于验证各个模块是否正常工作
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.analyzers.legacy import AnalyzerFactory
from data.arxiv_client import ArxivClient
from config import Config
from output.email_sender import EmailSender
from output.formatter import OutputFormatter
from utils.logger import logger


def test_config():
    """测试配置模块"""
    print("🔧 测试配置模块...")
    try:
        config = Config()
        print(f"✅ 配置加载成功")
        print(f"   - 论文类别: {config.CATEGORIES}")
        print(f"   - 最大论文数: {config.MAX_PAPERS}")
        print(f"   - 搜索天数: {config.SEARCH_DAYS}")

        # 创建目录
        config.create_directories()
        print(f"✅ 目录创建成功")

        return config
    except Exception as e:
        print(f"❌ 配置模块测试失败: {e}")
        return None


def test_arxiv_client(config):
    """测试ArXiv客户端"""
    print("\n📚 测试ArXiv客户端...")
    try:
        client = ArxivClient(
            categories=["cs.AI"],  # 只测试一个类别
            max_papers=3,  # 只获取3篇论文进行测试
            search_days=7,  # 扩大搜索范围
        )

        papers = client.get_recent_papers()
        print(f"✅ ArXiv客户端测试成功，找到 {len(papers)} 篇论文")

        if papers:
            paper = papers[0]
            print(f"   - 示例论文: {paper.title[:50]}...")

        return papers[:1] if papers else []  # 只返回第一篇用于测试
    except Exception as e:
        print(f"❌ ArXiv客户端测试失败: {e}")
        return []


def test_ai_analyzer(config, papers):
    """测试AI分析器"""
    print("\n🤖 测试AI分析器...")
    if not papers:
        print("⚠️  没有论文可供分析，跳过AI分析器测试")
        return []

    try:
        # 检查是否有API密钥
        if not config.DEEPSEEK_API_KEY:
            print("⚠️  未配置DEEPSEEK_API_KEY，跳过AI分析器测试")
            return []

        analyzer = AnalyzerFactory.create_analyzer(
            "deepseek",
            api_key=config.DEEPSEEK_API_KEY,
            model=config.AI_MODEL,
            retry_times=1,  # 测试时只重试1次
            delay=1,  # 测试时缩短延迟
        )

        paper = papers[0]
        print(f"   - 正在分析论文: {paper.title[:50]}...")

        analysis = analyzer.analyze_paper(paper)
        print(f"✅ AI分析器测试成功")
        print(f"   - 分析结果长度: {len(analysis)} 字符")

        return [(paper, analysis)]
    except Exception as e:
        print(f"❌ AI分析器测试失败: {e}")
        return []


def test_output_formatter(config, papers_analyses):
    """测试输出格式化器"""
    print("\n📄 测试输出格式化器...")
    try:
        formatter = OutputFormatter(config.TEMPLATES_DIR, config.GITHUB_REPO_URL)

        if papers_analyses:
            # 测试Markdown格式
            markdown_content = formatter.format_markdown(papers_analyses, "测试报告")
            print(f"✅ Markdown格式化成功，长度: {len(markdown_content)} 字符")

            # 测试HTML格式
            html_content = formatter.format_html_email(papers_analyses)
            print(f"✅ HTML格式化成功，长度: {len(html_content)} 字符")

            # 测试统计信息
            stats = formatter.create_summary_stats(papers_analyses)
            print(f"✅ 统计信息生成成功: {stats}")
        else:
            print("⚠️  没有分析结果可供格式化，跳过部分测试")

        print("✅ 输出格式化器测试成功")
        return True
    except Exception as e:
        print(f"❌ 输出格式化器测试失败: {e}")
        return False


def test_email_sender(config):
    """测试邮件发送器"""
    print("\n📧 测试邮件发送器...")
    try:
        email_sender = EmailSender.create_from_config(config)

        if email_sender:
            # 只测试连接，不发送实际邮件
            connection_ok = email_sender.test_connection()
            if connection_ok:
                print("✅ 邮件服务器连接测试成功")
            else:
                print("❌ 邮件服务器连接测试失败")
        else:
            print("⚠️  邮件配置不完整，跳过邮件发送器测试")

        return True
    except Exception as e:
        print(f"❌ 邮件发送器测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始组件测试...\n")

    # 测试配置
    config = test_config()
    if not config:
        print("\n❌ 配置测试失败，无法继续")
        return

    # 测试ArXiv客户端
    papers = test_arxiv_client(config)

    # 测试AI分析器
    papers_analyses = test_ai_analyzer(config, papers)

    # 测试输出格式化器
    test_output_formatter(config, papers_analyses)

    # 测试邮件发送器
    test_email_sender(config)

    print("\n🎉 组件测试完成！")
    print("\n💡 提示:")
    print("   - 如果所有测试都通过，说明项目配置正确")
    print("   - 如果某些测试失败，请检查相应的配置")
    print("   - 运行 'python main.py' 开始正式的论文分析")


if __name__ == "__main__":
    main()
