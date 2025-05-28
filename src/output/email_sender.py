#!/usr/bin/env python3
"""
邮件发送模块
支持多种邮件格式和错误处理
"""

import datetime
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

# 使用标准logging而不是自定义logger
logger = logging.getLogger(__name__)


class EmailSender:
    """邮件发送器"""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str,
    ):
        """
        初始化邮件发送器

        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP端口
            username: 用户名
            password: 密码
            from_email: 发件人邮箱
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        content: str,
        content_type: str = "html",
    ) -> bool:
        """
        发送邮件

        Args:
            to_emails: 收件人邮箱列表
            subject: 邮件主题
            content: 邮件内容
            content_type: 内容类型 ('html' 或 'plain')

        Returns:
            发送是否成功
        """
        if not to_emails:
            logger.error("收件人邮箱列表为空")
            return False

        try:
            # 创建邮件对象
            msg = MIMEMultipart("alternative")
            msg["From"] = self.from_email
            msg["To"] = ", ".join(to_emails)
            msg["Subject"] = subject

            # 添加邮件内容
            if content_type.lower() == "html":
                msg.attach(MIMEText(content, "html", "utf-8"))
            else:
                msg.attach(MIMEText(content, "plain", "utf-8"))

            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"邮件发送成功，收件人: {', '.join(to_emails)}")
            return True

        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            return False

    def send_paper_analysis_report(
        self, to_emails: List[str], html_content: str, paper_count: int = 0
    ) -> bool:
        """
        发送论文分析报告邮件

        Args:
            to_emails: 收件人邮箱列表
            html_content: HTML格式的邮件内容
            paper_count: 论文数量

        Returns:
            发送是否成功
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = f"📚 ArXiv论文分析报告 - {today}"

        if paper_count > 0:
            subject += f" ({paper_count}篇论文)"

        return self.send_email(to_emails, subject, html_content, "html")

    def send_error_notification(self, to_emails: List[str], error_message: str) -> bool:
        """
        发送错误通知邮件

        Args:
            to_emails: 收件人邮箱列表
            error_message: 错误信息

        Returns:
            发送是否成功
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"⚠️ ArXiv论文追踪器错误通知 - {today}"

        content = f"""
        <html>
        <body>
            <h2>⚠️ ArXiv论文追踪器运行错误</h2>
            <p><strong>时间</strong>: {today}</p>
            <p><strong>错误信息</strong>:</p>
            <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 4px;">
{error_message}
            </pre>
            <p>请检查配置和日志文件以获取更多信息。</p>
        </body>
        </html>
        """

        return self.send_email(to_emails, subject, content, "html")

    def send_ai_analysis_failure_notification(self, to_emails: List[str], paper_count: int = 0) -> bool:
        """
        发送AI分析失败通知邮件

        Args:
            to_emails: 收件人邮箱列表
            paper_count: 尝试分析的论文数量

        Returns:
            发送是否成功
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"🤖 ArXiv论文追踪器 - AI分析失败通知 - {today}"

        content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                    line-height: 1.6;
                    color: #2c3e50;
                    background-color: #f8f9fa;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                    overflow: hidden;
                }}
                .header {{
                    background: #dc3545;
                    color: white;
                    padding: 24px;
                    text-align: center;
                }}
                .content {{
                    padding: 24px;
                }}
                .alert {{
                    background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    color: #721c24;
                    padding: 16px;
                    border-radius: 4px;
                    margin: 16px 0;
                }}
                .solutions {{
                    background-color: #d1ecf1;
                    border: 1px solid #bee5eb;
                    color: #0c5460;
                    padding: 16px;
                    border-radius: 4px;
                    margin: 16px 0;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 16px 24px;
                    text-align: center;
                    font-size: 14px;
                    color: #6c757d;
                }}
                h3 {{
                    color: #495057;
                    margin-bottom: 8px;
                }}
                ul {{
                    margin: 8px 0;
                }}
                li {{
                    margin: 4px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 AI分析服务异常</h1>
                    <p>ArXiv论文追踪器无法完成AI分析</p>
                </div>
                
                <div class="content">
                    <div class="alert">
                        <h3>⚠️ 问题描述</h3>
                        <p><strong>时间</strong>: {today}</p>
                        <p><strong>状态</strong>: 所有AI模型分析失败</p>
                        <p><strong>影响范围</strong>: 今日{paper_count}篇论文无法生成分析报告</p>
                    </div>
                    
                    <div class="solutions">
                        <h3>💡 可能的解决方案</h3>
                        <ul>
                            <li><strong>检查API密钥</strong>: 确认您的DeepSeek API密钥是否有效且有足够余额</li>
                            <li><strong>检查网络连接</strong>: 确认GitHub Actions环境能正常访问DeepSeek API服务</li>
                            <li><strong>临时服务中断</strong>: DeepSeek服务可能临时维护，通常几小时后会恢复</li>
                            <li><strong>重新生成API密钥</strong>: 登录DeepSeek平台重新生成新的API密钥</li>
                            <li><strong>检查余额</strong>: 确认DeepSeek账户有足够的API调用余额</li>
                        </ul>
                    </div>
                    
                    <h3>🔧 推荐配置</h3>
                    <p>为了确保系统正常运行，请在GitHub Secrets中正确配置：</p>
                    <ul>
                        <li><code>DEEPSEEK_API_KEY</code> - DeepSeek API密钥 (必需)</li>
                        <li>访问 <a href="https://platform.deepseek.com/">DeepSeek平台</a> 获取API密钥</li>
                        <li>确保API密钥以 <code>sk-</code> 开头</li>
                    </ul>
                    
                    <h3>📊 下次运行</h3>
                    <p>系统将在下次计划时间自动重试分析。如果问题持续，请检查上述配置项。</p>
                </div>
                
                <div class="footer">
                    <p>这是一封自动生成的通知邮件</p>
                    <p>ArXiv论文追踪器 · 智能学术前沿助手</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(to_emails, subject, content, "html")

    def test_connection(self) -> bool:
        """
        测试邮件服务器连接

        Returns:
            连接是否成功
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)

            logger.info("邮件服务器连接测试成功")
            return True

        except Exception as e:
            logger.error(f"邮件服务器连接测试失败: {str(e)}")
            return False

    @classmethod
    def create_from_config(cls, config) -> Optional["EmailSender"]:
        """
        从配置创建邮件发送器

        Args:
            config: 配置对象

        Returns:
            邮件发送器实例，配置不完整时返回None
        """
        required_configs = [
            config.SMTP_SERVER,
            config.SMTP_PORT,
            config.SMTP_USERNAME,
            config.SMTP_PASSWORD,
            config.EMAIL_FROM,
        ]

        if not all(required_configs):
            logger.error("邮件配置不完整")
            return None

        return cls(
            smtp_server=config.SMTP_SERVER,
            smtp_port=config.SMTP_PORT,
            username=config.SMTP_USERNAME,
            password=config.SMTP_PASSWORD,
            from_email=config.EMAIL_FROM,
        )
