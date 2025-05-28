# 🎯 用户自定义模型配置指南

Hermes4ArXiv支持灵活的AI模型配置，让您可以精确控制使用哪些AI模型进行论文分析。

## 🚀 配置方式

### 方式1: 指定首选模型（推荐）

为每个AI提供商指定首选模型：

```bash
# OpenAI模型（2025年最新）
PREFERRED_OPENAI_MODEL=o4-mini        # 最新推理模型
# PREFERRED_OPENAI_MODEL=o3           # 强大推理模型
# PREFERRED_OPENAI_MODEL=o3-mini      # 高效推理模型

# Claude模型（2025年5月发布）
PREFERRED_CLAUDE_MODEL=claude-4-opus-20250514    # 世界最佳编程模型
# PREFERRED_CLAUDE_MODEL=claude-4-sonnet-20250514 # 平衡性能和效率

# Gemini模型
PREFERRED_GEMINI_MODEL=gemini-2.5-pro-preview-05-06  # 最新SOTA
# PREFERRED_GEMINI_MODEL=gemini-2.0-flash-exp         # 快速响应

# DeepSeek模型
PREFERRED_DEEPSEEK_MODEL=deepseek-chat    # 通用对话
# PREFERRED_DEEPSEEK_MODEL=deepseek-coder # 编程专用
```

### 方式2: 定义可用模型列表

指定每个提供商的可用模型列表（逗号分隔）：

```bash
# OpenAI可用模型
CUSTOM_OPENAI_MODELS=o4-mini,o3,o3-mini,o1-preview,gpt-4-turbo,gpt-4o

# Claude可用模型
CUSTOM_CLAUDE_MODELS=claude-4-opus-20250514,claude-4-sonnet-20250514,claude-3-5-sonnet-20241022

# Gemini可用模型
CUSTOM_GEMINI_MODELS=gemini-2.5-pro-preview-05-06,gemini-2.0-flash-exp,gemini-1.5-pro

# DeepSeek可用模型
CUSTOM_DEEPSEEK_MODELS=deepseek-chat,deepseek-coder,deepseek-reasoner
```

### 方式3: 指定唯一AI（最高优先级）

只使用特定的AI提供商：

```bash
PREFERRED_AI_MODEL=gemini  # 只使用Gemini
# 可选值：deepseek, openai, claude, gemini
```

## 🎯 配置优先级

系统按以下优先级选择模型：

1. **PREFERRED_AI_MODEL** - 指定唯一使用的AI
2. **PREFERRED_XXX_MODEL** - 各提供商的首选模型
3. **XXX_MODEL** - 基础模型配置
4. **默认SOTA模型** - 系统预设的最强模型

## 📊 推荐配置

### 🏆 SOTA性能优先
```bash
PREFERRED_OPENAI_MODEL=o4-mini
PREFERRED_CLAUDE_MODEL=claude-4-opus-20250514
PREFERRED_GEMINI_MODEL=gemini-2.5-pro-preview-05-06
AI_FALLBACK_ORDER=gemini,claude,openai,deepseek
```

### 💰 成本优化配置
```bash
PREFERRED_AI_MODEL=deepseek
PREFERRED_DEEPSEEK_MODEL=deepseek-chat
```

### ⚡ 速度优先配置
```bash
PREFERRED_CLAUDE_MODEL=claude-4-sonnet-20250514
PREFERRED_GEMINI_MODEL=gemini-2.0-flash-exp
AI_FALLBACK_ORDER=claude,gemini,deepseek
```

### 🛡️ 稳定性优先配置
```bash
PREFERRED_OPENAI_MODEL=o3
PREFERRED_DEEPSEEK_MODEL=deepseek-chat
AI_FALLBACK_ORDER=deepseek,openai,claude,gemini
```

## 🔍 模型特性对比

| 模型系列 | 优势 | 适用场景 |
|---------|------|----------|
| **Claude 4 Opus** | 世界最佳编程模型，SWE-bench 72.5% | 复杂代码分析、技术论文 |
| **OpenAI o4-mini** | 最新推理模型，高效快速 | 数学推理、逻辑分析 |
| **OpenAI o3** | 强大推理，ARC-AGI 87.5% | 复杂推理任务 |
| **Gemini 2.5 Pro** | 最新SOTA，多模态强 | 综合分析、创新论文 |
| **DeepSeek Chat** | 高性价比，稳定可靠 | 日常分析、保底方案 |

## 🚨 注意事项

1. **API密钥要求**: 必须配置对应的API密钥才能使用相应模型
2. **模型可用性**: 某些模型可能需要特殊权限或地区限制
3. **成本考虑**: 不同模型的成本差异较大，请合理配置
4. **失败回退**: 系统会自动回退到可用的其他模型

## 🔧 调试模式

查看当前使用的模型配置：

```bash
# 查看日志中的模型信息
tail -f src/storage/logs/latest.log | grep "🤖"
```

系统会显示类似信息：
```
🤖 gemini: gemini-2.5-pro-preview-05-06
🤖 claude: claude-4-opus-20250514
🤖 openai: o3
🤖 deepseek: deepseek-chat
```

---

💡 **提示**: 建议先使用默认配置测试，然后根据需要逐步调整模型选择。 