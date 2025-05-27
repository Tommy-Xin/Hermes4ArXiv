#!/usr/bin/env python3
"""
本地环境验证脚本 - 跳过 SMTP 测试
适用于网络环境限制的情况
"""

import os
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from dotenv import load_dotenv
    from config import Config
    from ai_analyzer import AnalyzerFactory
    import requests
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("💡 请确保已安装所有依赖: uv sync --all-extras --dev")
    sys.exit(1)

def load_environment():
    """加载环境变量"""
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
        print(f"📄 已加载环境变量文件: {env_file.absolute()}")
    else:
        print("⚠️  未找到 .env 文件，使用系统环境变量")

def validate_required_vars():
    """验证必需的环境变量"""
    print("🔍 验证必需的环境变量...")
    print("=" * 50)
    
    required_vars = [
        'DEEPSEEK_API_KEY',
        'SMTP_SERVER', 
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'EMAIL_FROM',
        'EMAIL_TO'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少以下环境变量: {', '.join(missing_vars)}")
        return False
    
    print("✅ 所有必需的环境变量都已设置")
    return True

def test_deepseek_api():
    """测试 DeepSeek API 连接"""
    print("\n" + "=" * 50)
    print("🤖 测试 DeepSeek API...")
    
    try:
        config = Config()
        analyzer = AnalyzerFactory.create_analyzer(
            "deepseek",
            api_key=config.DEEPSEEK_API_KEY,
            model=config.AI_MODEL,
            retry_times=config.API_RETRY_TIMES,
            delay=config.API_DELAY
        )
        
        # 简单的 API 测试 - 直接调用 OpenAI API
        import openai
        openai.api_key = config.DEEPSEEK_API_KEY
        openai.api_base = "https://api.deepseek.com/v1"
        
        response = openai.ChatCompletion.create(
            model=config.AI_MODEL,
            messages=[
                {"role": "user", "content": "请简单回答：这是一个API连接测试。"}
            ],
            max_tokens=50
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print("✅ DeepSeek API 连接成功")
            print(f"📝 测试响应: {content[:100]}...")
            return True
        else:
            print("❌ DeepSeek API 响应为空")
            return False
            
    except Exception as e:
        print(f"❌ DeepSeek API 测试失败: {e}")
        return False

def test_arxiv_connection():
    """测试 arXiv 连接"""
    print("\n" + "=" * 50)
    print("📚 测试 arXiv 连接...")
    
    try:
        # 测试 arXiv API 连接
        test_url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ arXiv API 连接成功")
            return True
        else:
            print(f"❌ arXiv API 连接失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ arXiv 连接测试失败: {e}")
        return False

def test_config_loading():
    """测试配置加载"""
    print("\n" + "=" * 50)
    print("⚙️  测试配置加载...")
    
    try:
        config = Config()
        
        # 验证关键配置
        checks = [
            ("AI_MODEL", config.AI_MODEL),
            ("MAX_PAPERS", config.MAX_PAPERS),
            ("SEARCH_DAYS", config.SEARCH_DAYS),
            ("CATEGORIES", config.CATEGORIES),
            ("API_RETRY_TIMES", config.API_RETRY_TIMES),
            ("API_DELAY", config.API_DELAY),
        ]
        
        for name, value in checks:
            print(f"   {name}: {value}")
        
        print("✅ 配置加载成功")
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def show_smtp_skip_notice():
    """显示 SMTP 跳过通知"""
    print("\n" + "=" * 50)
    print("📧 SMTP 测试 (已跳过)")
    print("💡 本地网络环境可能无法访问 SMTP 服务器")
    print("🚀 建议在 GitHub Actions 中进行完整测试")
    print("📋 GitHub Actions 测试步骤:")
    print("   1. 确保所有 Secrets 已在 GitHub 仓库中配置")
    print("   2. 进入 Actions → 🚀 一键设置 ArXiv 论文追踪器")
    print("   3. 选择 'test_configuration' 运行测试")

def show_github_actions_guide():
    """显示 GitHub Actions 测试指南"""
    print("\n" + "🚀" + "=" * 49)
    print("GitHub Actions 完整测试指南")
    print("=" * 50)
    
    print("\n📋 必需的 GitHub Secrets:")
    secrets = [
        "DEEPSEEK_API_KEY",
        "SMTP_SERVER", 
        "SMTP_USERNAME",
        "SMTP_PASSWORD", 
        "EMAIL_FROM",
        "EMAIL_TO"
    ]
    
    for secret in secrets:
        value = os.getenv(secret, "未设置")
        # 隐藏敏感信息
        if secret in ['DEEPSEEK_API_KEY', 'SMTP_PASSWORD']:
            display_value = f"{value[:8]}..." if value != "未设置" else "未设置"
        else:
            display_value = value
        print(f"   {secret}: {display_value}")
    
    print("\n🔧 GitHub Actions 测试步骤:")
    print("1. 进入您的 GitHub 仓库")
    print("2. 点击 'Actions' 页面")
    print("3. 选择 '🚀 一键设置 ArXiv 论文追踪器'")
    print("4. 点击 'Run workflow'")
    print("5. 选择以下测试选项:")
    print("   - check_secrets: 检查所有 Secrets 配置")
    print("   - test_configuration: 测试配置和 SMTP 连接")
    print("   - run_analysis: 运行完整的论文分析测试")

def main():
    """主函数"""
    print("🔍 本地环境验证 (跳过 SMTP 测试)")
    print("=" * 50)
    
    # 加载环境变量
    load_environment()
    
    # 运行测试
    tests = [
        ("环境变量验证", validate_required_vars),
        ("配置加载测试", test_config_loading),
        ("arXiv 连接测试", test_arxiv_connection),
        ("DeepSeek API 测试", test_deepseek_api),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 执行失败: {e}")
            results.append((test_name, False))
    
    # 显示 SMTP 跳过通知
    show_smtp_skip_notice()
    
    # 显示测试结果总结
    print("\n" + "📊" + "=" * 49)
    print("测试结果总结")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("\n🎉 本地验证完成！")
        print("💡 SMTP 功能需要在 GitHub Actions 中测试")
    else:
        print("\n⚠️  部分测试失败，请检查配置")
    
    # 显示 GitHub Actions 指南
    show_github_actions_guide()
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 