# 📧 Gmail 配置详细指南

## 🎯 Gmail SMTP 配置步骤

Gmail 需要特殊的安全设置才能用于 SMTP 发送邮件。请按照以下步骤操作：

### 第一步：启用两步验证

1. **登录 Google 账户**
   - 访问 [Google 账户设置](https://myaccount.google.com/)
   - 使用您的 Gmail 账号登录

2. **进入安全设置**
   - 点击左侧菜单的 **"安全性"**
   - 或直接访问：https://myaccount.google.com/security

3. **启用两步验证**
   - 找到 **"登录 Google"** 部分
   - 点击 **"两步验证"**
   - 如果未启用，点击 **"开始使用"**
   - 按照提示完成设置（通常需要手机号码验证）

### 第二步：生成应用专用密码

1. **返回安全设置页面**
   - 确保两步验证已启用
   - 在 **"登录 Google"** 部分找到 **"应用专用密码"**

2. **创建应用专用密码**
   - 点击 **"应用专用密码"**
   - 可能需要再次输入您的 Google 账户密码
   - 在下拉菜单中选择 **"邮件"**
   - 在设备下拉菜单中选择 **"其他（自定义名称）"**
   - 输入名称：`ArXiv论文追踪器` 或 `GitHub Actions`
   - 点击 **"生成"**

3. **保存生成的密码**
   - Google 会显示一个 16 位的应用专用密码
   - **重要**：立即复制并保存这个密码
   - 格式类似：`abcd efgh ijkl mnop`
   - 这个密码只会显示一次！

### 第三步：配置 GitHub Secrets

在您的 GitHub 仓库中配置以下 Secrets：

| Secret 名称 | 值 | 说明 |
|------------|---|------|
| `SMTP_SERVER` | `smtp.gmail.com` | Gmail SMTP 服务器 |
| `SMTP_PORT` | `587` | SMTP 端口（可选，默认587） |
| `SMTP_USERNAME` | `your-email@gmail.com` | 您的完整 Gmail 地址 |
| `SMTP_PASSWORD` | `abcd efgh ijkl mnop` | 刚生成的应用专用密码 |
| `EMAIL_FROM` | `your-email@gmail.com` | 发件人邮箱（同用户名） |
| `EMAIL_TO` | `recipient@example.com` | 收件人邮箱 |

### 第四步：配置步骤详解

1. **进入您的 GitHub 仓库**
   - 确保您已经 Fork 了 arxiv_paper_tracker 项目

2. **进入 Settings**
   - 点击仓库页面右上角的 **Settings**

3. **进入 Secrets 设置**
   - 在左侧菜单中找到 **Secrets and variables**
   - 点击 **Actions**

4. **添加每个 Secret**
   - 点击 **New repository secret**
   - 输入 Secret 名称（如：`SMTP_SERVER`）
   - 输入对应的值（如：`smtp.gmail.com`）
   - 点击 **Add secret**
   - 重复此步骤添加所有 6 个 Secrets

## 🔍 配置验证

### 方法一：使用设置向导
1. 进入仓库的 **Actions** 页面
2. 选择 **🚀 一键设置 ArXiv 论文追踪器**
3. 点击 **Run workflow**
4. 选择 **check_secrets** 检查配置

### 方法二：手动测试
添加完所有 Secrets 后，运行一次测试：
1. 在 Actions 页面选择 **Daily Paper Analysis**
2. 点击 **Run workflow**
3. 查看运行日志确认邮件发送成功

## ⚠️ 常见问题

### Q1: 找不到"应用专用密码"选项
**A**: 确保您已经启用了两步验证。只有启用两步验证后，应用专用密码选项才会出现。

### Q2: 生成的密码包含空格
**A**: 应用专用密码通常显示为 `abcd efgh ijkl mnop` 格式，在配置时可以包含空格，也可以去掉空格写成 `abcdefghijklmnop`。

### Q3: 邮件发送失败，提示认证错误
**A**: 检查以下几点：
- 确认使用的是应用专用密码，不是 Google 账户密码
- 确认用户名是完整的邮箱地址
- 确认两步验证已正确启用

### Q4: 提示"不够安全的应用"
**A**: 使用应用专用密码就不会有这个问题。如果仍然出现，请确认：
- 使用的是应用专用密码
- SMTP 服务器设置正确
- 端口设置为 587

## 🔐 安全提醒

1. **应用专用密码安全性**
   - 应用专用密码只能用于特定应用
   - 即使泄露也不会影响您的 Google 账户安全
   - 可以随时撤销和重新生成

2. **定期维护**
   - 建议每 6 个月更换一次应用专用密码
   - 不再使用时及时删除应用专用密码

3. **监控使用**
   - 定期检查 Google 账户的安全活动
   - 关注异常登录和应用访问

## 📝 完整配置示例

假设您的 Gmail 是 `john.doe@gmail.com`，生成的应用专用密码是 `abcd efgh ijkl mnop`：

```
SMTP_SERVER: smtp.gmail.com
SMTP_USERNAME: john.doe@gmail.com
SMTP_PASSWORD: abcd efgh ijkl mnop
EMAIL_FROM: john.doe@gmail.com
EMAIL_TO: john.doe@gmail.com
```

## 🎉 配置完成

配置完成后，您将收到：
- 📧 美观的 HTML 格式论文分析邮件
- 🤖 AI 智能分析的论文摘要
- 📊 每日论文统计和分类
- 🔄 完全自动化的每日更新

**开始享受您的 AI 论文助手吧！** 🚀 