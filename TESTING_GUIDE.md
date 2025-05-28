# 🧪 测试指南

## 🚀 快速测试部署

### 1. Fork 仓库测试
```bash
# 1. Fork本仓库到您的GitHub账号
# 2. 克隆Fork的仓库到本地（可选）
git clone https://github.com/YOUR_USERNAME/arxiv_paper_tracker.git
```

### 2. 配置GitHub Secrets
进入Fork的仓库 **Settings** → **Secrets and variables** → **Actions**，添加：

```bash
# 必需配置
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
SMTP_USERNAME=your-email@gmail.com  
SMTP_PASSWORD=your-app-password
EMAIL_TO=recipient@gmail.com

# 可选优化配置（用于自定义）
ANALYSIS_TYPE=comprehensive
MAX_PAPERS=10  # 测试建议使用小数量
CATEGORIES=cs.AI,cs.LG,cs.CL
```

### 3. 手动触发测试
1. 进入 **Actions** 页面
2. 选择 **Daily Paper Analysis**
3. 点击 **Run workflow**
4. 等待运行完成（约5-10分钟）

### 4. 验证结果
- ✅ 检查Actions运行日志无错误
- ✅ 检查邮箱收到分析报告
- ✅ 报告包含AI分析的论文列表

## 🔧 本地配置测试（可选）

### 1. 使用配置助手
```bash
# 安装依赖
make install

# 运行配置助手
make configure

# 验证环境配置
make validate-env
```

### 2. 检查核心功能
```bash
# 查看可用命令
make help

# 清理缓存
make clean
```

## 🎯 测试重点

### ✅ 必须通过的测试
1. **GitHub Actions工作流正常运行**
2. **DeepSeek API调用成功**  
3. **邮件发送成功**
4. **论文分析结果合理**

### 🔍 预期改进
1. **部署过程** - 从复杂的多步骤简化为3分钟配置
2. **文档体验** - README清晰直接，高级配置分离
3. **错误处理** - 失败时日志信息明确
4. **成本控制** - DeepSeek API成本极低

## 📊 测试场景

### 场景1：新用户首次部署
- 按照README快速开始部分操作
- 预期：3分钟内完成配置，首次运行成功

### 场景2：自定义配置
- 使用ADVANCED_CONFIG.md中的配置选项
- 预期：可以灵活调整论文数量和分析类型

### 场景3：错误处理
- 故意配置错误的API密钥
- 预期：Actions失败时日志信息清晰

## 🐛 常见问题测试

1. **API密钥问题** - 检查错误信息是否清晰
2. **邮件发送失败** - 检查SMTP配置提示
3. **论文数量过多** - 检查是否有合理的限制和提示

---

**测试完成后，请在Issues中反馈结果！** 🎉 