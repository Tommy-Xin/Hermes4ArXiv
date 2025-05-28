# 🚀 DeepSeek AI 配置指南

Hermes4ArXiv 采用 DeepSeek 模型提供高质量、低成本的论文分析服务，专为 GitHub Actions 部署优化。

## 🔧 GitHub Actions快速配置

### 1. 获取 DeepSeek API 密钥

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 进入 **API 管理** 页面
4. 点击 **创建新密钥**
5. 复制生成的 API 密钥（格式：`sk-xxxxxxxx`）

### 2. 在GitHub仓库中配置Secrets

1. 进入您Fork的仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下必需配置：

```bash
# 必需配置
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# 邮件配置（也是必需的）
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_TO=recipient@gmail.com
```

### 3. 可选优化配置

如果需要自定义分析行为，可以添加以下可选配置：

```bash
# 分析配置
ANALYSIS_TYPE=comprehensive        # quick/comprehensive/detailed
MAX_PAPERS=50                     # 论文数量
CATEGORIES=cs.AI,cs.LG,cs.CL     # 研究领域

# 性能优化
ENABLE_PARALLEL=true
MAX_WORKERS=4
```

## 📊 成本预估

DeepSeek 的超低成本让您可以放心使用：

| 论文数量 | 预估成本 | 适用场景 |
|----------|----------|----------|
| 10 篇 | ¥0.10-0.20 | 每日跟踪 |
| 50 篇 | ¥0.50-1.00 | 周报总结 |
| 100 篇 | ¥1.00-2.00 | 月度调研 |

## 🔬 分析类型选择

```bash
# 简洁分析（200-300字）- 节省成本，快速筛选
ANALYSIS_TYPE=quick

# 全面分析（400-600字）- 默认推荐，平衡性价比
ANALYSIS_TYPE=comprehensive

# 详细分析（600-900字）- 深度分析，丰富细节
ANALYSIS_TYPE=detailed
```

## 🛠️ 故障排除

### API 密钥问题

**密钥无效**：
- 检查GitHub Secrets中密钥格式是否以`sk-`开头
- 登录 [DeepSeek平台](https://platform.deepseek.com/) 验证密钥有效性
- 重新生成新密钥并更新GitHub Secrets

**余额不足**：
- 登录 [DeepSeek平台](https://platform.deepseek.com/)
- 查看账户余额和使用统计
- 充值或申请免费额度

### GitHub Actions运行问题

**运行失败**：
1. 检查GitHub Actions页面的运行日志
2. 确认所有必需的Secrets都已正确添加
3. 验证API密钥格式和有效性

**分析质量不满意**：
```bash
# 调整为更详细的分析
ANALYSIS_TYPE=detailed
```

**速度太慢**：
```bash
# 启用并行处理
ENABLE_PARALLEL=true
MAX_WORKERS=6
```

## 📝 最佳实践

### GitHub Actions配置建议

1. **从小开始**: 首次运行建议设置`MAX_PAPERS=10`测试
2. **监控成本**: 在DeepSeek平台查看API使用量
3. **定期更新**: 建议每3-6个月更新API密钥
4. **查看日志**: 在Actions页面监控运行状态和结果

### 推荐配置组合

**日常使用**（推荐新用户）：
```bash
ANALYSIS_TYPE=comprehensive
MAX_PAPERS=30
CATEGORIES=cs.AI,cs.LG,cs.CL
ENABLE_PARALLEL=true
MAX_WORKERS=4
```

**大量筛选**（处理更多论文）：
```bash
ANALYSIS_TYPE=quick
MAX_PAPERS=100
CATEGORIES=cs.AI,cs.LG,cs.CL,cs.CV
ENABLE_PARALLEL=true
MAX_WORKERS=6
```

**深度分析**（重点论文）：
```bash
ANALYSIS_TYPE=detailed
MAX_PAPERS=20
CATEGORIES=cs.AI,cs.LG
ENABLE_PARALLEL=true
MAX_WORKERS=2
```

## 🔗 相关资源

- [DeepSeek 开放平台](https://platform.deepseek.com/)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [高级配置指南](../../ADVANCED_CONFIG.md)
- [Gmail邮箱设置](GMAIL_SETUP_GUIDE.md)

---
