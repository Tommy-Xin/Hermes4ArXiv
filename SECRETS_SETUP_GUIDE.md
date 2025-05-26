# 🔐 GitHub Secrets 配置指南

## 必需的 GitHub Secrets

在您的 GitHub 仓库中，进入 **Settings** → **Secrets and variables** → **Actions**，添加以下密钥：

### 1. AI API 配置

#### DEEPSEEK_API_KEY (必需)
- **描述**: DeepSeek AI API 密钥
- **获取方式**: 
  1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
  2. 注册账号并登录
  3. 进入 API Keys 页面
  4. 创建新的 API Key
- **格式**: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **注意**: 确保账户有足够余额

### 2. 邮件服务配置

#### SMTP_SERVER (必需)
- **描述**: SMTP 服务器地址
- **常用值**:
  - QQ邮箱: `smtp.qq.com`
  - 163邮箱: `smtp.163.com`
  - Gmail: `smtp.gmail.com`
  - Outlook: `smtp-mail.outlook.com`

#### SMTP_PORT (可选，默认587)
- **描述**: SMTP 服务器端口
- **常用值**: `587` (TLS) 或 `465` (SSL)

#### SMTP_USERNAME (必需)
- **描述**: 邮箱账号
- **格式**: `your-email@example.com`

#### SMTP_PASSWORD (必需)
- **描述**: 邮箱授权码（不是登录密码）
- **获取方式**:
  - **QQ邮箱**: 设置 → 账户 → POP3/IMAP/SMTP → 开启服务 → 生成授权码
  - **163邮箱**: 设置 → POP3/SMTP/IMAP → 开启服务 → 设置客户端授权密码
  - **Gmail**: 开启两步验证 → 应用专用密码
- **格式**: 通常是16位字符串

#### EMAIL_FROM (必需)
- **描述**: 发件人邮箱
- **格式**: `your-email@example.com`
- **注意**: 通常与 SMTP_USERNAME 相同

#### EMAIL_TO (必需)
- **描述**: 收件人邮箱列表
- **格式**: 
  - 单个邮箱: `recipient@example.com`
  - 多个邮箱: `user1@example.com,user2@example.com,user3@example.com`

## 📋 配置检查清单

- [ ] DEEPSEEK_API_KEY - DeepSeek API 密钥
- [ ] SMTP_SERVER - SMTP 服务器地址
- [ ] SMTP_USERNAME - 邮箱账号
- [ ] SMTP_PASSWORD - 邮箱授权码
- [ ] EMAIL_FROM - 发件人邮箱
- [ ] EMAIL_TO - 收件人邮箱

## 🔧 本地测试配置

### 1. 创建 .env 文件
```bash
# 复制环境变量模板
cp env.example .env
```

### 2. 编辑 .env 文件
```bash
# AI API 配置
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# 邮件配置
SMTP_SERVER=smtp.qq.com
SMTP_PORT=587
SMTP_USERNAME=your-email@qq.com
SMTP_PASSWORD=your-authorization-code
EMAIL_FROM=your-email@qq.com
EMAIL_TO=recipient1@example.com,recipient2@example.com
```

### 3. 验证配置
```bash
# 运行环境验证脚本
uv run scripts/validate_env.py

# 或使用 Makefile
make validate-env
```

## 🚨 安全注意事项

1. **永远不要**将真实的 API 密钥提交到代码仓库
2. **确保** .env 文件在 .gitignore 中
3. **定期轮换** API 密钥和邮箱授权码
4. **使用最小权限**原则配置邮箱授权
5. **监控** API 使用量和费用

## 🔍 常见问题

### Q: DeepSeek API 调用失败
- 检查 API 密钥是否正确
- 确认账户余额充足
- 验证网络连接

### Q: 邮件发送失败
- 确认使用授权码而非登录密码
- 检查 SMTP 服务器和端口设置
- 验证邮箱服务商的 SMTP 设置

### Q: GitHub Actions 运行失败
- 检查所有必需的 Secrets 是否已配置
- 查看 Actions 日志中的具体错误信息
- 确认 Secrets 名称拼写正确

## 📞 获取帮助

如果遇到配置问题，可以：
1. 查看项目的 Issues 页面
2. 运行 `make help` 查看可用命令
3. 使用 `make validate-env` 检查配置 