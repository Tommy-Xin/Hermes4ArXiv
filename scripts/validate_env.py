#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-dotenv>=1.0.0", "requests>=2.31.0"]
# ///
"""
环境变量验证脚本
用于验证 Gmail SMTP 配置是否正确
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    # 查找 .env 文件（在项目根目录）
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"📄 已加载环境变量文件: {env_path}")
    else:
        print("⚠️  未找到 .env 文件，使用系统环境变量")
except ImportError:
    print("⚠️  python-dotenv 未安装，使用系统环境变量")

def check_required_env_vars():
    """检查必需的环境变量"""
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
        print("❌ 缺少以下环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ 所有必需的环境变量都已设置")
    return True

def test_smtp_connection():
    """测试 SMTP 连接"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port_str = os.getenv('SMTP_PORT', '587').strip()
        smtp_port = int(smtp_port_str) if smtp_port_str else 587
        username = os.getenv('SMTP_USERNAME')
        password = os.getenv('SMTP_PASSWORD')
        
        print(f"🔍 测试 SMTP 连接: {smtp_server}:{smtp_port}")
        
        # 创建 SMTP 连接
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print("✅ SMTP 服务器连接成功")
        
        # 测试登录
        server.login(username, password)
        print("✅ SMTP 认证成功")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP 认证失败: {e}")
        print("💡 请检查:")
        print("   - 是否使用了应用专用密码（不是登录密码）")
        print("   - 是否启用了两步验证")
        print("   - 用户名是否为完整邮箱地址")
        return False
        
    except Exception as e:
        print(f"❌ SMTP 连接失败: {e}")
        return False

def send_test_email():
    """发送测试邮件"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port_str = os.getenv('SMTP_PORT', '587').strip()
        smtp_port = int(smtp_port_str) if smtp_port_str else 587
        username = os.getenv('SMTP_USERNAME')
        password = os.getenv('SMTP_PASSWORD')
        email_from = os.getenv('EMAIL_FROM')
        email_to = os.getenv('EMAIL_TO')
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "🧪 ArXiv 论文追踪器 - 配置测试"
        
        body = """
        <html>
        <body>
        <h2>🎉 配置测试成功！</h2>
        <p>恭喜！您的 Gmail SMTP 配置已经正确设置。</p>
        <p>ArXiv 论文追踪器现在可以正常发送邮件了。</p>
        <hr>
        <p><small>这是一封自动生成的测试邮件</small></p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # 发送邮件
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        
        text = msg.as_string()
        server.sendmail(email_from, email_to.split(','), text)
        server.quit()
        
        print("✅ 测试邮件发送成功")
        print(f"📧 请检查邮箱: {email_to}")
        return True
        
    except Exception as e:
        print(f"❌ 测试邮件发送失败: {e}")
        return False

def test_deepseek_api():
    """测试 DeepSeek API 连接"""
    try:
        import requests
        
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            print("❌ DEEPSEEK_API_KEY 未设置")
            return False
            
        if not api_key.startswith('sk-'):
            print("❌ DEEPSEEK_API_KEY 格式不正确（应以 'sk-' 开头）")
            return False
            
        # 测试 API 连接
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 发送一个简单的测试请求
        data = {
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': 'Hello'}],
            'max_tokens': 10
        }
        
        response = requests.post(
            'https://api.deepseek.com/chat/completions',
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ DeepSeek API 连接成功")
            return True
        else:
            print(f"❌ DeepSeek API 测试失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except ImportError:
        print("⚠️  requests 库未安装，跳过 API 测试")
        return True
    except Exception as e:
        print(f"❌ DeepSeek API 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 开始验证环境配置...")
    print("=" * 50)
    
    # 检查环境变量
    if not check_required_env_vars():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # 测试 DeepSeek API
    print("🤖 测试 DeepSeek API...")
    test_deepseek_api()
    
    print("\n" + "=" * 50)
    
    # 测试 SMTP 连接
    print("📧 测试 SMTP 连接...")
    if not test_smtp_connection():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # 发送测试邮件
    print("📨 发送测试邮件...")
    if send_test_email():
        print("\n🎉 所有测试通过！配置正确。")
        print("💡 您现在可以运行完整的论文分析了。")
    else:
        print("\n⚠️  邮件发送测试失败，请检查配置。")
        sys.exit(1)

if __name__ == "__main__":
    main() 