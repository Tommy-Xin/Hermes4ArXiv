# 🏆 SOTA模型单一配置指南

Hermes4ArXiv支持当前最先进的AI模型，采用单模型策略确保科研质量。根据您配置的API密钥自动选择使用的模型。

## 🎯 支持的SOTA模型（2025年5月最新）

### 🥇 Claude Opus 4 - 世界最强推理模型
- **模型**：`claude-opus-4-20250514`
- **特点**：世界最强编程能力，持续7小时工作，扩展思考
- **适用**：复杂的学术论文分析，高质量要求
- **配置**：`CLAUDE_API_KEY=your-key`

### 🥈 Gemini 2.5 Pro Preview - Google最新SOTA
- **模型**：`gemini-2.5-pro-preview-05-06`
- **特点**：最新发布，多模态理解巅峰，超长上下文
- **适用**：包含图表、公式的复杂论文分析
- **配置**：`GEMINI_API_KEY=your-key`

### 🥉 OpenAI o3 - 推理能力王者
- **模型**：`o3-2025-04-16`
- **特点**：史上最强推理能力，复杂问题解决专家
- **适用**：需要深度逻辑推理的论文分析
- **配置**：`OPENAI_API_KEY=your-key`

### 💰 DeepSeek R1 - 高性价比SOTA
- **模型**：`deepseek-r1`
- **特点**：推理能力强，成本极低，中文友好
- **适用**：大量论文的高质量批量分析
- **配置**：`DEEPSEEK_API_KEY=your-key`

## 🚀 单模型配置策略

系统会根据您配置的API密钥自动选择使用的模型，**只需要配置一个API密钥即可**。

### 🏆 Claude Opus 4 配置（推荐）
```bash
# 只需配置Claude API
CLAUDE_API_KEY=sk-ant-your-claude-api-key
CLAUDE_MODEL=claude-opus-4-20250514

# 基本设置
MAX_PAPERS=10
SEARCH_DAYS=2
ANALYSIS_TYPE=comprehensive
```

### 🔬 Gemini 2.5 Pro 配置
```bash
# 只需配置Gemini API  
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-pro-preview-05-06

# 基本设置
MAX_PAPERS=10
SEARCH_DAYS=2
ANALYSIS_TYPE=comprehensive
```

### 🧠 OpenAI o3 配置
```bash
# 只需配置OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=o3-2025-04-16

# 基本设置
MAX_PAPERS=10
SEARCH_DAYS=2
ANALYSIS_TYPE=comprehensive
```

### 💰 DeepSeek R1 配置（经济型）
```bash
# 只需配置DeepSeek API
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_MODEL=deepseek-r1

# 可以处理更多论文（成本低）
MAX_PAPERS=20
SEARCH_DAYS=2
ANALYSIS_TYPE=comprehensive
```

## 📊 SOTA模型对比

| 模型 | 学术质量 | 推理能力 | 速度 | 成本 | 推荐场景 |
|------|----------|----------|------|------|----------|
| Claude Opus 4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 🏆 高质量科研分析 |
| Gemini 2.5 Pro | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | 🔬 多模态论文分析 |
| OpenAI o3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | 🧠 复杂推理任务 |
| DeepSeek R1 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 高性价比批量分析 |

## 🧪 测试和验证

### 快速测试
```bash
# 运行组件测试
uv run src/tests/test_components.py

# 测试少量论文（经济模式）
uv run src/main.py --max-papers 3 --search-days 1
```

## 💡 最佳实践

### 💰 成本控制建议
1. **使用DeepSeek R1**：性价比最高的选择
2. **限制论文数量**：设置`MAX_PAPERS=5-10`控制成本
3. **缩短搜索周期**：设置`SEARCH_DAYS=1`减少API调用
4. **监控API使用量**：定期检查账单，避免超支

### ⚡ 性能优化
1. **单模型策略**：避免多模型降级的复杂性
2. **合理设置并发**：根据API限制调整`MAX_WORKERS`
3. **使用批处理**：大量论文时启用`BATCH_SIZE=10`

### 🔧 日常维护
1. **定期更新API密钥**：确保服务不中断
2. **检查模型版本**：关注提供商的模型更新
3. **备份配置文件**：保存有效的环境变量配置

---

💰 **经济实用的AI论文分析解决方案！** 