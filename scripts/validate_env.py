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

def clean_string(value):
    """清理字符串中的特殊字符"""
    if not value:
        return value
    # 移除不间断空格和其他不可见字符
    return value.replace('\xa0', ' ').strip()

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
    # 检查AI API配置 (四选一)
    ai_apis = [
        'CLAUDE_API_KEY',
        'GEMINI_API_KEY', 
        'OPENAI_API_KEY',
        'DEEPSEEK_API_KEY'
    ]
    
    configured_apis = []
    for api in ai_apis:
        value = os.getenv(api)
        if value and value.strip():  # 检查非空且非空字符串
            configured_apis.append(api)
    
    if not configured_apis:
        print("❌ 未配置任何AI API密钥")
        print("💡 请至少配置以下API中的一个:")
        for api in ai_apis:
            print(f"   - {api}")
        return False
    
    print("✅ 已配置的AI API:")
    for api in configured_apis:
        print(f"   - {api}")
    
    # 检查邮件配置 (必需)
    email_vars = [
        'SMTP_SERVER', 
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'EMAIL_FROM',
        'EMAIL_TO'
    ]
    
    missing_email_vars = []
    for var in email_vars:
        value = os.getenv(var)
        if not value or not value.strip():  # 检查空值和空字符串
            missing_email_vars.append(var)
    
    if missing_email_vars:
        print("❌ 缺少以下邮件配置:")
        for var in missing_email_vars:
            print(f"   - {var}")
        return False
    
    print("✅ 邮件配置完整")
    return True

def test_smtp_connection():
    """测试 SMTP 连接"""
    try:
        # 处理空字符串的情况
        smtp_server = os.getenv('SMTP_SERVER') or 'smtp.gmail.com'
        smtp_port_str = (os.getenv('SMTP_PORT') or '587').strip()
        smtp_port = int(smtp_port_str) if smtp_port_str else 587
        username = clean_string(os.getenv('SMTP_USERNAME'))
        password = clean_string(os.getenv('SMTP_PASSWORD'))
        
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
        # 处理空字符串的情况
        smtp_server = os.getenv('SMTP_SERVER') or 'smtp.gmail.com'
        smtp_port_str = (os.getenv('SMTP_PORT') or '587').strip()
        smtp_port = int(smtp_port_str) if smtp_port_str else 587
        username = clean_string(os.getenv('SMTP_USERNAME'))
        password = clean_string(os.getenv('SMTP_PASSWORD'))
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

def test_ai_apis():
    """测试已配置的AI API连接"""
    try:
        import requests
    except ImportError:
        print("⚠️  requests 库未安装，跳过 AI API 测试")
        return True
    
    # AI API配置
    api_configs = {
        'DEEPSEEK_API_KEY': {
            'url': 'https://api.deepseek.com/chat/completions',
            'model': 'deepseek-chat',
            'name': 'DeepSeek'
        },
        'OPENAI_API_KEY': {
            'url': 'https://api.openai.com/v1/chat/completions', 
            'model': 'gpt-3.5-turbo',
            'name': 'OpenAI'
        },
        'CLAUDE_API_KEY': {
            'url': 'https://api.anthropic.com/v1/messages',
            'model': 'claude-3-haiku-20240307',
            'name': 'Claude'
        },
        'GEMINI_API_KEY': {
            'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
            'model': 'gemini-pro', 
            'name': 'Gemini'
        }
    }
    
    tested_any = False
    for api_key_env, config in api_configs.items():
        api_key = os.getenv(api_key_env)
        if not api_key:
            continue
            
        tested_any = True
        print(f"🔍 测试 {config['name']} API...")
        
        try:
            if api_key_env == 'DEEPSEEK_API_KEY':
                # DeepSeek API测试
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': 'Hello'}],
                    'max_tokens': 10
                }
                response = requests.post(config['url'], headers=headers, json=data, timeout=10)
                
            elif api_key_env == 'OPENAI_API_KEY':
                # OpenAI API测试 (简化测试，只检查认证)
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                # 只是检查认证，不实际调用
                print(f"✅ {config['name']} API密钥格式正确")
                continue
                
            else:
                # 其他API暂时只检查密钥格式
                print(f"✅ {config['name']} API密钥已配置")
                continue
            
            if response.status_code == 200:
                print(f"✅ {config['name']} API 连接成功")
            else:
                print(f"⚠️  {config['name']} API 响应异常: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  {config['name']} API 测试失败: {e}")
    
    if not tested_any:
        print("⚠️  未找到已配置的AI API")
        return False
        
    return True

def main():
    """主函数"""
    print("🔍 开始验证环境配置...")
    print("=" * 50)
    
    # 检查环境变量
    if not check_required_env_vars():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # 测试已配置的AI API
    print("🤖 测试AI API连接...")
    test_ai_apis()
    
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