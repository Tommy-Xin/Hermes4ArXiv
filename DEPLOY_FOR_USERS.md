# 🚀 用户部署指南 - 如何使用 ArXiv 论文追踪器

## 📋 概述

这个项目完全运行在 **GitHub Actions** 上，您的所有密钥都是**私有且安全的**。其他人无法看到您的配置信息。

## 🔐 安全保障

### ✅ 您的密钥完全安全
- **加密存储**: GitHub Secrets 使用企业级加密
- **仅您可见**: 只有您能设置和使用这些密钥
- **日志屏蔽**: 密钥在日志中自动显示为 `***`
- **Fork 隔离**: 其他人 Fork 您的项目时不会获得您的密钥

### 🚫 其他人无法访问
- 其他人使用此项目需要配置**自己的密钥**
- 您的 API 费用和邮箱完全私有
- 代码是开源的，但配置是私有的

## 🎯 一键部署流程

### 步骤 1: Fork 项目
1. 点击本仓库右上角的 **Fork** 按钮
2. 创建您自己的副本

### 步骤 2: 配置 GitHub Secrets
在您的 Fork 仓库中：

1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 添加以下 6 个密钥：

| Secret 名称 | 描述 | 示例 |
|------------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek AI API 密钥 | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `SMTP_SERVER` | 邮件服务器地址 | `smtp.qq.com` |
| `SMTP_USERNAME` | 邮箱账号 | `your-email@qq.com` |
| `SMTP_PASSWORD` | 邮箱授权码 | `abcdefghijklmnop` |
| `EMAIL_FROM` | 发件人邮箱 | `your-email@qq.com` |
| `EMAIL_TO` | 收件人邮箱 | `recipient@example.com` |

### 步骤 3: 验证配置
1. 进入 **Actions** 页面
2. 选择 **🚀 一键设置 ArXiv 论文追踪器**
3. 点击 **Run workflow**
4. 选择 **check_secrets** 检查配置

### 步骤 4: 测试运行
1. 配置验证通过后，再次运行工作流
2. 选择 **test_configuration** 测试配置
3. 选择 **run_analysis** 运行测试分析

### 步骤 5: 启用自动化
配置成功后，系统将：
- ✅ 每天早上 8:00 自动运行
- ✅ 发送论文分析邮件到您的邮箱
- ✅ 完全自动化，无需人工干预

## 🔑 获取必需的密钥

### 1. DeepSeek API Key
1. 访问 [DeepSeek 平台](https://platform.deepseek.com/)
2. 注册账号并登录
3. 充值（建议至少 $5，实际使用成本很低）
4. 创建 API Key
5. 复制密钥（格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）

### 2. 邮箱配置（以 QQ 邮箱为例）
1. 登录 QQ 邮箱
2. 进入 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP** 服务
4. 开启 **SMTP** 服务
5. 生成**授权码**（这不是您的登录密码！）
6. 记录以下信息：
   - SMTP_SERVER: `smtp.qq.com`
   - SMTP_USERNAME: 您的 QQ 邮箱
   - SMTP_PASSWORD: 刚生成的授权码
   - EMAIL_FROM: 您的 QQ 邮箱
   - EMAIL_TO: 接收论文的邮箱

### 3. 其他邮箱服务商
| 服务商 | SMTP 服务器 | 端口 | 说明 |
|--------|-------------|------|------|
| QQ 邮箱 | smtp.qq.com | 587 | 需要开启 SMTP 并生成授权码 |
| 163 邮箱 | smtp.163.com | 587 | 需要开启 SMTP 并设置客户端授权密码 |
| Gmail | smtp.gmail.com | 587 | 需要开启两步验证并生成应用专用密码 |
| Outlook | smtp-mail.outlook.com | 587 | 需要开启两步验证 |

## 💰 成本估算

### DeepSeek API 费用
- **每篇论文分析**: 约 $0.01-0.02
- **每日 50 篇论文**: 约 $0.5-1.0
- **每月费用**: 约 $15-30
- **年费用**: 约 $180-360

### 其他费用
- **GitHub Actions**: 免费（公开仓库）
- **邮件发送**: 免费
- **存储**: 免费

## 🔄 日常使用

### 自动运行
- 配置完成后完全自动化
- 每天早上 8:00 收到邮件
- 无需任何手动操作

### 手动触发
1. 进入 **Actions** 页面
2. 选择 **Daily Paper Analysis**
3. 点击 **Run workflow**

### 调整配置
如需修改搜索参数，在 Secrets 中添加：
- `MAX_PAPERS`: 最大论文数量（默认 50）
- `SEARCH_DAYS`: 搜索天数（默认 2）
- `CATEGORIES`: 论文类别（默认 cs.AI,cs.LG,cs.CL）

## 🆘 常见问题

### Q: 其他人能看到我的密钥吗？
**A: 绝对不能！** GitHub Secrets 是完全私有的，即使项目是公开的。

### Q: 我的 API 费用会被其他人使用吗？
**A: 不会！** 每个人都需要配置自己的 API 密钥。

### Q: 如何停止自动运行？
**A: 在 Actions 页面禁用工作流，或删除 Secrets。**

### Q: 邮件发送失败怎么办？
**A: 检查邮箱授权码（不是登录密码），确认 SMTP 设置正确。**

### Q: API 调用失败怎么办？
**A: 检查 API 密钥和账户余额，确认网络连接正常。**

## 🎉 享受您的 AI 论文助手！

配置完成后，您将拥有一个：
- 🤖 **智能的** AI 论文分析助手
- 📧 **美观的** HTML 邮件报告
- 🔄 **自动化的** 每日更新
- 🔐 **安全的** 私有配置
- 💰 **经济的** 运行成本

**开始您的学术追踪之旅吧！** 🚀 