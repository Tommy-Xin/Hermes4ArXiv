#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-dotenv>=1.0.0"]
# ///
"""
环境变量验证脚本
验证所有必需的环境变量是否已正确设置
"""

import os
import sys
from pathlib import Path


def validate_required_vars():
    """验证必需的环境变量"""
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
        print(f"❌ 缺少必需的环境变量: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ 所有必需的环境变量都已设置")
        return True


def validate_optional_vars():
    """验证可选的环境变量"""
    optional_vars = {
        'CATEGORIES': 'cs.AI,cs.LG,cs.CL',
        'MAX_PAPERS': '50',
        'SEARCH_DAYS': '2',
        'SMTP_PORT': '587'
    }
    
    print("\n📋 可选环境变量状态:")
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        status = "✅ 已设置" if os.getenv(var) else "⚠️  使用默认值"
        print(f"   {var}: {value} ({status})")


def validate_email_format():
    """验证邮箱格式"""
    email_from = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')
    
    if email_from and '@' not in email_from:
        print(f"❌ EMAIL_FROM 格式错误: {email_from}")
        return False
    
    if email_to:
        emails = [email.strip() for email in email_to.split(',')]
        invalid_emails = [email for email in emails if '@' not in email]
        if invalid_emails:
            print(f"❌ EMAIL_TO 中包含无效邮箱: {', '.join(invalid_emails)}")
            return False
    
    print("✅ 邮箱格式验证通过")
    return True


def test_api_connection():
    """测试 API 连接"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("⚠️  无法测试 API 连接: 缺少 DEEPSEEK_API_KEY")
        return False
    
    if len(api_key) < 10:
        print("❌ DEEPSEEK_API_KEY 似乎太短，请检查")
        return False
    
    print("✅ API 密钥格式验证通过")
    return True


def check_file_permissions():
    """检查文件权限"""
    project_root = Path(__file__).parent.parent
    
    # 检查关键目录
    dirs_to_check = [
        project_root / "src",
        project_root / "src" / "papers",
        project_root / "src" / "logs"
    ]
    
    for dir_path in dirs_to_check:
        if dir_path.exists():
            if not os.access(dir_path, os.W_OK):
                print(f"❌ 目录无写权限: {dir_path}")
                return False
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ 创建目录: {dir_path}")
            except Exception as e:
                print(f"❌ 无法创建目录 {dir_path}: {e}")
                return False
    
    print("✅ 文件权限检查通过")
    return True


def main():
    """主函数"""
    print("🔍 环境变量验证开始...\n")
    
    all_valid = True
    
    # 验证必需变量
    if not validate_required_vars():
        all_valid = False
    
    # 验证可选变量
    validate_optional_vars()
    
    # 验证邮箱格式
    if not validate_email_format():
        all_valid = False
    
    # 测试 API 连接
    if not test_api_connection():
        all_valid = False
    
    # 检查文件权限
    if not check_file_permissions():
        all_valid = False
    
    print("\n" + "="*50)
    
    if all_valid:
        print("🎉 环境验证通过！项目可以正常运行。")
        sys.exit(0)
    else:
        print("❌ 环境验证失败！请修复上述问题后重试。")
        print("\n💡 提示:")
        print("   1. 检查 .env 文件是否存在并包含所有必需变量")
        print("   2. 在 GitHub 仓库设置中添加相应的 Secrets")
        print("   3. 确保邮箱和 API 密钥格式正确")
        sys.exit(1)


if __name__ == "__main__":
    main() 