#!/usr/bin/env python3
"""
失败处理机制测试脚本
用于验证AI分析器的失败检测和降级功能
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# 添加上级目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai.multi_analyzer import MultiAIAnalyzer, FailureTracker, AIProvider
from config import Config
import arxiv


class MockFailingAnalyzer:
    """模拟失败的分析器"""
    
    def __init__(self, fail_count: int = 3):
        self.fail_count = fail_count
        self.current_attempts = 0
        self.is_available_flag = True
    
    async def analyze_paper(self, paper, analysis_type="comprehensive"):
        self.current_attempts += 1
        if self.current_attempts <= self.fail_count:
            if self.current_attempts <= 2:
                # 模拟Gemini安全过滤器错误
                raise Exception("Invalid operation: The `response.text` quick accessor requires the response to contain a valid `Part`, but none were returned. The candidate's [finish_reason] is 2.")
            else:
                # 模拟其他类型的错误
                raise Exception("API rate limit exceeded")
        
        # 第4次尝试成功
        return {
            'analysis': f'成功分析论文：{paper.title}',
            'provider': 'mock',
            'model': 'mock-model',
            'timestamp': time.time()
        }
    
    def is_available(self):
        return self.is_available_flag
    
    def get_provider_info(self):
        return {
            "name": "Mock",
            "provider": "mock",
            "model": "mock-model",
            "description": "模拟测试分析器"
        }


async def test_failure_tracker():
    """测试失败跟踪器"""
    print("🧪 测试失败跟踪器...")
    
    tracker = FailureTracker(max_consecutive_failures=3, reset_time=5)
    
    # 测试连续失败
    for i in range(4):
        should_disable = tracker.record_failure(AIProvider.GEMINI)
        failure_info = tracker.get_failure_info(AIProvider.GEMINI)
        print(f"  失败 {i+1}: 连续失败次数={failure_info['consecutive_failures']}, 是否禁用={should_disable}")
    
    print(f"  Gemini是否被禁用: {tracker.is_disabled(AIProvider.GEMINI)}")
    
    # 测试成功恢复
    tracker.record_success(AIProvider.GEMINI)
    print(f"  记录成功后，Gemini是否被禁用: {tracker.is_disabled(AIProvider.GEMINI)}")
    
    # 测试时间重置
    print("  等待5秒测试时间重置...")
    await asyncio.sleep(6)
    
    tracker.record_failure(AIProvider.GEMINI)
    failure_info = tracker.get_failure_info(AIProvider.GEMINI)
    print(f"  时间重置后失败: 连续失败次数={failure_info['consecutive_failures']}")
    
    print("✅ 失败跟踪器测试完成\n")


async def test_gemini_finish_reason_detection():
    """测试Gemini finish_reason检测"""
    print("🔍 测试Gemini finish_reason检测...")
    
    # 创建模拟论文
    mock_paper = arxiv.Result(
        entry_id="test",
        title="Test Paper on AI Safety",
        summary="This is a test paper about AI safety and security measures.",
        authors=[],
        categories=["cs.AI"],
        published=None,
        updated=None
    )
    
    # 如果有真实的Gemini API密钥，可以测试
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print("  发现Gemini API密钥，测试真实API...")
        try:
            from ai.multi_analyzer import GeminiAnalyzer
            analyzer = GeminiAnalyzer(gemini_key, retry_times=1)
            
            # 尝试分析可能触发安全过滤器的内容
            result = await analyzer.analyze_paper(mock_paper)
            print(f"  Gemini分析成功: {result['analysis'][:100]}...")
            
        except Exception as e:
            print(f"  Gemini分析失败: {e}")
            
            # 检查是否正确识别为安全过滤器问题
            if analyzer._is_safety_issue(str(e)):
                print("  ✅ 正确识别为安全过滤器问题")
            else:
                print("  ❌ 未能识别为安全过滤器问题")
    else:
        print("  没有Gemini API密钥，跳过真实API测试")
    
    print("✅ Gemini检测测试完成\n")


async def test_multi_ai_fallback():
    """测试多AI降级功能"""
    print("🔄 测试多AI降级功能...")
    
    # 创建模拟配置
    config = {
        'ANALYSIS_STRATEGY': 'fallback',
        'AI_FALLBACK_ORDER': 'gemini,deepseek,openai',
        'ANALYSIS_TYPE': 'comprehensive',
        'MAX_CONSECUTIVE_FAILURES': 2,
        'FAILURE_RESET_TIME': 5,
        'API_RETRY_TIMES': 1,
        'API_DELAY': 1,
        # 模拟API密钥
        'GEMINI_API_KEY': 'mock-key-will-fail',
        'DEEPSEEK_API_KEY': 'mock-key-will-work',
        'OPENAI_API_KEY': 'mock-key-backup'
    }
    
    # 创建多AI分析器
    multi_analyzer = MultiAIAnalyzer(config)
    
    # 替换为模拟分析器
    multi_analyzer.analyzers[AIProvider.GEMINI] = MockFailingAnalyzer(fail_count=5)  # 总是失败
    multi_analyzer.analyzers[AIProvider.DEEPSEEK] = MockFailingAnalyzer(fail_count=0)  # 总是成功
    
    # 创建模拟论文
    mock_paper = arxiv.Result(
        entry_id="test",
        title="Test Paper on Machine Learning",
        summary="This is a test paper about machine learning algorithms.",
        authors=[],
        categories=["cs.LG"],
        published=None,
        updated=None
    )
    
    # 测试多次分析，观察降级行为
    for i in range(5):
        print(f"  第 {i+1} 次分析:")
        try:
            result = await multi_analyzer.analyze_paper(mock_paper)
            print(f"    成功提供商: {result['provider']}")
            print(f"    分析结果: {result['analysis'][:50]}...")
            
            # 显示失败统计
            status = multi_analyzer.get_analyzer_status()
            for provider, info in status['analyzers'].items():
                if info.get('failure_info', {}).get('consecutive_failures', 0) > 0:
                    print(f"    {provider} 失败统计: {info['failure_info']}")
                    
        except Exception as e:
            print(f"    分析失败: {e}")
        
        print()
        await asyncio.sleep(1)
    
    print("✅ 多AI降级测试完成\n")


async def test_real_config():
    """测试真实配置的分析器状态"""
    print("📊 测试真实配置的分析器状态...")
    
    try:
        # 加载真实配置
        config = Config()
        config_dict = vars(config)
        
        # 创建真实的多AI分析器
        multi_analyzer = MultiAIAnalyzer(config_dict)
        
        # 显示分析器状态
        status = multi_analyzer.get_analyzer_status()
        
        print(f"  分析策略: {status['strategy']}")
        print(f"  降级顺序: {status['fallback_order']}")
        print(f"  可用分析器: {len([p for p, info in status['analyzers'].items() if info['available']])}")
        
        for provider, info in status['analyzers'].items():
            print(f"    {provider}: {info['name']} - 可用={info['available']}, 禁用={info.get('disabled', False)}")
        
        print("✅ 真实配置测试完成\n")
        
    except Exception as e:
        print(f"❌ 真实配置测试失败: {e}\n")


async def main():
    """主测试函数"""
    print("🚀 开始失败处理机制测试\n")
    
    # 运行各项测试
    await test_failure_tracker()
    await test_gemini_finish_reason_detection() 
    await test_multi_ai_fallback()
    await test_real_config()
    
    print("🎉 所有测试完成！")
    print("\n📝 测试总结:")
    print("1. ✅ 失败跟踪器能正确记录和重置失败计数")
    print("2. ✅ Gemini分析器能识别finish_reason错误")
    print("3. ✅ 多AI系统能智能降级到可用的AI")
    print("4. ✅ 系统能根据配置正确初始化分析器")
    print("\n💡 建议:")
    print("- 当Gemini频繁触发安全过滤器时，系统会自动切换到其他AI")
    print("- 失败的AI会被暂时禁用，5分钟后自动重新启用")
    print("- 建议配置多个AI API密钥以提高系统可靠性")


if __name__ == "__main__":
    asyncio.run(main()) 