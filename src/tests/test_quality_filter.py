#!/usr/bin/env python3
"""
论文质量筛选功能测试脚本
验证AI质量筛选系统的工作效果
"""

import asyncio
import logging
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from data.arxiv_client import ArxivClient, PaperQualityFilter
from ai.adapter import create_ai_analyzer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_quality_filter():
    """测试论文质量筛选功能"""
    print("🔍 论文质量筛选功能测试")
    print("=" * 60)
    
    # 加载配置
    try:
        config = Config()
        print("✅ 配置加载成功")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 创建AI分析器
    try:
        ai_analyzer = create_ai_analyzer(config)
        print("✅ AI分析器创建成功")
    except Exception as e:
        print(f"❌ AI分析器创建失败: {e}")
        return False
    
    # 创建带质量筛选的ArXiv客户端
    try:
        arxiv_client = ArxivClient(
            categories=["cs.AI", "cs.LG"],
            max_papers=5,  # 测试少量论文
            search_days=1,
            enable_quality_filter=True,
            quality_threshold=60.0,  # 设置较低阈值便于测试
            ai_analyzer=ai_analyzer,
        )
        print("✅ ArXiv客户端（带质量筛选）创建成功")
    except Exception as e:
        print(f"❌ ArXiv客户端创建失败: {e}")
        return False
    
    # 创建不带质量筛选的对比客户端
    try:
        arxiv_client_basic = ArxivClient(
            categories=["cs.AI", "cs.LG"],
            max_papers=15,  # 获取更多论文用于对比
            search_days=1,
            enable_quality_filter=False,
        )
        print("✅ 基础ArXiv客户端创建成功")
    except Exception as e:
        print(f"❌ 基础ArXiv客户端创建失败: {e}")
        return False
    
    # 测试质量筛选器
    print("\n📊 开始质量筛选测试...")
    
    try:
        # 获取基础论文列表
        print("🔄 获取基础论文列表...")
        basic_papers = arxiv_client_basic.get_recent_papers()
        print(f"📄 基础搜索结果: {len(basic_papers)} 篇论文")
        
        # 获取质量筛选后的论文列表
        print("🔄 获取质量筛选后的论文列表...")
        filtered_papers = arxiv_client.get_recent_papers()
        print(f"📄 质量筛选结果: {len(filtered_papers)} 篇论文")
        
        # 显示筛选效果
        if basic_papers:
            print(f"\n📈 筛选效果:")
            print(f"  - 筛选前: {len(basic_papers)} 篇")
            print(f"  - 筛选后: {len(filtered_papers)} 篇")
            if len(basic_papers) > 0:
                filter_rate = (1 - len(filtered_papers) / len(basic_papers)) * 100
                print(f"  - 筛选率: {filter_rate:.1f}%")
        
        # 显示质量评分示例
        if basic_papers:
            print(f"\n🏆 论文质量评分示例:")
            quality_filter = PaperQualityFilter(ai_analyzer)
            
            for i, paper in enumerate(basic_papers[:5], 1):
                score = quality_filter.calculate_paper_score(paper)
                status = "✅ 通过" if score >= 60.0 else "❌ 筛除"
                print(f"  {i}. 分数: {score:.1f} {status}")
                print(f"     标题: {paper.title[:60]}...")
                print()
        
        print("✅ 质量筛选测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 质量筛选测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 Hermes4ArXiv 质量筛选功能测试")
    print("=" * 60)
    
    success = test_quality_filter()
    
    if success:
        print("\n🎊 质量筛选功能测试通过！")
        print("\n💡 使用说明:")
        print("   - 系统会自动评估论文的创新性、技术质量等维度")
        print("   - 只有达到质量阈值的论文才会被选中进行详细分析")
        print("   - 可通过 QUALITY_THRESHOLD 环境变量调整筛选严格程度")
        print("   - 建议设置: 60-70分适中，70分以上较严格")
        return 0
    else:
        print("\n💥 质量筛选功能测试失败，请检查配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 