#!/usr/bin/env python3
"""
单模型配置测试脚本
验证系统能够根据配置的API密钥自动选择使用的模型
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


def test_single_model_selection():
    """测试单模型选择逻辑"""
    print("🧪 单模型配置测试")
    print("=" * 50)
    
    # 加载配置
    try:
        config = Config()
        print("✅ 配置加载成功")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False
    
    # 检查配置的API密钥
    api_keys = {
        'DeepSeek': config.DEEPSEEK_API_KEY,
        'OpenAI': config.OPENAI_API_KEY,
        'Claude': config.CLAUDE_API_KEY,
        'Gemini': config.GEMINI_API_KEY,
    }
    
    configured_apis = [name for name, key in api_keys.items() if key and len(key) > 10]
    print(f"🔑 已配置的API: {configured_apis}")
    
    if not configured_apis:
        print("⚠️ 没有配置任何API密钥，无法进行测试")
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
            print(f"🔄 使用顺序: {status['fallback_order']}")
            
            available_analyzers = [name for name, analyzer_info in status['analyzers'].items() 
                                 if analyzer_info['available']]
            print(f"🤖 可用分析器: {available_analyzers}")
            
            if len(available_analyzers) == 1:
                print("✅ 成功配置为单模型模式")
            elif len(available_analyzers) > 1:
                print(f"⚠️ 检测到多个模型，将使用优先级最高的: {available_analyzers[0]}")
            else:
                print("❌ 没有可用的分析器")
                return False
        else:
            print(f"🔧 使用传统分析器: {info.get('provider', 'unknown')}")
        
    except Exception as e:
        print(f"❌ AI分析器创建失败: {e}")
        return False
    
    # 测试连接
    try:
        connection_info = ai_analyzer.test_connection()
        print(f"🔗 连接测试: {connection_info}")
    except Exception as e:
        print(f"⚠️ 连接测试失败: {e}")
    
    return True


def main():
    """主函数"""
    print("🚀 Hermes4ArXiv 单模型配置测试")
    print("=" * 60)
    
    success = test_single_model_selection()
    
    if success:
        print("\n🎊 单模型配置测试通过！")
        print("\n💡 使用说明:")
        print("   - 系统会自动选择您配置的API密钥对应的模型")
        print("   - 如果配置了多个API，将优先使用SOTA模型（Claude Opus 4）")
        print("   - 您只需要配置一个API密钥即可开始使用")
        return 0
    else:
        print("\n💥 单模型配置测试失败，请检查配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 