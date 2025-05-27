# Hermes4ArXiv - 5分钟自动部署指南

🏛️ **赫尔墨斯智慧信使** - 完全自动化的ArXiv论文追踪器

## 🚀 一键部署（5分钟搞定）

### 第1步：Fork仓库
点击右上角的 **Fork** 按钮，将项目复制到您的GitHub账号

### 第2步：配置Secrets
在您的Fork仓库中，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下配置：

#### 🤖 AI模型（四选一即可）
```
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here    # 💰 高性价比首选
CLAUDE_API_KEY=sk-ant-your-claude-key-here        # 🏆 最强推理模型
GEMINI_API_KEY=your-gemini-key-here               # 🔬 Google最新SOTA
OPENAI_API_KEY=sk-your-openai-key-here            # 🧠 推理能力王者
```

#### 📧 邮件配置（必需）
```
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com  
SMTP_PASSWORD=your-app-password
EMAIL_TO=your-email@gmail.com
```

#### 可选配置（有默认值）
```
CATEGORIES=cs.AI,cs.LG,cs.CL    # 论文类别
MAX_PAPERS=50                   # 每日最大论文数
SEARCH_DAYS=2                   # 搜索最近几天
```

### 第3步：启动自动化
- 配置完成后，GitHub Actions会每天自动运行
- 也可以在 `Actions` 页面手动触发测试

## 📧 Gmail快速配置

1. **启用两步验证**：[Google账户安全设置](https://myaccount.google.com/security)
2. **生成应用密码**：搜索"应用专用密码" → 选择"邮件" → 生成16位密码
3. **使用应用密码**：将生成的密码填入 `SMTP_PASSWORD`

## 🎯 就这么简单！

- ✅ **零服务器成本**：完全基于GitHub Actions
- ✅ **智能AI切换**：配置多个AI时自动降级，确保成功率
- ✅ **自动运行**：每天北京时间8点自动分析
- ✅ **邮件推送**：HTML邮件直达您的邮箱


## 🔧 高级配置（可选）

如需自定义更多选项，可在Secrets中添加：
- `PREFERRED_AI_MODEL`: 指定优先使用的AI（deepseek/claude/gemini/openai）
- `AI_FALLBACK_ORDER`: 自定义AI降级顺序（默认：deepseek,openai,claude,gemini）
- `EMAIL_FROM`: 发件人邮箱（默认同SMTP_USERNAME）
- `ENABLE_PARALLEL`: 是否启用并行处理（默认true）

## 🆘 遇到问题？

1. **邮件发送失败**：检查Gmail应用密码是否正确
2. **AI分析失败**：配置多个AI密钥可提高成功率
3. **没有收到邮件**：检查垃圾邮件文件夹

---

**🏛️ 愿赫尔墨斯的智慧，每日为您带来学术前沿的启迪！** 