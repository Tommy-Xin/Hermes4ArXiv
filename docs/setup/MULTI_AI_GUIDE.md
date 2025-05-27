# 🤖 多AI分析器使用指南

Hermes4ArXiv现在支持多个AI提供商，提供更强大的分析能力和更高的可靠性。

## 🎯 功能特色

### ✨ 多AI支持
- **DeepSeek**: 高性价比的中文AI模型（默认）
- **OpenAI GPT**: 业界领先的AI模型
- **Claude**: Anthropic的安全可靠AI助手
- **Gemini**: Google的多模态AI模型

### 🔄 智能策略
- **降级策略**: 按顺序尝试，确保分析成功
- **并行策略**: 同时调用多个AI，使用最快结果
- **共识策略**: 多个AI达成共识，提高准确性
- **尽力而为**: 尝试所有策略，最大化成功率

### 📝 优质提示词
- **综合分析**: 400-600字的深度分析
- **快速分析**: 200-300字的简洁分析
- **详细分析**: 600-900字的技术深度分析

## 🚀 快速开始

### 基础配置（仅DeepSeek）
```bash
# 只需配置DeepSeek API密钥
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
```

### 多AI配置
```bash
# 主要AI（必需）
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# 备用AI（可选，提供降级能力）
OPENAI_API_KEY=sk-your-openai-api-key
CLAUDE_API_KEY=sk-ant-your-claude-api-key
GEMINI_API_KEY=your-gemini-api-key

# 分析策略配置
ANALYSIS_STRATEGY=fallback
AI_FALLBACK_ORDER=deepseek,openai,claude,gemini
ANALYSIS_TYPE=comprehensive
```

## 📋 配置详解

### AI分析策略

#### 1. 降级策略（fallback）- 推荐
```bash
ANALYSIS_STRATEGY=fallback
AI_FALLBACK_ORDER=deepseek,openai,claude,gemini
```

**特点**：
- ✅ 按顺序尝试AI，第一个成功即返回
- ✅ 成本最低，优先使用便宜的AI
- ✅ 高可靠性，有多个备选方案
- ✅ 适合日常使用

**使用场景**：日常论文分析，追求稳定性和成本效益

#### 2. 并行策略（parallel）
```bash
ANALYSIS_STRATEGY=parallel
```

**特点**：
- ⚡ 同时调用多个AI，使用最快结果
- 💰 成本较高，会同时消耗多个API
- 🚀 速度最快，适合紧急情况
- 🎯 结果质量高，使用最快响应的AI

**使用场景**：紧急分析，对速度要求高的场景

#### 3. 共识策略（consensus）
```bash
ANALYSIS_STRATEGY=consensus
```

**特点**：
- 🎯 多个AI达成共识，结果更准确
- 💰 成本最高，需要调用多个AI
- 🔬 质量最高，适合重要论文分析
- ⏱️ 速度较慢，需要等待多个AI完成

**使用场景**：重要论文分析，对准确性要求极高的场景

#### 4. 尽力而为（best_effort）
```bash
ANALYSIS_STRATEGY=best_effort
```

**特点**：
- 🛡️ 最高可靠性，尝试所有策略
- 🔄 自动降级，从共识→并行→降级
- 💪 适合网络不稳定的环境
- ⚖️ 平衡成本和质量

**使用场景**：网络不稳定，对成功率要求极高的场景

### 分析类型

#### 综合分析（comprehensive）- 推荐
```bash
ANALYSIS_TYPE=comprehensive
```
- 📊 **长度**: 400-600字
- 🎯 **特点**: 五维度深度分析
- 💡 **适用**: 日常使用，平衡详细度和可读性

#### 快速分析（quick）
```bash
ANALYSIS_TYPE=quick
```
- ⚡ **长度**: 200-300字
- 🎯 **特点**: 简洁精准，突出要点
- 💡 **适用**: 大量论文快速筛选

#### 详细分析（detailed）
```bash
ANALYSIS_TYPE=detailed
```
- 🔬 **长度**: 600-900字
- 🎯 **特点**: 技术深度分析
- 💡 **适用**: 重要论文深度研究

## 🔧 高级配置

### 自定义AI模型
```bash
# 指定具体的AI模型
DEEPSEEK_MODEL=deepseek-chat
OPENAI_MODEL=gpt-4  # 使用GPT-4（成本更高但质量更好）
CLAUDE_MODEL=claude-3-sonnet-20240229  # 使用更强的Claude模型
GEMINI_MODEL=gemini-pro
```

### 自定义降级顺序
```bash
# 优先使用OpenAI，然后是DeepSeek
AI_FALLBACK_ORDER=openai,deepseek,claude,gemini

# 只使用特定的AI
AI_FALLBACK_ORDER=deepseek,openai
```

## 🧪 测试和验证

### 本地测试
```bash
# 测试多AI功能
make test-multi-ai

# 测试组件
make test-components

# 验证环境配置
make validate-env
```

### GitHub Actions测试
1. 在仓库的 `Actions` 页面手动触发工作流
2. 查看日志中的AI分析器信息
3. 检查邮件中的分析质量

## 💰 成本优化建议

### 经济型配置
```bash
# 只使用DeepSeek，成本最低
DEEPSEEK_API_KEY=sk-your-key
ANALYSIS_STRATEGY=fallback
ANALYSIS_TYPE=quick
```

### 平衡型配置（推荐）
```bash
# DeepSeek + OpenAI降级
DEEPSEEK_API_KEY=sk-your-deepseek-key
OPENAI_API_KEY=sk-your-openai-key
ANALYSIS_STRATEGY=fallback
AI_FALLBACK_ORDER=deepseek,openai
ANALYSIS_TYPE=comprehensive
```

### 高质量配置
```bash
# 多AI共识分析
DEEPSEEK_API_KEY=sk-your-deepseek-key
OPENAI_API_KEY=sk-your-openai-key
CLAUDE_API_KEY=sk-your-claude-key
ANALYSIS_STRATEGY=consensus
ANALYSIS_TYPE=detailed
```

## 🔍 故障排除

### 常见问题

#### Q: 多AI功能没有启用？
**A**: 检查以下条件：
- 配置了多个有效的API密钥
- 或者设置了非默认的分析策略
- API密钥长度大于10个字符

#### Q: 分析失败，显示"所有AI提供商都不可用"？
**A**: 可能的原因：
1. **API密钥无效**: 检查密钥格式和有效性
2. **网络问题**: 检查网络连接
3. **API额度不足**: 检查各AI平台的余额
4. **API限制**: 降低调用频率

#### Q: 成本过高？
**A**: 优化建议：
1. 使用 `fallback` 策略而非 `parallel` 或 `consensus`
2. 优先使用成本较低的AI（如DeepSeek）
3. 使用 `quick` 分析类型减少token消耗
4. 减少论文数量或分析频率

#### Q: 分析质量不满意？
**A**: 改进建议：
1. 使用 `detailed` 分析类型
2. 尝试 `consensus` 策略
3. 使用更强的AI模型（如GPT-4、Claude Sonnet）
4. 调整降级顺序，优先使用质量更高的AI

### 调试技巧

#### 查看分析器状态
```bash
# 运行测试脚本查看详细信息
cd src && python test_multi_ai.py
```

#### 检查日志
```bash
# 查看GitHub Actions日志
# 搜索关键词：AI分析器、多AI、分析策略
```

## 📚 API密钥获取

### DeepSeek
1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 进入API管理页面
4. 创建新的API密钥

### OpenAI
1. 访问 [OpenAI平台](https://platform.openai.com/)
2. 注册并登录账号
3. 进入API Keys页面
4. 创建新的API密钥

### Claude
1. 访问 [Anthropic控制台](https://console.anthropic.com/)
2. 注册并登录账号
3. 进入API Keys页面
4. 创建新的API密钥

### Gemini
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用Google账号登录
3. 创建新的API密钥

## 🎉 最佳实践

1. **渐进式配置**: 先配置DeepSeek，确保基本功能正常，再添加其他AI
2. **成本控制**: 使用降级策略，优先使用成本较低的AI
3. **质量优化**: 对重要论文使用详细分析或共识策略
4. **监控使用**: 定期检查各AI平台的使用量和余额
5. **备份方案**: 至少配置2个AI提供商，确保服务可用性

---

🤖 **愿多AI的智慧，为您带来更精准的学术洞察！** 