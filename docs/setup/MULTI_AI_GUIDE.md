# 🤖 智能AI回退系统使用指南

Hermes4ArXiv采用智能AI回退系统，确保论文分析的高可靠性。您可以配置一个主要AI和多个备用AI，当主要AI失败时自动切换到备用AI。

## 🎯 核心概念

### ✨ 智能回退策略
- **主要AI**: 您首选的AI模型（如Gemini 2.5 Pro Preview）
- **备用AI**: 当主要AI失败时自动使用的备选方案
- **自动切换**: 系统智能检测失败并自动回退
- **单次分析**: 每篇论文只使用一个AI分析，不重复调用

### 🔄 工作原理
1. 系统首先使用您配置的主要AI
2. 如果主要AI失败（网络问题、API限制、安全过滤器等）
3. 自动切换到第一个备用AI
4. 如果仍然失败，继续尝试下一个备用AI
5. 直到成功或所有AI都尝试完毕

## 🚀 推荐配置

### 方案一：Gemini主要 + DeepSeek备用（推荐）
```bash
# 主要AI：Gemini 2.5 Pro Preview（最新SOTA模型）
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-pro-preview-05-06

# 备用AI：DeepSeek（高性价比备选）
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# AI使用顺序（主要→备用）
AI_FALLBACK_ORDER=gemini,deepseek

# 分析配置
ANALYSIS_TYPE=comprehensive
```

### 方案二：Claude主要 + DeepSeek备用
```bash
# 主要AI：Claude 3.5 Sonnet（推理能力强）
CLAUDE_API_KEY=sk-ant-your-claude-api-key
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# 备用AI：DeepSeek
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# AI使用顺序
AI_FALLBACK_ORDER=claude,deepseek
```

### 方案三：仅使用单一AI（经济型）
```bash
# 只配置一个AI，无备用方案
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
```

## 📋 配置详解

### 环境变量说明

#### AI API密钥（选择配置）
```bash
# Gemini API（Google AI Studio获取）
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-pro-preview-05-06  # 可选，默认使用此模型

# Claude API（Anthropic Console获取）
CLAUDE_API_KEY=sk-ant-your-claude-api-key
CLAUDE_MODEL=claude-3-5-sonnet-20241022    # 可选

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview           # 可选

# DeepSeek API（高性价比选择）
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_MODEL=deepseek-chat               # 可选
```

#### 回退策略配置
```bash
# AI使用顺序（从左到右尝试）
AI_FALLBACK_ORDER=gemini,deepseek,claude,openai

# 单一AI使用（不想要备用AI）
PREFERRED_AI_MODEL=gemini  # 只使用指定的AI
```

#### 分析类型
```bash
# comprehensive: 400-600字全面分析（推荐）
# quick: 200-300字快速分析
# detailed: 600-900字详细分析
ANALYSIS_TYPE=comprehensive
```

## 🛡️ 失败处理机制

### 智能失败检测
- **API错误**: 自动重试3次，失败后切换到备用AI
- **安全过滤器**: Gemini安全过滤器触发时立即切换到备用AI
- **网络超时**: 30秒超时后自动切换
- **配额限制**: API配额耗尽时切换到备用AI

### 临时禁用机制
- AI连续失败3次后临时禁用5分钟
- 其他AI正常时，被禁用的AI会自动恢复
- 防止在故障AI上浪费时间

## 💰 成本考虑

### 推荐搭配（性价比最优）
```bash
# 主要使用高性价比的DeepSeek
DEEPSEEK_API_KEY=sk-your-key
AI_FALLBACK_ORDER=deepseek

# 成本：约￥0.01-0.02/篇论文
```

### 质量优先搭配
```bash
# 主要使用SOTA模型，DeepSeek作备用
GEMINI_API_KEY=your-gemini-key
DEEPSEEK_API_KEY=sk-your-deepseek-key  
AI_FALLBACK_ORDER=gemini,deepseek

# 大部分时候使用Gemini，失败时用DeepSeek保底
```

### 极致可靠性搭配
```bash
# 配置多个备用AI
CLAUDE_API_KEY=sk-ant-your-claude-key
GEMINI_API_KEY=your-gemini-key
DEEPSEEK_API_KEY=sk-your-deepseek-key
AI_FALLBACK_ORDER=claude,gemini,deepseek

# 三重保险，确保分析成功
```

## 🔍 故障排除

### 常见问题

#### Q: 为什么Gemini一直失败？
**A**: 可能的原因：
1. **安全过滤器拦截**: 这是常见问题，系统会自动切换到备用AI
2. **地理位置限制**: 本地测试可能有限制，GitHub Actions中正常
3. **API密钥问题**: 检查密钥是否正确
4. **模型不可用**: 某些Preview模型可能暂时不可用

#### Q: 如何确保至少有一个AI可用？
**A**: 建议配置：
```bash
# 至少配置DeepSeek作为保底
DEEPSEEK_API_KEY=sk-your-key
# 再配置你想要的主要AI
GEMINI_API_KEY=your-key
AI_FALLBACK_ORDER=gemini,deepseek
```

#### Q: 如何只使用特定的AI，不要回退？
**A**: 使用PREFERRED_AI_MODEL：
```bash
GEMINI_API_KEY=your-key
PREFERRED_AI_MODEL=gemini  # 只使用Gemini，失败就失败
```

#### Q: 回退是否会影响分析质量？
**A**: 不会：
- 每个AI都使用相同的分析提示词
- 备用AI（如DeepSeek）质量也很高
- 系统只是确保分析能够完成

### 调试技巧

#### 查看AI使用情况
```bash
# 在GitHub Actions日志中搜索：
# "✅ 配置验证通过！已配置的AI模型"
# "使用 gemini 分析论文"
# "✅ gemini 分析成功"
```

#### 测试AI连接
```bash
# 本地测试（在项目根目录）
cd scripts && python validate_env.py
```

## 📚 API密钥获取

### Gemini API（推荐主要AI）
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用Google账号登录
3. 创建新的API密钥
4. **注意**: Gemini 2.5 Pro Preview可能有地理限制

### DeepSeek API（推荐备用AI）
1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 进入API管理页面
4. 创建新的API密钥
5. **优势**: 性价比高，地理限制少

### Claude API
1. 访问 [Anthropic控制台](https://console.anthropic.com/)
2. 注册并登录账号
3. 进入API Keys页面
4. 创建新的API密钥

### OpenAI API
1. 访问 [OpenAI平台](https://platform.openai.com/)
2. 注册并登录账号
3. 进入API Keys页面
4. 创建新的API密钥

## 🎉 最佳实践

1. **双AI策略**: 配置一个主要AI + DeepSeek作备用
2. **成本控制**: 主要使用DeepSeek，特殊需求时使用高端AI
3. **可靠性优先**: 至少配置两个不同提供商的AI
4. **监控使用**: 定期检查API使用量和成本
5. **GitHub Actions测试**: 本地可能有地理限制，以GitHub Actions结果为准

---

🤖 **一个主要AI + 智能回退，让您的论文分析更可靠！** 