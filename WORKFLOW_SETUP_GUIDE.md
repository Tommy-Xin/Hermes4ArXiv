# 🚀 ArXiv 论文追踪器 - 完整工作流设置指南

## 📋 配置清单

### 1. 必需的密钥信息

您需要准备以下信息：

#### 🤖 AI API 配置
- **DeepSeek API Key**: 访问 [DeepSeek 平台](https://platform.deepseek.com/) 获取
  - 注册账号并充值（建议至少 $5）
  - 创建 API Key，格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### 📧 邮件服务配置
- **邮箱服务商**: 推荐使用 QQ 邮箱或 163 邮箱
- **SMTP 设置**: 
  - QQ 邮箱: `smtp.qq.com:587`
  - 163 邮箱: `smtp.163.com:587`
  - Gmail: `smtp.gmail.com:587`
- **授权码**: 在邮箱设置中开启 SMTP 服务并生成授权码

## 🔧 本地开发设置

### 步骤 1: 环境准备
```bash
# 1. 克隆仓库
git clone https://github.com/your-username/arxiv_paper_tracker.git
cd arxiv_paper_tracker

# 2. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 安装依赖
make install-dev
```

### 步骤 2: 配置环境变量
```bash
# 1. 复制环境变量模板
cp env.example .env

# 2. 编辑 .env 文件，填入真实值
nano .env  # 或使用您喜欢的编辑器
```

### 步骤 3: 验证配置
```bash
# 运行环境验证脚本
make validate-env

# 如果验证通过，运行组件测试
make test-components

# 运行完整测试套件
make test
```

### 步骤 4: 本地测试运行
```bash
# 运行主程序（完整流程）
make run

# 或者快速分析（少量论文）
make quick-analysis
```

## 🔐 GitHub Secrets 配置

### 步骤 1: 在 GitHub 仓库中配置 Secrets

进入您的 GitHub 仓库：**Settings** → **Secrets and variables** → **Actions**

添加以下 Repository secrets：

| Secret 名称 | 描述 | 示例值 |
|------------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek AI API 密钥 | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `SMTP_SERVER` | SMTP 服务器地址 | `smtp.qq.com` |
| `SMTP_USERNAME` | 邮箱账号 | `your-email@qq.com` |
| `SMTP_PASSWORD` | 邮箱授权码 | `abcdefghijklmnop` |
| `EMAIL_FROM` | 发件人邮箱 | `your-email@qq.com` |
| `EMAIL_TO` | 收件人邮箱 | `recipient@example.com` |

### 步骤 2: 使用 GitHub CLI 快速配置（可选）
```bash
# 安装 GitHub CLI
# 然后运行以下命令（替换为您的真实值）

gh secret set DEEPSEEK_API_KEY --body "sk-your-api-key"
gh secret set SMTP_SERVER --body "smtp.qq.com"
gh secret set SMTP_USERNAME --body "your-email@qq.com"
gh secret set SMTP_PASSWORD --body "your-authorization-code"
gh secret set EMAIL_FROM --body "your-email@qq.com"
gh secret set EMAIL_TO --body "recipient@example.com"
```

## 🔄 GitHub Actions 工作流

### 当前可用的工作流

1. **daily_paper_analysis.yml**: 每日自动论文分析
   - 触发时间: 每天早上 8:00 (北京时间)
   - 手动触发: 支持
   
2. **test.yml**: 多平台测试矩阵
   - 触发条件: Push 和 Pull Request
   - 平台: Ubuntu, Windows, macOS
   - Python 版本: 3.10, 3.11, 3.12

3. **quality.yml**: 代码质量检查
   - 代码格式检查
   - 类型检查
   - 安全检查

### 手动触发工作流
1. 进入 GitHub 仓库的 **Actions** 页面
2. 选择 **Daily Paper Analysis** 工作流
3. 点击 **Run workflow** 按钮
4. 选择分支并点击 **Run workflow**

## 📊 监控和维护

### 查看运行状态
- **GitHub Actions**: 在 Actions 页面查看工作流运行状态
- **邮件通知**: 成功时收到论文分析邮件，失败时收到错误通知
- **日志文件**: 在仓库的 `src/logs/` 目录查看详细日志

### 常见问题排查

#### 1. 工作流运行失败
```bash
# 检查 Secrets 配置
gh secret list

# 查看工作流日志
# 在 GitHub Actions 页面点击失败的运行查看详细日志
```

#### 2. 邮件发送失败
- 检查邮箱授权码是否正确
- 确认 SMTP 服务器设置
- 验证网络连接

#### 3. API 调用失败
- 检查 DeepSeek API 密钥
- 确认账户余额充足
- 查看 API 使用限制

### 性能监控
```bash
# 查看项目状态
make status

# 运行性能基准测试
make benchmark

# 查看缓存使用情况
make cache-info
```

## 🔄 日常使用流程

### 自动化运行（推荐）
1. 配置完成后，系统每天自动运行
2. 每天早上 8:00 收到论文分析邮件
3. 定期检查 GitHub Actions 运行状态

### 手动运行
```bash
# 本地测试新功能
make test-components
make run

# 推送到 GitHub 触发自动化
git add .
git commit -m "feat: 添加新功能"
git push origin main

# 手动触发 GitHub Actions
# 在 GitHub 网页界面操作
```

### 配置调整
```bash
# 修改搜索参数（在 src/config.py 中）
# 或通过环境变量覆盖：
export MAX_PAPERS=30
export SEARCH_DAYS=3

# 重新验证配置
make validate-env
```

## 🚨 安全最佳实践

1. **密钥管理**
   - 永远不要将真实密钥提交到代码仓库
   - 定期轮换 API 密钥和邮箱授权码
   - 使用最小权限原则

2. **监控使用**
   - 定期检查 API 使用量和费用
   - 监控邮件发送频率
   - 关注异常活动

3. **备份配置**
   - 记录重要配置信息（不包括密钥）
   - 定期备份自定义设置
   - 文档化特殊配置

## 📈 扩展功能

### 启用多 AI 支持
```bash
# 设置多 AI API 支持
make setup-multi-ai

# 添加其他 AI 提供商的 API 密钥
gh secret set OPENAI_API_KEY --body "sk-your-openai-key"
gh secret set CLAUDE_API_KEY --body "sk-your-claude-key"
```

### 启用 Web 界面
```bash
# 设置 Web 开发环境
make setup-web-dev

# 部署 Web 界面
make deploy-web
```

### 数据库集成
```bash
# 设置数据库支持
make setup-database

# 配置数据库连接
gh secret set DATABASE_URL --body "postgresql://user:pass@host:port/db"
```

## 🆘 获取帮助

### 文档资源
- **配置指南**: `SECRETS_SETUP_GUIDE.md`
- **扩展路线图**: `EXTENSION_ROADMAP.md`
- **部署指南**: `DEPLOYMENT_GUIDE.md`

### 命令帮助
```bash
# 查看所有可用命令
make help

# 验证环境配置
make validate-env

# 查看项目状态
make status
```

### 问题反馈
- 查看项目 Issues 页面
- 提交新的 Issue 描述问题
- 参考故障排除文档

---

**🎉 恭喜！** 按照以上步骤完成配置后，您的 ArXiv 论文追踪器就可以正常运行了！ 