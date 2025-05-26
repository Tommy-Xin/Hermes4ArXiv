#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-dotenv>=1.0.0", "requests>=2.31.0"]
# ///
"""
环境变量验证脚本
验证所有必需的环境变量是否已正确设置
"""

import os
import sys
import re
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import requests
except ImportError:
    requests = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)


def print_section(title):
    """打印章节标题"""
    print(f"\n📋 {title}")
    print('-'*40)


def validate_required_vars():
    """验证必需的环境变量"""
    print_section("必需环境变量检查")
    
    required_vars = {
        'DEEPSEEK_API_KEY': {
            'description': 'DeepSeek AI API 密钥',
            'pattern': r'^sk-[a-zA-Z0-9]{32,}$',
            'help': '访问 https://platform.deepseek.com/ 获取'
        },
        'SMTP_SERVER': {
            'description': 'SMTP 服务器地址',
            'pattern': r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'help': '如: smtp.qq.com, smtp.gmail.com'
        },
        'SMTP_USERNAME': {
            'description': '邮箱账号',
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'help': '完整的邮箱地址'
        },
        'SMTP_PASSWORD': {
            'description': '邮箱授权码',
            'pattern': r'^.{8,}$',
            'help': '邮箱的授权码，不是登录密码'
        },
        'EMAIL_FROM': {
            'description': '发件人邮箱',
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'help': '通常与 SMTP_USERNAME 相同'
        },
        'EMAIL_TO': {
            'description': '收件人邮箱',
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(,\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})*$',
            'help': '单个或多个邮箱，用逗号分隔'
        }
    }
    
    missing_vars = []
    invalid_vars = []
    
    for var, config in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"   ❌ {var}: 未设置")
            print(f"      📝 {config['description']}")
            print(f"      💡 {config['help']}")
        elif not re.match(config['pattern'], value.strip()):
            invalid_vars.append(var)
            print(f"   ⚠️  {var}: 格式可能有误")
            print(f"      📝 {config['description']}")
            print(f"      💡 {config['help']}")
        else:
            # 隐藏敏感信息
            display_value = value if var not in ['DEEPSEEK_API_KEY', 'SMTP_PASSWORD'] else f"{value[:8]}..."
            print(f"   ✅ {var}: {display_value}")
    
    if missing_vars or invalid_vars:
        print(f"\n❌ 发现问题:")
        if missing_vars:
            print(f"   缺少变量: {', '.join(missing_vars)}")
        if invalid_vars:
            print(f"   格式错误: {', '.join(invalid_vars)}")
        return False
    else:
        print("\n✅ 所有必需的环境变量都已正确设置")
        return True


def validate_optional_vars():
    """验证可选的环境变量"""
    print_section("可选环境变量状态")
    
    optional_vars = {
        'SMTP_PORT': {'default': '587', 'description': 'SMTP 端口'},
        'CATEGORIES': {'default': 'cs.AI,cs.LG,cs.CL', 'description': '论文类别'},
        'MAX_PAPERS': {'default': '50', 'description': '最大论文数量'},
        'SEARCH_DAYS': {'default': '2', 'description': '搜索天数'},
        'AI_MODEL': {'default': 'deepseek-chat', 'description': 'AI 模型'},
        'API_RETRY_TIMES': {'default': '3', 'description': 'API 重试次数'},
        'API_DELAY': {'default': '2', 'description': 'API 调用间隔'}
    }
    
    for var, config in optional_vars.items():
        value = os.getenv(var, config['default'])
        status = "✅ 已设置" if os.getenv(var) else "⚠️  使用默认值"
        print(f"   {var}: {value} ({status}) - {config['description']}")


def test_smtp_connection():
    """测试 SMTP 连接"""
    print_section("SMTP 连接测试")
    
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not all([smtp_server, smtp_username, smtp_password]):
        print("   ⚠️  跳过 SMTP 测试: 缺少必需配置")
        return False
    
    try:
        print(f"   🔗 连接到 {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("   🔐 验证登录凭据...")
        server.login(smtp_username, smtp_password)
        server.quit()
        
        print("   ✅ SMTP 连接测试成功")
        return True
    except Exception as e:
        print(f"   ❌ SMTP 连接失败: {e}")
        print("   💡 请检查:")
        print("      - SMTP 服务器地址和端口")
        print("      - 邮箱账号和授权码")
        print("      - 网络连接")
        return False


def test_api_connection():
    """测试 API 连接"""
    print_section("DeepSeek API 连接测试")
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("   ⚠️  跳过 API 测试: 缺少 DEEPSEEK_API_KEY")
        return False
    
    if not requests:
        print("   ⚠️  跳过 API 测试: 缺少 requests 库")
        return False
    
    try:
        print("   🔗 测试 API 连接...")
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 测试简单的 API 调用
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json={
                'model': 'deepseek-chat',
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'max_tokens': 10
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ API 连接测试成功")
            return True
        elif response.status_code == 401:
            print("   ❌ API 密钥无效")
            return False
        else:
            print(f"   ⚠️  API 返回状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ API 连接失败: {e}")
        print("   💡 请检查:")
        print("      - API 密钥是否正确")
        print("      - 账户余额是否充足")
        print("      - 网络连接")
        return False


def check_file_permissions():
    """检查文件权限"""
    print_section("文件权限检查")
    
    project_root = Path(__file__).parent.parent
    
    # 检查关键目录
    dirs_to_check = [
        project_root / "src",
        project_root / "src" / "papers",
        project_root / "src" / "logs",
        project_root / "src" / "templates"
    ]
    
    all_ok = True
    for dir_path in dirs_to_check:
        if dir_path.exists():
            if os.access(dir_path, os.W_OK):
                print(f"   ✅ {dir_path.name}: 可写")
            else:
                print(f"   ❌ {dir_path.name}: 无写权限")
                all_ok = False
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ {dir_path.name}: 已创建")
            except Exception as e:
                print(f"   ❌ {dir_path.name}: 创建失败 - {e}")
                all_ok = False
    
    return all_ok


def generate_setup_commands():
    """生成设置命令"""
    print_section("快速设置命令")
    
    print("   📝 本地开发设置:")
    print("      cp env.example .env")
    print("      # 编辑 .env 文件填入真实值")
    print("      uv run scripts/validate_env.py")
    
    print("\n   🔧 GitHub Secrets 设置:")
    secrets = [
        'DEEPSEEK_API_KEY',
        'SMTP_SERVER', 
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'EMAIL_FROM',
        'EMAIL_TO'
    ]
    
    for secret in secrets:
        value = os.getenv(secret, 'your-value-here')
        if secret in ['DEEPSEEK_API_KEY', 'SMTP_PASSWORD']:
            value = 'your-secret-value'
        print(f"      gh secret set {secret} --body '{value}'")


def main():
    """主函数"""
    print_header("ArXiv 论文追踪器 - 环境验证")
    
    all_valid = True
    
    # 验证必需变量
    if not validate_required_vars():
        all_valid = False
    
    # 验证可选变量
    validate_optional_vars()
    
    # 测试连接
    smtp_ok = test_smtp_connection()
    api_ok = test_api_connection()
    
    # 检查文件权限
    files_ok = check_file_permissions()
    
    # 生成设置命令
    generate_setup_commands()
    
    print_header("验证结果")
    
    if all_valid and smtp_ok and api_ok and files_ok:
        print("🎉 所有检查都通过！项目可以正常运行。")
        print("\n🚀 下一步:")
        print("   1. 运行 'make test-components' 测试组件")
        print("   2. 运行 'make run' 执行完整流程")
        print("   3. 推送到 GitHub 触发自动化工作流")
        sys.exit(0)
    else:
        print("❌ 发现问题需要修复:")
        if not all_valid:
            print("   - 环境变量配置不完整")
        if not smtp_ok:
            print("   - SMTP 连接失败")
        if not api_ok:
            print("   - API 连接失败")
        if not files_ok:
            print("   - 文件权限问题")
        
        print("\n💡 解决方案:")
        print("   1. 查看详细的配置指南: SECRETS_SETUP_GUIDE.md")
        print("   2. 检查 .env 文件配置")
        print("   3. 验证邮箱和 API 密钥")
        print("   4. 重新运行此脚本验证")
        sys.exit(1)


if __name__ == "__main__":
    main() 