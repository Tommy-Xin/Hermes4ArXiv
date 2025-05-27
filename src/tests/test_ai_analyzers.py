#!/usr/bin/env python3
"""
多AI功能测试脚本
测试新的多AI分析器功能
"""

import asyncio
import logging
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from ai.adapter import create_ai_analyzer
from data.arxiv_client import ArxivClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_multi_ai_analyzer():
    """测试多AI分析器"""
    print("🧪 多AI分析器功能测试")
    print("=" * 50)
    
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
        
        # 获取分析器信息
        info = ai_analyzer.get_analyzer_info()
        print(f"📊 分析器类型: {info['type']}")
        
        if info['type'] == 'multi_ai':
            status = info['status']
            print(f"📋 分析策略: {status['strategy']}")
            print(f"🔄 降级顺序: {status['fallback_order']}")
            
            available_analyzers = [name for name, analyzer_info in status['analyzers'].items() 
                                 if analyzer_info['available']]
            print(f"🤖 可用分析器: {available_analyzers}")
            
            if not available_analyzers:
                print("⚠️ 没有可用的AI分析器，请检查API密钥配置")
                return False
        else:
            print(f"🔧 使用传统分析器: {info.get('provider', 'unknown')}")
        
    except Exception as e:
        print(f"❌ AI分析器创建失败: {e}")
        return False
    
    # 测试连接
    try:
        connection_info = ai_analyzer.test_connection()
        print(f"🔗 连接测试结果: {connection_info}")
    except Exception as e:
        print(f"⚠️ 连接测试失败: {e}")
    
    # 获取测试论文
    try:
        print("\n📄 获取测试论文...")
        arxiv_client = ArxivClient(
            categories=["cs.AI"],
            max_papers=1,
            search_days=7
        )
        
        papers = arxiv_client.get_recent_papers()
        if not papers:
            print("❌ 没有找到测试论文")
            return False
        
        test_paper = papers[0]
        print(f"✅ 获取到测试论文: {test_paper.title[:50]}...")
        
    except Exception as e:
        print(f"❌ 获取测试论文失败: {e}")
        return False
    
    # 测试同步分析
    try:
        print("\n🔍 测试同步分析...")
        analysis_result = ai_analyzer.analyze_paper(test_paper)
        
        if analysis_result:
            print("✅ 同步分析成功")
            print(f"📝 分析结果长度: {len(analysis_result)} 字符")
            print(f"📄 分析预览: {analysis_result[:200]}...")
        else:
            print("❌ 同步分析返回空结果")
            return False
            
    except Exception as e:
        print(f"❌ 同步分析失败: {e}")
        return False
    
    # 测试异步分析（如果支持）
    if hasattr(ai_analyzer, 'analyze_paper_async'):
        try:
            print("\n⚡ 测试异步分析...")
            async_result = await ai_analyzer.analyze_paper_async(test_paper)
            
            if async_result:
                print("✅ 异步分析成功")
                print(f"🤖 使用的AI: {async_result.get('provider', 'unknown')}")
                print(f"🧠 使用的模型: {async_result.get('model', 'unknown')}")
                print(f"📝 分析结果长度: {len(async_result.get('analysis', ''))} 字符")
                
                if 'error' in async_result:
                    print(f"⚠️ 分析过程中有错误: {async_result['error']}")
            else:
                print("❌ 异步分析返回空结果")
                
        except Exception as e:
            print(f"❌ 异步分析失败: {e}")
    
    print("\n🎉 多AI功能测试完成！")
    return True


def test_prompt_manager():
    """测试提示词管理器"""
    print("\n🎯 测试提示词管理器")
    print("-" * 30)
    
    from ai.prompts import PromptManager
    
    # 测试不同类型的系统提示词
    for analysis_type in ['comprehensive', 'quick', 'detailed']:
        prompt = PromptManager.get_system_prompt(analysis_type)
        print(f"📋 {analysis_type} 提示词长度: {len(prompt)} 字符")
    
    # 测试HTML格式化
    test_analysis = """🎯 核心贡献
这是一个测试分析。

🔧 技术方法
使用了**深度学习**和*机器学习*技术。

🧪 实验验证
在数据集上取得了95%的准确率。"""
    
    html_result = PromptManager.format_analysis_for_html(test_analysis)
    print(f"🌐 HTML格式化测试: {len(html_result)} 字符")
    print("✅ 提示词管理器测试完成")


def main():
    """主函数"""
    print("🚀 Hermes4ArXiv 多AI功能测试套件")
    print("=" * 60)
    
    # 测试提示词管理器
    test_prompt_manager()
    
    # 测试多AI分析器
    success = asyncio.run(test_multi_ai_analyzer())
    
    if success:
        print("\n🎊 所有测试通过！多AI功能正常工作。")
        return 0
    else:
        print("\n💥 测试失败，请检查配置和网络连接。")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 