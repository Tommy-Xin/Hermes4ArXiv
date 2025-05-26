# 🚀 快速开始指南

## 📋 您需要配置的密钥信息

### 🔑 必需配置（6个）

| 配置项 | 描述 | 获取方式 |
|--------|------|----------|
| **DEEPSEEK_API_KEY** | AI API 密钥 | [DeepSeek 平台](https://platform.deepseek.com/) 注册并创建 API Key |
| **SMTP_SERVER** | 邮件服务器 | `smtp.qq.com` (QQ邮箱) 或 `smtp.163.com` (163邮箱) |
| **SMTP_USERNAME** | 邮箱账号 | 您的完整邮箱地址 |
| **SMTP_PASSWORD** | 邮箱授权码 | 邮箱设置中开启SMTP并生成授权码（不是登录密码） |
| **EMAIL_FROM** | 发件人邮箱 | 通常与 SMTP_USERNAME 相同 |
| **EMAIL_TO** | 收件人邮箱 | 接收论文分析的邮箱地址 |

## 🔧 三步完成配置

### 步骤 1: 本地测试配置
```bash
# 1. 复制环境变量模板
cp env.example .env

# 2. 编辑 .env 文件，填入上述 6 个配置项
nano .env

# 3. 验证配置
make validate-env
```

### 步骤 2: GitHub Secrets 配置
在 GitHub 仓库中：**Settings** → **Secrets and variables** → **Actions**

添加上述 6 个 Repository secrets（名称和值与 .env 文件相同）

### 步骤 3: 启动自动化
```bash
# 推送代码触发 GitHub Actions
git add .
git commit -m "feat: 配置完成"
git push origin main

# 或手动触发：GitHub Actions 页面 → Daily Paper Analysis → Run workflow
```

## ✅ 验证是否成功

### 本地验证
```bash
# 环境验证（应该全部通过）
make validate-env

# 组件测试
make test-components

# 完整运行测试
make run
```

### GitHub Actions 验证
- 查看 Actions 页面，确保工作流运行成功
- 检查邮箱，应该收到论文分析邮件

## 🎯 预期结果

配置成功后，您将：
- ✅ 每天早上 8:00 自动收到 AI 分析的最新论文邮件
- ✅ 邮件包含精美的 HTML 格式和详细的论文分析
- ✅ 支持多平台自动化运行（Ubuntu/Windows/macOS）
- ✅ 完整的错误处理和通知机制

## 🆘 遇到问题？

### 常见问题
1. **邮件发送失败** → 检查邮箱授权码（不是登录密码）
2. **API 调用失败** → 检查 DeepSeek API 密钥和账户余额
3. **GitHub Actions 失败** → 检查 Secrets 配置是否完整

### 获取帮助
- 运行 `make validate-env` 查看详细错误信息
- 查看 `SECRETS_SETUP_GUIDE.md` 获取详细配置说明
- 查看 `WORKFLOW_SETUP_GUIDE.md` 了解完整工作流

---

**🎉 就这么简单！** 配置完成后，您就拥有了一个全自动的 AI 论文追踪系统！ 