#!/usr/bin/env python3
"""
ArXiv 论文追踪器 - 快速开始向导
帮助用户快速配置 Gmail SMTP 设置
"""

import os
import sys
import webbrowser
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🚀 ArXiv 论文追踪器 - 快速开始向导")
    print("=" * 60)
    print("这个向导将帮助您快速配置 Gmail SMTP 设置")
    print("让您的 AI 论文助手尽快运行起来！")
    print()

def check_prerequisites():
    """检查前置条件"""
    print("📋 检查前置条件...")
    
    # 检查是否已经 Fork 项目
    if not Path('.git').exists():
        print("❌ 请先 Fork 并克隆此项目到本地")
        print("💡 步骤:")
        print("   1. 访问: https://github.com/your-username/arxiv_paper_tracker")
        print("   2. 点击右上角的 'Fork' 按钮")
        print("   3. 克隆到本地: git clone https://github.com/你的用户名/arxiv_paper_tracker.git")
        return False
    
    print("✅ 项目已克隆到本地")
    return True

def guide_gmail_setup():
    """引导 Gmail 设置"""
    print("\n📧 Gmail 配置指南")
    print("-" * 30)
    
    print("Gmail 需要特殊的安全设置才能用于 SMTP。")
    print("我们需要启用两步验证并生成应用专用密码。")
    
    input("\n按 Enter 继续...")
    
    # 步骤1: 两步验证
    print("\n🔐 步骤 1: 启用两步验证")
    print("1. 我将为您打开 Google 账户安全设置页面")
    print("2. 找到 '登录 Google' 部分")
    print("3. 点击 '两步验证' 并按提示设置")
    
    if input("\n是否打开 Google 安全设置页面？(y/n): ").lower() == 'y':
        webbrowser.open('https://myaccount.google.com/security')
    
    input("\n✅ 两步验证设置完成后，按 Enter 继续...")
    
    # 步骤2: 应用专用密码
    print("\n🔑 步骤 2: 生成应用专用密码")
    print("1. 在同一个安全设置页面")
    print("2. 找到 '应用专用密码' 选项")
    print("3. 选择 '邮件' 和 '其他（自定义名称）'")
    print("4. 输入名称: 'ArXiv论文追踪器'")
    print("5. 复制生成的 16 位密码")
    
    input("\n按 Enter 继续...")
    
    return True

def collect_configuration():
    """收集配置信息"""
    print("\n📝 收集配置信息")
    print("-" * 30)
    
    config = {}
    
    # Gmail 地址
    while True:
        email = input("请输入您的 Gmail 地址: ").strip()
        if email and '@gmail.com' in email:
            config['gmail'] = email
            break
        print("❌ 请输入有效的 Gmail 地址")
    
    # 应用专用密码
    while True:
        password = input("请输入刚生成的应用专用密码: ").strip()
        if password and len(password) >= 16:
            config['app_password'] = password
            break
        print("❌ 应用专用密码应该是 16 位字符")
    
    # DeepSeek API Key
    print("\n🤖 DeepSeek API 配置")
    print("访问 https://platform.deepseek.com/ 获取 API 密钥")
    
    if input("是否打开 DeepSeek 平台？(y/n): ").lower() == 'y':
        webbrowser.open('https://platform.deepseek.com/')
    
    while True:
        api_key = input("请输入 DeepSeek API 密钥: ").strip()
        if api_key and api_key.startswith('sk-'):
            config['api_key'] = api_key
            break
        print("❌ API 密钥应该以 'sk-' 开头")
    
    # 收件人邮箱
    recipient = input(f"收件人邮箱（默认使用 {config['gmail']}）: ").strip()
    config['recipient'] = recipient if recipient else config['gmail']
    
    return config

def generate_github_secrets_commands(config):
    """生成 GitHub Secrets 设置命令"""
    print("\n🔧 GitHub Secrets 设置")
    print("-" * 30)
    
    secrets = {
        'DEEPSEEK_API_KEY': config['api_key'],
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_USERNAME': config['gmail'],
        'SMTP_PASSWORD': config['app_password'],
        'EMAIL_FROM': config['gmail'],
        'EMAIL_TO': config['recipient']
    }
    
    print("请在您的 GitHub 仓库中设置以下 Secrets:")
    print("路径: Settings → Secrets and variables → Actions")
    print()
    
    for name, value in secrets.items():
        # 隐藏敏感信息
        display_value = value
        if name in ['DEEPSEEK_API_KEY', 'SMTP_PASSWORD']:
            display_value = f"{value[:8]}..."
        
        print(f"Secret 名称: {name}")
        print(f"Secret 值:   {display_value}")
        print("-" * 40)
    
    # 生成 GitHub CLI 命令
    print("\n💡 如果您安装了 GitHub CLI，可以使用以下命令:")
    for name, value in secrets.items():
        print(f"gh secret set {name} --body '{value}'")

def create_env_file(config):
    """创建本地 .env 文件"""
    print("\n📄 创建本地 .env 文件")
    print("-" * 30)
    
    env_content = f"""# ArXiv 论文追踪器配置文件
# 请勿将此文件提交到 Git

# DeepSeek API 配置
DEEPSEEK_API_KEY={config['api_key']}

# Gmail SMTP 配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME={config['gmail']}
SMTP_PASSWORD={config['app_password']}

# 邮件配置
EMAIL_FROM={config['gmail']}
EMAIL_TO={config['recipient']}

# 可选配置
MAX_PAPERS=50
SEARCH_DAYS=2
CATEGORIES=cs.AI,cs.LG,cs.CL
"""
    
    env_path = Path('.env')
    if env_path.exists():
        if input("⚠️  .env 文件已存在，是否覆盖？(y/n): ").lower() != 'y':
            return
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env 文件已创建")
    print("💡 您现在可以在本地测试配置了")

def run_validation_test():
    """运行验证测试"""
    print("\n🧪 运行配置验证测试")
    print("-" * 30)
    
    if input("是否立即运行配置验证测试？(y/n): ").lower() == 'y':
        print("运行验证脚本...")
        os.system("python validate_env.py")

def show_next_steps():
    """显示后续步骤"""
    print("\n🎉 配置完成！")
    print("=" * 60)
    
    print("📋 后续步骤:")
    print("1. 在 GitHub 仓库中设置上述 Secrets")
    print("2. 进入 Actions 页面运行 '🚀 一键设置 ArXiv 论文追踪器'")
    print("3. 选择 'test_configuration' 测试配置")
    print("4. 选择 'run_analysis' 运行测试分析")
    print("5. 配置成功后，系统将每天自动运行")
    
    print("\n📚 相关文档:")
    print("- Gmail 详细配置: GMAIL_SETUP_GUIDE.md")
    print("- 完整部署指南: DEPLOY_FOR_USERS.md")
    print("- 安全说明: SECURITY.md")
    
    print("\n🆘 如遇问题:")
    print("- 运行: python validate_env.py 验证配置")
    print("- 查看 GitHub Actions 日志")
    print("- 检查邮箱是否收到测试邮件")

def main():
    """主函数"""
    print_banner()
    
    # 检查前置条件
    if not check_prerequisites():
        sys.exit(1)
    
    # 引导 Gmail 设置
    if not guide_gmail_setup():
        sys.exit(1)
    
    # 收集配置信息
    config = collect_configuration()
    
    # 生成 GitHub Secrets 命令
    generate_github_secrets_commands(config)
    
    # 创建本地 .env 文件
    if input("\n是否创建本地 .env 文件用于测试？(y/n): ").lower() == 'y':
        create_env_file(config)
    
    # 运行验证测试
    run_validation_test()
    
    # 显示后续步骤
    show_next_steps()

if __name__ == "__main__":
    main() 