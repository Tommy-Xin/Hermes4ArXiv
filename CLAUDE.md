# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Hermes4ArXiv 是一个基于 GitHub Actions 的自动化工具，每日追踪和分析 ArXiv 最新论文，通过邮件发送分析报告。

**核心工作流程**：ArXiv 论文获取 → 双阶段分析（排名 + 深度分析）→ HTML 报告生成 → 邮件发送

## 开发命令

### 基础命令

```bash
# 安装依赖
make install
# 或直接使用：
uv sync

# 运行主程序（完整分析流程）
make run
# 或直接使用：
cd src && uv run python main.py

# 验证环境变量配置
make validate-env
# 或直接使用：
uv run scripts/validate_env.py

# 交互式配置助手
make configure
# 或直接使用：
uv run scripts/configure_analysis.py
```

### 维护命令

```bash
# 更新依赖
make update-deps

# 清理临时文件
make clean

# 查看依赖树
make show-deps

# 缓存管理
make cache-info
make clean-cache
```

### 测试

测试基础设施已配置，但测试用例需要实现：
```bash
# 运行测试（当测试编写完成后）
uv run pytest

# 测试文件应放在：
# src/tests/test_*.py
```

## 核心架构

### 双阶段分析流程

系统采用两阶段分析流程，在 `src/ai/batch_coordinator.py` 中实现：

**第一阶段：滑动窗口排名** (`_run_stage1_ranking`)
- 论文按重叠窗口处理（默认：每窗口10篇，步长5篇）
- 每个窗口调用 `DeepSeekAnalyzer.rank_papers_in_batch()` 进行排名
- 出现在多个窗口的论文会聚合分数（取最高分）
- 输出：按 `stage1_score` 排序的论文列表

**第二阶段：深度分析** (`_run_stage2_deep_analysis`)
1. 筛选高于阈值的论文（默认：≥3.5分）
2. 限制为前N篇（默认：20篇）以控制成本
3. **并行全文提取**：使用 ThreadPoolExecutor 下载并提取 PDF 文本
4. 对全文进行批量深度分析 `DeepSeekAnalyzer.analyze_papers_batch()`
5. 解析结果并附加 `analysis` 和 `html_analysis` 到论文字典

**配置项**：`config.yml` 中的 `STAGE_ANALYSIS` 部分。设置 `ENABLED: false` 可使用旧版直接批量分析。

### 核心组件

**`src/main.py`** - 主入口和流程编排
- `ArxivPaperTracker` 类协调整个流程
- 初始化所有组件（ArxivClient、DeepSeekAnalyzer、BatchCoordinator、EmailSender）
- 执行工作流：获取 → 分析 → 格式化 → 发送邮件
- 错误通知通过邮件发送

**`src/config.py`** - 配置管理
- 从 `config.yml` 和环境变量加载（环境变量优先级更高）
- 处理类型转换（CATEGORIES/EMAIL_TO 为列表，数值类型，布尔值）
- 管理存储目录路径
- `validate()` 方法检查必需配置

**`src/data/arxiv_client.py`** - ArXiv API 集成
- 使用 `arxiv` Python 库获取论文
- `get_full_text()` 方法：下载 PDF 并使用 PyMuPDF 提取文本
- 可配置搜索类别、日期范围和最大论文数

**`src/ai/analyzer.py`** - AI 模型抽象层 (`DeepSeekAnalyzer`)
- **多提供商支持**：自动检测并使用智谱GLM（优先）或 DeepSeek
- **提供商差异处理**：GLM 不支持 `response_format` 和 `timeout` 参数
- 三个分析方法：
  - `rank_papers_in_batch()`: 第一阶段排名（返回带评分的JSON）
  - `analyze_papers_batch()`: 第二阶段深度分析（返回格式化文本）
  - `analyze_paper()`: 单篇论文分析（后备/旧版）
- 使用 `tenacity` 实现自动重试和指数退避

**`src/ai/batch_coordinator.py`** - 分析流程协调
- 实现双阶段分析流程（如上所述）
- 使用 ThreadPoolExecutor 并行处理排名和全文提取
- 旧版批量分析后备方案 (`_run_legacy_batch_analysis`)
- 使用正则表达式按 Paper ID 分割批量分析文本

**`src/ai/prompts.py`** - 提示词管理 (`PromptManager`)
- 第一阶段排名提示词：返回 JSON 格式的 paper_id 和 score (1-5)
- 第二阶段分析提示词：详细分析结构（质量、创新性、严谨性、价值等）
- 支持三种分析类型：`quick`(200-300字)、`comprehensive`(400-600字)、`detailed`(600-900字)
- HTML 格式化用于邮件展示

**`src/output/formatter.py`** - 报告生成
- Markdown 输出保存到 `storage/conclusion.md`
- 使用 Jinja2 模板（`output/templates/`）生成 HTML 邮件
- 处理原始文本和预格式化的 HTML 分析结果

**`src/output/email_sender.py`** - 邮件发送
- SMTP 邮件发送，支持 HTML 内容
- 错误通知邮件
- 支持多个收件人（EMAIL_TO 逗号分隔）

### 数据流

```
1. ArxivClient.get_recent_papers()
   → List[(arxiv.Result, dict)]

2. BatchCoordinator.run_batch_analysis(papers)
   a. 第一阶段：每个窗口执行 rank_papers_in_batch()
      → 带 stage1_score 的论文
   b. 按阈值筛选 → 前N篇论文
   c. 并行：对前N篇论文执行 get_full_text()
      → 带 full_text 的论文
   d. 使用全文执行 analyze_papers_batch()
      → 原始分析文本
   e. _parse_batch_analysis() 解析
      → 带 analysis 和 html_analysis 的论文

3. OutputFormatter.format_html_email(analyzed_papers)
   → HTML 报告

4. EmailSender.send_email()
   → 发送报告
```

## 配置说明

### 必需的环境变量

必须在 GitHub Secrets 或 `.env` 文件中设置：

```bash
# AI 模型（至少配置一个，Qwen 优先）
QWEN_API_KEY=your-qwen-api-key         # 推荐：阿里云通义千问API
QWEN_MODEL=qwen-max                    # 可选，默认 qwen-max
# 或者
GLM_API_KEY=your-glm-api-key           # 推荐：智谱GLM-4.6
GLM_MODEL=glm-4.6                      # 可选，默认 glm-4.6
# 或者
DEEPSEEK_API_KEY=sk-your-api-key      # 备选：DeepSeek
DEEPSEEK_MODEL=deepseek-chat          # 可选，R1模型用 deepseek-reasoner

# 邮件配置（全部必需）
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@gmail.com          # 多个收件人用逗号分隔
```

### 配置文件：`config.yml`

关键设置（环境变量会覆盖这些值）：

- **论文搜索**：`CATEGORIES`（ArXiv分类）、`MAX_PAPERS`、`SEARCH_DAYS`
- **分析类型**：`ANALYSIS_TYPE`（quick/comprehensive/detailed）
- **性能**：`ENABLE_PARALLEL`、`MAX_WORKERS`（0=自动）、`BATCH_SIZE`
- **API设置**：`API_RETRY_TIMES`、`API_DELAY`、`API_TIMEOUT`
- **双阶段分析**：
  - `STAGE_ANALYSIS.ENABLED`
  - `STAGE1.WINDOW_SIZE`、`STAGE1.STEP_SIZE`、`STAGE1.PROMOTION_SCORE_THRESHOLD`
  - `STAGE2.MAX_PAPERS_TO_ANALYZE`

### GitHub Actions 工作流

位置：`.github/workflows/daily_paper_analysis_optimized.yml`

- **定时运行**：每日 23:00 UTC（北京时间 07:00）
- **手动触发**：支持通过 workflow_dispatch 按需运行
- **超时设置**：总共90分钟，分析步骤45分钟
- **缓存策略**：使用 uv 缓存和论文缓存提速
- **错误处理**：依赖安装和 git push 有重试机制
- **日志归档**：失败时也会上传日志（保留7天）

## 重要实现细节

### AI 模型提供商差异

在 `src/ai/analyzer.py` 中修改 AI 调用时注意：

- **智谱GLM**：不支持 `response_format` 和 `timeout` 参数
- **DeepSeek**：支持完整的 OpenAI API 参数，包括 `response_format={"type": "json_object"}` 和 `timeout`
- 始终使用 `_create_completion()` 辅助方法，它会处理这些差异

### 并行处理

系统在多个地方使用并行处理：

1. **第一阶段排名**：ThreadPoolExecutor 并发处理多个窗口排名
2. **全文提取**：ThreadPoolExecutor 并行下载和提取 PDF
3. **Worker 配置**：`MAX_WORKERS=0` 根据 CPU 核心自动计算；设置具体值可限制并发数

### 错误处理

- **重试机制**：使用 `tenacity` 库实现指数退避（默认3次重试）
- **邮件错误**：通过 `EmailSender.send_error_notification()` 发送给配置的收件人
- **日志记录**：集中在 `src/utils/logger.py`，输出到控制台和 `storage/logs/`
- **GitHub Actions**：缓存失败不影响主流程，所有情况都会上传日志

### 论文ID格式

论文使用 ArXiv 短 ID（如 "2401.12345"），通过 `arxiv.Result.get_short_id()` 获取。这是整个系统中用于匹配、解析和去重的唯一标识符。

### 存储结构

```
storage/
├── papers/          # 下载的 PDF 文件（缓存）
├── logs/            # 应用日志
├── conclusion.md    # Markdown 报告
└── report.html      # HTML 报告（不提交，通过邮件发送）
```

## 常见任务

### 添加新的 AI 提供商

1. 在 `Config.validate()` 中添加 API 密钥检查（src/config.py）
2. 在 `DeepSeekAnalyzer.__init__()` 中添加初始化逻辑（src/ai/analyzer.py）
3. 更新 `_create_completion()` 处理提供商特定参数
4. 测试：`make validate-env && make run`

### 修改分析提示词

编辑 `src/ai/prompts.py`：
- `get_stage1_ranking_system_prompt()`: 排名标准
- `get_system_prompt()`: 深度分析结构和评分标准
- `format_batch_analysis_prompt()`: 论文呈现格式

### 更改邮件模板

编辑 `output/templates/` 目录中的 Jinja2 模板。格式化器使用 `OutputFormatter.format_html_email()` 加载模板并渲染论文数据。

### 调整成本/性能平衡

在 `config.yml` 中：
- 减少 `STAGE2.MAX_PAPERS_TO_ANALYZE` 降低 API 成本
- 提高 `STAGE1.PROMOTION_SCORE_THRESHOLD` 更严格筛选
- 切换 `ANALYSIS_TYPE` 为 "quick" 缩短分析
- 减少 `MAX_PAPERS` 或 `SEARCH_DAYS` 处理更少论文
- 增加 `MAX_WORKERS` 加快处理速度（增加 API 并发）

### 调试分析问题

1. 查看 `storage/logs/` 或 GitHub Actions 工件中的日志
2. 验证 API 密钥和模型名称：`make validate-env`
3. 用少量论文测试：在 config 中设置 `MAX_PAPERS=5`
4. 禁用双阶段分析简化调试：`STAGE_ANALYSIS.ENABLED: false`
5. 检查 `_parse_batch_analysis()` 的解析结果 - 日志会显示 "Successfully parsed analysis for paper X"

## 项目特定约定

- **语言**：代码和文档混用中英文（用户文档用中文，代码注释和技术文档用英文）
- **提交信息**：使用 emoji 前缀（📚 论文更新、🔧 修复、📝 文档）
- **错误消息**：用户错误用中文，调试日志用英文
- **评分理念**：采用严格学术标准（5星制，大多数论文2-3星，4+星需要重大突破）

## 待优化事项参考

详见 `TODO_OPTIMIZATION.md`，主要优化方向：
1. 简化系统提示词（~173行 → ~30行）
2. 统一语言策略（全中文）
3. 改为逐篇并行分析（提升稳定性，成本不变）
4. 智能章节提取（而非简单截取）
5. 优化第一阶段动态排名分布
