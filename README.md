# Hermes4ArXiv - 赫尔墨斯为您带来每日 arXiv 研究精华

🏛️ **赫尔墨斯，智慧信使，现已降临数字时代！** 这位希腊神话中的信使，化身为您的专属 AI 学术助手。

每日清晨，赫尔墨斯便会穿梭于 arXiv 的知识海洋，为您精心筛选最新的学术成果。借助 AI 的深度洞察，他将解读论文核心，凝练成精美的摘要邮件，准时送达您的案头。

> 🚀 **新用户？** 请查阅 [快速上手指南](docs/setup/QUICK_START_SUMMARY.md)，仅需 5 分钟即可完成配置！

## ✨ 赫尔墨斯的核心能力

### 🏗️ 精心设计的系统架构
- **配置核心 (Config Core)**: 统一管理所有运行参数与密钥。
- **历史记录 (Persistent Log)**: 详细记录每次任务执行与成果。
- **ArXiv 探索器 (ArXiv Explorer)**: 高效抓取 arXiv 最新论文。
- **AI 分析引擎 (AI Analysis Engine)**: 集成多种先进 AI 模型进行深度分析。
- **多格式输出 (Versatile Output)**: 将分析结果格式化为邮件、Markdown 等多种形式。
- **邮件投递 (Reliable Delivery)**: 确保学术摘要准确送达您的邮箱。

### 🎨 精致的成果呈现
- **响应式邮件设计**: 完美适配桌面与移动设备，随时随地轻松阅读。
- **优雅排版**: 类比羊皮纸卷轴的经典质感，提供舒适的阅读体验。
- **数据洞察**: 自动统计已分析论文的数量与分类。
- **多彩分类标签**: 使用清晰的标签区分不同研究领域。

### 🤖 AI 驱动的深度洞察
- **智能提示工程 (Smart Prompting)**: 优化与 AI 的交互，获取更精准的分析结果。
- **多模型支持 (Multi-Model Support)**: 可灵活切换 DeepSeek, OpenAI, Claude 等多种 AI 服务。
- **强大的容错性 (Robust Retries)**: 遇到网络波动或 API 限制时，自动智能重试。
- **五维分析法 (5-Dimension Analysis)**: 从核心贡献、技术方法、实验验证、潜在影响、局限与展望五个维度全面解读论文。

### ⚡ 高效的运行机制
- **并行处理 (Parallel Processing)**: 支持并发分析多篇论文，大幅提升处理效率。
- **智能并发调度 (Smart Concurrency)**: 自动优化并发数量，平衡速度与资源消耗。
- **资源优化 (Resource Optimization)**: 精简操作流程，减少不必要的 API 调用和 GitHub Actions 运行时间。
- **性能日志 (Performance Logging)**: 记录每次运行的耗时与效率，为持续优化提供数据支持。

### 🔧 稳健的运行保障
- **启动自检 (Pre-flight Checks)**: 任务开始前检查配置与环境，确保一切就绪。
- **错误处理机制 (Error Handling)**: 完善的异常捕获与处理，确保系统稳定运行。
- **依赖健康检查 (Dependency Health)**: 内置工具检查核心依赖是否正常。
- **详细日志记录 (Comprehensive Logging)**: 记录运行过程中的关键信息，便于追踪与调试。

## 📁 项目结构

```
arxiv_paper_tracker/
├── src/
│   ├── config.py              # 配置管理
│   ├── main.py                # 主程序
│   ├── test_components.py     # 组件测试脚本
│   ├── arxiv_client.py        # ArXiv客户端
│   ├── ai_analyzer.py         # AI分析器
│   ├── output_formatter.py    # 输出格式化器
│   ├── email_sender.py        # 邮件发送器
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py          # 日志管理
│   ├── templates/
│   │   └── email_template.html # HTML邮件模板
│   ├── papers/                # 临时PDF存储目录 (可选)
│   ├── logs/                  # 日志文件目录
│   └── conclusion.md          # 分析结果汇总文件
├── .github/
│   └── workflows/
│       └── daily_paper_analysis.yml
├── requirements.txt
└── README.md
```

## 🔐 安全保障

### ✅ 您的密钥安全无虞
- **GitHub Secrets 企业级加密**: 您的 API 密钥等敏感信息在 GitHub 服务器上经过加密存储。
- **完全私有**: 只有您能设置和查看这些密钥。
- **日志自动脱敏**: 敏感信息（如 API 密钥）在日志输出时会自动以 `***` 替代。
- **Fork 隔离**: 其他用户 Fork 您的项目时，不会获取到您的 Secrets 配置。

### 🚫 他人无法访问您的配置
- 其他用户使用此项目需要配置**其各自的密钥**。
- 您的 API 调用额度、费用以及邮箱账户完全私有。
- 项目代码开源，但您的个人配置是私密的。

## 🚀 快速开始 (推荐)

### 方式一: 使用 `make` 快速启动 (最简单)
```bash
# 1. 克隆赫尔墨斯到本地
git clone https://github.com/你的用户名/hermes4arxiv.git # 请替换为你的 Fork
cd hermes4arxiv

# 2. 启动快速配置向导
make quick-start
```
此向导将帮助您：
- 🔐 安全地设置 Gmail (或其他邮件服务商) 的访问凭证和 AI API 密钥。
- 📝 收集运行赫尔墨斯所需的基础配置。
- 🔧 生成 GitHub Actions 所需的 Secrets 列表 (供您手动复制粘贴)。
- 🧪 测试核心组件，确保一切准备就绪。

### 方式二: 手动部署到 GitHub Actions
1.  **Fork 此仓库** 到您的 GitHub 账号。
2.  **配置 Secrets**: 在您的 Fork 仓库中，前往 `Settings` → `Secrets and variables` → `Actions`。
3.  **运行设置向导 (可选但推荐)**: 在您的 Fork 仓库中，前往 `Actions` 标签页，找到名为 "🚀 一键设置 ArXiv 论文追踪器" (或类似名称) 的 Workflow 并手动触发它来引导您完成配置。

**📋 配置指南**：
- [📖 用户部署指南](docs/setup/DEPLOY_FOR_USERS.md) - 完整部署流程
- [📧 Gmail 配置指南](docs/setup/GMAIL_SETUP_GUIDE.md) - Gmail 专用配置（推荐）
- [🧪 完整测试指南](docs/development/TESTING_GUIDE.md) - 本地和 GitHub Actions 测试
- [⚡ 并行优化指南](docs/development/PARALLEL_OPTIMIZATION_GUIDE.md) - 性能优化和成本节省
- [🔧 缓存问题指南](docs/development/CACHE_ISSUES_GUIDE.md) - GitHub Actions 缓存超时解决方案
- [🔐 安全说明](docs/setup/SECURITY.md) - 安全保障说明

### 方式三: 本地开发与运行

#### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/hermes4arxiv.git # 请替换为你的 Fork
cd hermes4arxiv
```

#### 2. 安装 uv (推荐的 Python 包管理器)
```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 3. 安装依赖
```bash
# 仅安装生产环境依赖
uv sync

# 安装所有依赖，包括开发和测试工具
uv sync --all-extras --dev
```

#### 4. 配置环境变量
在 GitHub 仓库 `Settings` → `Secrets and variables` → `Actions` 中添加以下 Secrets，或在本地创建 `.env` 文件进行配置 (参考 `.env.example`)：

##### 必需配置
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥 (或其他 AI 服务商的密钥，如 `OPENAI_API_KEY`)
- `SMTP_SERVER`: 邮件服务器地址 (例如: `smtp.gmail.com`, `smtp.qq.com`)
- `SMTP_PORT`: 邮件服务器端口 (例如: `587` for TLS, `465` for SSL)
- `SMTP_USERNAME`: 您的邮箱账号
- `SMTP_PASSWORD`: 您的邮箱授权码 (注意：通常不是邮箱登录密码)
- `EMAIL_FROM`: 发件人邮箱地址
- `EMAIL_TO`: 收件人邮箱地址 (多个邮箱请用逗号 `,` 分隔)

##### 可选配置 (可在 `src/config.py` 中修改默认值)
- `CATEGORIES`: 关注的 arXiv 论文类别 (默认: `cs.AI, cs.LG, cs.CL`)
- `MAX_PAPERS`: 每次获取和分析的最大论文数量 (默认: `50`)
- `SEARCH_DAYS`: 搜索最近几天的论文 (默认: `2` 天)
- `AI_PROVIDER`: 使用的AI服务商 (默认: `deepseek`, 可选 `openai`, `claude` 等，需确保对应KEY已配置)

## 📧 邮件模板预览

我们的 HTML 邮件模板具备：
- 🎨 现代、响应式设计，适配各种屏幕尺寸。
- 📊 清晰的论文统计概览。
- 🏷️ 为不同学科领域设计的直观分类标签。
- 📱 移动端优先的友好布局。
- 🔗 每篇论文均附带原文直达链接。

## 🔄 使用方法

### 自动运行 (GitHub Actions)
- 默认配置下，GitHub Actions 将在北京时间每日早上 8 点自动运行。
- 自动分析最新的论文并发送邮件报告。
- 分析结果 (如 `conclusion.md`) 会自动提交到您的仓库。

### 手动触发 (GitHub Actions)
1.  进入您 Fork 后仓库的 `Actions` 页面。
2.  选择 "Daily Paper Analysis" (或类似名称的) 工作流。
3.  点击 "Run workflow" 按钮手动触发。

### 本地运行与测试

#### 使用 Makefile (推荐)
```bash
# 查看所有可用命令
make help

# 设置开发环境 (创建虚拟环境并安装依赖)
make dev-setup

# 运行组件连接性测试 (如 AI API, SMTP 服务)
make test-components

# 运行完整的单元测试和集成测试套件
make test

# 在本地运行主程序 (抓取、分析、发送邮件)
make run

# 代码格式化 (Black, isort)
make format

# 代码风格与静态检查 (Flake8, MyPy)
make lint
```

#### 手动运行命令
```bash
# (确保已激活虚拟环境或使用 uv run)

# 组件连接性测试
cd src && uv run python test_components.py

# 完整运行主程序
cd src && uv run python main.py

# 运行单元测试
uv run pytest tests/ -v

# 性能基准测试
make benchmark-quick    # 快速基准测试
make benchmark         # 标准基准测试
make benchmark-full    # 完整基准测试

# 代码格式化
uv run black src tests
uv run isort src tests
```

## 🛠️ 扩展与定制

### 添加新的 AI 分析器
1.  在 `src/ai_analyzer.py` 文件中，创建一个继承自 `AIAnalyzer` 基类的新类。
2.  实现其 `analyze_paper` 方法，以符合您的新 AI 服务或定制逻辑。
3.  在 `AnalyzerFactory` 中注册您的新分析器，并在配置文件中指定使用。

### 自定义邮件模板
1.  编辑 `src/templates/email_template.html` 文件。
2.  该模板使用 Jinja2 模板引擎语法。
3.  您可以自由修改 HTML 结构和 CSS 样式。

### 添加新的输出格式
1.  在 `src/output_formatter.py` 中，添加新的格式化方法或类。
2.  例如，您可以轻松添加对 JSON、XML 或其他文本格式的支持。

## 📊 分析结果示例

每篇论文的分析报告通常包含以下五个方面：

1.  **核心贡献 (Core Contribution)**: 论文的主要创新点和对领域的贡献。
2.  **技术方法 (Technical Methods)**: 使用的关键技术、算法和模型细节。
3.  **实验验证 (Experimental Validation)**: 实验设计、所用数据集及主要结果。
4.  **影响与意义 (Impact & Significance)**: 该研究对学术界或工业界的潜在影响。
5.  **局限与展望 (Limitations & Future Work)**: 研究的局限性以及未来可能的研究方向。

## 🔍 故障排除

### 常见问题解答
1.  **邮件发送失败**:
    *   检查 `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` 配置是否正确。
    *   确认邮箱是否开启了 SMTP 服务，以及 `SMTP_PASSWORD` 是否为正确的授权码而非登录密码。
    *   检查网络连接和防火墙设置。
2.  **AI API 调用失败**:
    *   检查对应的 API 密钥 (如 `DEEPSEEK_API_KEY`) 是否正确且有效。
    *   确认您的 API 账户有足够的余额或配额。
    *   部分 AI 服务可能有区域限制或请求频率限制。
3.  **论文下载或解析失败**:
    *   可能是 arXiv 暂时无法访问或网络问题，程序内置了重试机制。
    *   PDF 文件损坏或格式特殊，这种情况较为罕见。

### 日志查看
- **控制台输出**: 在本地运行时，关键信息会直接打印到控制台。
- **文件日志**: 详细日志保存在 `src/logs/` 目录下的文件中，按日期命名。
- **GitHub Actions 日志**: 在 GitHub 仓库的 `Actions` 标签页，点击对应的工作流运行记录，可以查看详细的执行日志。

## 🤝 贡献指南

我们热烈欢迎各种形式的贡献，包括但不限于提交 Issue、发起 Pull Request！

### 开发建议
1.  请尽量遵循项目现有的代码结构和命名约定。
2.  在添加新功能或修复 Bug 时，请添加适当的日志记录。
3.  确保代码包含必要的错误处理逻辑。
4.  如果改动较大或添加了新功能，请更新相关的文档（如 README 或 docs 目录下的文件）。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源。

## 🐳 Docker 部署 (应该用不上吧)

### 使用 Docker Compose
```bash
# 1. 复制环境变量模板文件
cp .env.example .env

# 2. 编辑 .env 文件，填入您的配置信息
# nano .env  (或其他编辑器)

# 3. 启动服务 (后台运行)
docker-compose up -d

# 查看服务日志
docker-compose logs -f arxiv-tracker

# 停止并移除服务
docker-compose down
```

### 单独使用 Docker
```bash
# 1. 构建 Docker 镜像
docker build -t hermes4arxiv .

# 2. 运行 Docker 容器
# (请将下面的your_key, smtp.example.com等替换为您的实际配置)
docker run -d \
  --name hermes-tracker \
  -e DEEPSEEK_API_KEY="your_deepseek_key" \
  -e SMTP_SERVER="smtp.example.com" \
  -e SMTP_PORT="587" \
  -e SMTP_USERNAME="your_email_username" \
  -e SMTP_PASSWORD="your_email_app_password" \
  -e EMAIL_FROM="sender@example.com" \
  -e EMAIL_TO="recipient@example.com" \
  -v $(pwd)/src/papers:/app/src/papers `# 可选：挂载论文存储目录` \
  -v $(pwd)/src/logs:/app/src/logs `# 可选：挂载日志目录` \
  hermes4arxiv
```

## 🧪 测试与质量保证

### 测试覆盖率
```bash
# 运行测试并生成覆盖率报告
make test-cov

# 在浏览器中打开 HTML 格式的覆盖率报告
# (通常在 htmlcov/index.html)
open htmlcov/index.html # macOS
# xdg-open htmlcov/index.html # Linux
```

### 代码质量检查
```bash
# 运行所有配置的 CI 测试 (格式化、Linter、类型检查等)
make ci-check

# 单独运行各项检查:
make format        # 自动格式化代码 (Black, isort)
make lint          # 代码风格和静态分析 (Flake8)
make type-check    # 类型检查 (MyPy)
make security      # 安全漏洞扫描 (Bandit)
```

### Pre-commit Hooks
为了在提交代码前自动进行代码检查和格式化，推荐设置 pre-commit hooks。
```bash
# 安装 pre-commit 到您的 git hooks
make pre-commit-install

# (可选) 手动对所有文件运行 pre-commit 检查
make pre-commit-run
```

## 🔧 开发工具与依赖管理 (使用 uv)

`uv` 是一个极速的 Python 包安装器和解析器，能显著提升开发体验。

### 依赖管理
```bash
# 添加新的生产依赖
uv pip install package_name
# 然后更新 requirements.txt:
uv pip freeze > requirements.txt

# 添加新的开发依赖
uv pip install --dev package_name
# 然后更新 requirements-dev.txt (如果使用此文件):
# uv pip freeze --dev > requirements-dev.txt (或手动添加到pyproject.toml)

# 更新所有依赖到最新兼容版本
make update-deps

# 查看项目依赖树
uv pip list --tree # (或 uv tree，取决于uv版本和配置)
```
*注意: `uv add` 和 `uv sync` 更适用于 `pyproject.toml` 管理的项目。对于 `requirements.txt`，通常使用 `uv pip install` 和 `uv pip freeze`。Makefile 命令已适配这些操作。*

### 性能分析
```bash
# 使用 Python 内置 cProfile 进行性能分析
uv run python -m cProfile -o profile.stats src/main.py
# 之后可以使用 snakeviz 或 pstats 查看结果

# 内存使用分析 (需要安装 memory_profiler)
# 在关键函数上添加 @profile 装饰器
# uv run python -m memory_profiler src/main.py
```

## 🔮 未来计划

- [ ] 支持更多 AI API 服务商 (例如 Google Gemini)。
- [ ] 用户友好的 Web 界面，用于配置和查阅历史记录。
- [ ] 论文关系图谱可视化，探索研究主题间的联系。
- [ ] 基于用户阅读历史和偏好的智能论文推荐。
- [ ] 多语言支持 (UI 和论文摘要翻译)。
- [ ] 将历史分析结果存储到数据库 (如 SQLite, PostgreSQL)。
- [ ] 更细致的用户个性化订阅选项 (例如按关键词、作者订阅)。
- [ ] 实时通知系统 (例如通过 Slack, Telegram)。
- [ ] 论文相似度分析，发现相关研究。
- [ ] 自动生成周报或月报形式的研究进展报告。

## 📈 性能优势 (受益于 `uv`)

本项目使用 [uv](https://github.com/astral-sh/uv) 作为包管理器，为您带来显著的性能提升：
- **极速安装**: `uv` 的安装和依赖解析速度远超传统 `pip` 和 `venv` 组合，通常快 10-100 倍。
- **高效缓存**: 全局缓存机制有效减少重复下载和构建。
- **并行处理**: `uv` 在安装和构建包时利用并行处理，进一步加速。
- **更低资源占用**: 相比其他一些工具，`uv` 在操作时内存占用更低。

### 🚀 `uv` 助力开发效率 (通过 `Makefile`)

本项目 `Makefile` 集成了 `uv` 的诸多便利功能，简化开发流程：

#### 脚本运行
```bash
# 运行特定脚本，uv 会确保其依赖在隔离环境中可用
# 例如，若有 scripts/analyze_single_paper.py:
# uv run python scripts/analyze_single_paper.py --arxiv-id 2305.00001
```

#### 项目管理与环境
```bash
# 创建或同步虚拟环境并安装依赖
make dev-setup # 内部使用 uv sync

# 添加/移除依赖 (通过 Makefile 封装 uv 命令)
make add-dep DEP=requests
make remove-dep DEP=requests-cache

# 查看当前项目状态和依赖 (封装 uv 相关命令)
make status
make show-deps
```

#### 性能与缓存
```bash
# 查看 uv 缓存信息
make cache-info

# 运行性能基准测试
make benchmark
```

---

**核心改动点总结:**

1.  **标题和副标题:** 更直接地说明项目价值。
2.  **特性列表:** 将原来的“神力”名称改为了更贴近功能、同时又不失专业性的描述。例如，“神殿般的架构设计” 改为 “精心设计的系统架构”，其下的“智慧中枢”改为“配置核心”。这样既保留了“赫尔墨斯”的品牌形象，又清晰说明了功能。
3.  **语言风格:** 整体更流畅，减少了生硬的比喻，使描述更自然。
4.  **配置部分:** 对环境变量和 `config.py` 的说明更清晰。Okay, I can definitely help you refine this README. The core idea of Hermes is great, and the enthusiasm is there! We can make the language more polished and ensure the metaphors enhance rather than feel tacked on.

Here's a revised version. I've tried to:

1.  **Tone down overly "forced" metaphors:** Some are kept where they add charm, but others are replaced with more direct, professional language that still sounds engaging.
2.  **Improve flow and readability:** Make transitions smoother.
3.  **Strengthen clarity:** Ensure the "what" and "why" are immediately obvious.
4.  **Maintain enthusiasm:** Keep the positive and exciting tone, just make it more refined.
5.  **Keep the structure:** The existing structure is good and comprehensive.

Here's the suggested revision:

---

# Hermes4ArXiv - 赫尔墨斯为您带来每日 arXiv 研究精华

🏛️ **赫尔墨斯，智慧信使，现已降临数字时代！** 这位希腊神话中的信使，化身为您的专属 AI 学术助手。

每日清晨，赫尔墨斯便会穿梭于 arXiv 的知识海洋，为您精心筛选最新的学术成果。借助 AI 的深度洞察，他将解读论文核心，凝练成精美的摘要邮件，准时送达您的案头。

> 🚀 **新用户？** 请查阅 [快速上手指南](docs/setup/QUICK_START_SUMMARY.md)，仅需 5 分钟即可完成配置！

## ✨ 赫尔墨斯的核心能力

### 🏗️ 精心设计的系统架构
- **配置核心 (Config Core)**: 统一管理所有运行参数与密钥。
- **历史记录 (Persistent Log)**: 详细记录每次任务执行与成果。
- **ArXiv 探索器 (ArXiv Explorer)**: 高效抓取 arXiv 最新论文。
- **AI 分析引擎 (AI Analysis Engine)**: 集成多种先进 AI 模型进行深度分析。
- **多格式输出 (Versatile Output)**: 将分析结果格式化为邮件、Markdown 等多种形式。
- **邮件投递 (Reliable Delivery)**: 确保学术摘要准确送达您的邮箱。

### 🎨 精致的成果呈现
- **响应式邮件设计**: 完美适配桌面与移动设备，随时随地轻松阅读。
- **优雅排版**: 类比羊皮纸卷轴的经典质感，提供舒适的阅读体验。
- **数据洞察**: 自动统计已分析论文的数量与分类。
- **多彩分类标签**: 使用清晰的标签区分不同研究领域。

### 🤖 AI 驱动的深度洞察
- **智能提示工程 (Smart Prompting)**: 优化与 AI 的交互，获取更精准的分析结果。
- **多模型支持 (Multi-Model Support)**: 可灵活切换 DeepSeek, OpenAI, Claude 等多种 AI 服务。
- **强大的容错性 (Robust Retries)**: 遇到网络波动或 API 限制时，自动智能重试。
- **五维分析法 (5-Dimension Analysis)**: 从核心贡献、技术方法、实验验证、潜在影响、局限与展望五个维度全面解读论文。

### ⚡ 高效的运行机制
- **并行处理 (Parallel Processing)**: 支持并发分析多篇论文，大幅提升处理效率。
- **智能并发调度 (Smart Concurrency)**: 自动优化并发数量，平衡速度与资源消耗。
- **资源优化 (Resource Optimization)**: 精简操作流程，减少不必要的 API 调用和 GitHub Actions 运行时间。
- **性能日志 (Performance Logging)**: 记录每次运行的耗时与效率，为持续优化提供数据支持。

### 🔧 稳健的运行保障
- **启动自检 (Pre-flight Checks)**: 任务开始前检查配置与环境，确保一切就绪。
- **错误处理机制 (Error Handling)**: 完善的异常捕获与处理，确保系统稳定运行。
- **依赖健康检查 (Dependency Health)**: 内置工具检查核心依赖是否正常。
- **详细日志记录 (Comprehensive Logging)**: 记录运行过程中的关键信息，便于追踪与调试。

## 📁 项目结构

```
arxiv_paper_tracker/
├── src/
│   ├── config.py              # 配置管理
│   ├── main.py                # 主程序
│   ├── test_components.py     # 组件测试脚本
│   ├── arxiv_client.py        # ArXiv客户端
│   ├── ai_analyzer.py         # AI分析器
│   ├── output_formatter.py    # 输出格式化器
│   ├── email_sender.py        # 邮件发送器
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py          # 日志管理
│   ├── templates/
│   │   └── email_template.html # HTML邮件模板
│   ├── papers/                # 临时PDF存储目录 (可选)
│   ├── logs/                  # 日志文件目录
│   └── conclusion.md          # 分析结果汇总文件
├── .github/
│   └── workflows/
│       └── daily_paper_analysis.yml
├── requirements.txt
└── README.md
```

## 🔐 安全保障

### ✅ 您的密钥安全无虞
- **GitHub Secrets 企业级加密**: 您的 API 密钥等敏感信息在 GitHub 服务器上经过加密存储。
- **完全私有**: 只有您能设置和查看这些密钥。
- **日志自动脱敏**: 敏感信息（如 API 密钥）在日志输出时会自动以 `***` 替代。
- **Fork 隔离**: 其他用户 Fork 您的项目时，不会获取到您的 Secrets 配置。

### 🚫 他人无法访问您的配置
- 其他用户使用此项目需要配置**其各自的密钥**。
- 您的 API 调用额度、费用以及邮箱账户完全私有。
- 项目代码开源，但您的个人配置是私密的。

## 🚀 快速开始 (推荐)

### 方式一: 使用 `make` 快速启动 (最简单)
```bash
# 1. 克隆赫尔墨斯到本地
git clone https://github.com/你的用户名/hermes4arxiv.git # 请替换为你的 Fork
cd hermes4arxiv

# 2. 启动快速配置向导
make quick-start
```
此向导将帮助您：
- 🔐 安全地设置 Gmail (或其他邮件服务商) 的访问凭证和 AI API 密钥。
- 📝 收集运行赫尔墨斯所需的基础配置。
- 🔧 生成 GitHub Actions 所需的 Secrets 列表 (供您手动复制粘贴)。
- 🧪 测试核心组件，确保一切准备就绪。

### 方式二: 手动部署到 GitHub Actions
1.  **Fork 此仓库** 到您的 GitHub 账号。
2.  **配置 Secrets**: 在您的 Fork 仓库中，前往 `Settings` → `Secrets and variables` → `Actions`。
3.  **运行设置向导 (可选但推荐)**: 在您的 Fork 仓库中，前往 `Actions` 标签页，找到名为 "🚀 一键设置 ArXiv 论文追踪器" (或类似名称) 的 Workflow 并手动触发它来引导您完成配置。

**📋 配置指南**：
- [📖 用户部署指南](docs/setup/DEPLOY_FOR_USERS.md) - 完整部署流程
- [📧 Gmail 配置指南](docs/setup/GMAIL_SETUP_GUIDE.md) - Gmail 专用配置（推荐）
- [🧪 完整测试指南](docs/development/TESTING_GUIDE.md) - 本地和 GitHub Actions 测试
- [⚡ 并行优化指南](docs/development/PARALLEL_OPTIMIZATION_GUIDE.md) - 性能优化和成本节省
- [🔧 缓存问题指南](docs/development/CACHE_ISSUES_GUIDE.md) - GitHub Actions 缓存超时解决方案
- [🔐 安全说明](docs/setup/SECURITY.md) - 安全保障说明

### 方式三: 本地开发与运行

#### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/hermes4arxiv.git # 请替换为你的 Fork
cd hermes4arxiv
```

#### 2. 安装 uv (推荐的 Python 包管理器)
```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 3. 安装依赖
```bash
# 仅安装生产环境依赖
uv sync

# 安装所有依赖，包括开发和测试工具
uv sync --all-extras --dev
```

#### 4. 配置环境变量
在 GitHub 仓库 `Settings` → `Secrets and variables` → `Actions` 中添加以下 Secrets，或在本地创建 `.env` 文件进行配置 (参考 `.env.example`)：

##### 必需配置
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥 (或其他 AI 服务商的密钥，如 `OPENAI_API_KEY`)
- `SMTP_SERVER`: 邮件服务器地址 (例如: `smtp.gmail.com`, `smtp.qq.com`)
- `SMTP_PORT`: 邮件服务器端口 (例如: `587` for TLS, `465` for SSL)
- `SMTP_USERNAME`: 您的邮箱账号
- `SMTP_PASSWORD`: 您的邮箱授权码 (注意：通常不是邮箱登录密码)
- `EMAIL_FROM`: 发件人邮箱地址
- `EMAIL_TO`: 收件人邮箱地址 (多个邮箱请用逗号 `,` 分隔)

##### 可选配置 (可在 `src/config.py` 中修改默认值)
- `CATEGORIES`: 关注的 arXiv 论文类别 (默认: `cs.AI, cs.LG, cs.CL`)
- `MAX_PAPERS`: 每次获取和分析的最大论文数量 (默认: `50`)
- `SEARCH_DAYS`: 搜索最近几天的论文 (默认: `2` 天)
- `AI_PROVIDER`: 使用的AI服务商 (默认: `deepseek`, 可选 `openai`, `claude` 等，需确保对应KEY已配置)

## 📧 邮件模板预览

我们的 HTML 邮件模板具备：
- 🎨 现代、响应式设计，适配各种屏幕尺寸。
- 📊 清晰的论文统计概览。
- 🏷️ 为不同学科领域设计的直观分类标签。
- 📱 移动端优先的友好布局。
- 🔗 每篇论文均附带原文直达链接。

## 🔄 使用方法

### 自动运行 (GitHub Actions)
- 默认配置下，GitHub Actions 将在北京时间每日早上 8 点自动运行。
- 自动分析最新的论文并发送邮件报告。
- 分析结果 (如 `conclusion.md`) 会自动提交到您的仓库。

### 手动触发 (GitHub Actions)
1.  进入您 Fork 后仓库的 `Actions` 页面。
2.  选择 "Daily Paper Analysis" (或类似名称的) 工作流。
3.  点击 "Run workflow" 按钮手动触发。

### 本地运行与测试

#### 使用 Makefile (推荐)
```bash
# 查看所有可用命令
make help

# 设置开发环境 (创建虚拟环境并安装依赖)
make dev-setup

# 运行组件连接性测试 (如 AI API, SMTP 服务)
make test-components

# 运行完整的单元测试和集成测试套件
make test

# 在本地运行主程序 (抓取、分析、发送邮件)
make run

# 代码格式化 (Black, isort)
make format

# 代码风格与静态检查 (Flake8, MyPy)
make lint
```

#### 手动运行命令
```bash
# (确保已激活虚拟环境或使用 uv run)

# 组件连接性测试
cd src && uv run python test_components.py

# 完整运行主程序
cd src && uv run python main.py

# 运行单元测试
uv run pytest tests/ -v

# 性能基准测试
make benchmark-quick    # 快速基准测试
make benchmark         # 标准基准测试
make benchmark-full    # 完整基准测试

# 代码格式化
uv run black src tests
uv run isort src tests
```

## 🛠️ 扩展与定制

### 添加新的 AI 分析器
1.  在 `src/ai_analyzer.py` 文件中，创建一个继承自 `AIAnalyzer` 基类的新类。
2.  实现其 `analyze_paper` 方法，以符合您的新 AI 服务或定制逻辑。
3.  在 `AnalyzerFactory` 中注册您的新分析器，并在配置文件中指定使用。

### 自定义邮件模板
1.  编辑 `src/templates/email_template.html` 文件。
2.  该模板使用 Jinja2 模板引擎语法。
3.  您可以自由修改 HTML 结构和 CSS 样式。

### 添加新的输出格式
1.  在 `src/output_formatter.py` 中，添加新的格式化方法或类。
2.  例如，您可以轻松添加对 JSON、XML 或其他文本格式的支持。

## 📊 分析结果示例

每篇论文的分析报告通常包含以下五个方面：

1.  **核心贡献 (Core Contribution)**: 论文的主要创新点和对领域的贡献。
2.  **技术方法 (Technical Methods)**: 使用的关键技术、算法和模型细节。
3.  **实验验证 (Experimental Validation)**: 实验设计、所用数据集及主要结果。
4.  **影响与意义 (Impact & Significance)**: 该研究对学术界或工业界的潜在影响。
5.  **局限与展望 (Limitations & Future Work)**: 研究的局限性以及未来可能的研究方向。

## 🔍 故障排除

### 常见问题解答
1.  **邮件发送失败**:
    *   检查 `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` 配置是否正确。
    *   确认邮箱是否开启了 SMTP 服务，以及 `SMTP_PASSWORD` 是否为正确的授权码而非登录密码。
    *   检查网络连接和防火墙设置。
2.  **AI API 调用失败**:
    *   检查对应的 API 密钥 (如 `DEEPSEEK_API_KEY`) 是否正确且有效。
    *   确认您的 API 账户有足够的余额或配额。
    *   部分 AI 服务可能有区域限制或请求频率限制。
3.  **论文下载或解析失败**:
    *   可能是 arXiv 暂时无法访问或网络问题，程序内置了重试机制。
    *   PDF 文件损坏或格式特殊，这种情况较为罕见。

### 日志查看
- **控制台输出**: 在本地运行时，关键信息会直接打印到控制台。
- **文件日志**: 详细日志保存在 `src/logs/` 目录下的文件中，按日期命名。
- **GitHub Actions 日志**: 在 GitHub 仓库的 `Actions` 标签页，点击对应的工作流运行记录，可以查看详细的执行日志。

## 🤝 贡献指南

我们热烈欢迎各种形式的贡献，包括但不限于提交 Issue、发起 Pull Request！

### 开发建议
1.  请尽量遵循项目现有的代码结构和命名约定。
2.  在添加新功能或修复 Bug 时，请添加适当的日志记录。
3.  确保代码包含必要的错误处理逻辑。
4.  如果改动较大或添加了新功能，请更新相关的文档（如 README 或 docs 目录下的文件）。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源。

## 🐳 Docker 部署 (可选)

### 使用 Docker Compose
```bash
# 1. 复制环境变量模板文件
cp .env.example .env

# 2. 编辑 .env 文件，填入您的配置信息
# nano .env  (或其他编辑器)

# 3. 启动服务 (后台运行)
docker-compose up -d

# 查看服务日志
docker-compose logs -f arxiv-tracker

# 停止并移除服务
docker-compose down
```

### 单独使用 Docker
```bash
# 1. 构建 Docker 镜像
docker build -t hermes4arxiv .

# 2. 运行 Docker 容器
# (请将下面的your_key, smtp.example.com等替换为您的实际配置)
docker run -d \
  --name hermes-tracker \
  -e DEEPSEEK_API_KEY="your_deepseek_key" \
  -e SMTP_SERVER="smtp.example.com" \
  -e SMTP_PORT="587" \
  -e SMTP_USERNAME="your_email_username" \
  -e SMTP_PASSWORD="your_email_app_password" \
  -e EMAIL_FROM="sender@example.com" \
  -e EMAIL_TO="recipient@example.com" \
  -v $(pwd)/src/papers:/app/src/papers `# 可选：挂载论文存储目录` \
  -v $(pwd)/src/logs:/app/src/logs `# 可选：挂载日志目录` \
  hermes4arxiv
```

## 🧪 测试与质量保证

### 测试覆盖率
```bash
# 运行测试并生成覆盖率报告
make test-cov

# 在浏览器中打开 HTML 格式的覆盖率报告
# (通常在 htmlcov/index.html)
open htmlcov/index.html # macOS
# xdg-open htmlcov/index.html # Linux
```

### 代码质量检查
```bash
# 运行所有配置的 CI 测试 (格式化、Linter、类型检查等)
make ci-check

# 单独运行各项检查:
make format        # 自动格式化代码 (Black, isort)
make lint          # 代码风格和静态分析 (Flake8)
make type-check    # 类型检查 (MyPy)
make security      # 安全漏洞扫描 (Bandit)
```

### Pre-commit Hooks
为了在提交代码前自动进行代码检查和格式化，推荐设置 pre-commit hooks。
```bash
# 安装 pre-commit 到您的 git hooks
make pre-commit-install

# (可选) 手动对所有文件运行 pre-commit 检查
make pre-commit-run
```

## 🔧 开发工具与依赖管理 (使用 uv)

`uv` 是一个极速的 Python 包安装器和解析器，能显著提升开发体验。

### 依赖管理
```bash
# 添加新的生产依赖
uv pip install package_name
# 然后更新 requirements.txt:
uv pip freeze > requirements.txt

# 添加新的开发依赖
uv pip install --dev package_name
# 然后更新 requirements-dev.txt (如果使用此文件):
# uv pip freeze --dev > requirements-dev.txt (或手动添加到pyproject.toml)

# 更新所有依赖到最新兼容版本
make update-deps

# 查看项目依赖树
uv pip list --tree # (或 uv tree，取决于uv版本和配置)
```
*注意: `uv add` 和 `uv sync` 更适用于 `pyproject.toml` 管理的项目。对于 `requirements.txt`，通常使用 `uv pip install` 和 `uv pip freeze`。Makefile 命令已适配这些操作。*

### 性能分析
```bash
# 使用 Python 内置 cProfile 进行性能分析
uv run python -m cProfile -o profile.stats src/main.py
# 之后可以使用 snakeviz 或 pstats 查看结果

# 内存使用分析 (需要安装 memory_profiler)
# 在关键函数上添加 @profile 装饰器
# uv run python -m memory_profiler src/main.py
```

## 🔮 未来计划

- [ ] 支持更多 AI API 服务商 (例如 Google Gemini)。
- [ ] 用户友好的 Web 界面，用于配置和查阅历史记录。
- [ ] 论文关系图谱可视化，探索研究主题间的联系。
- [ ] 基于用户阅读历史和偏好的智能论文推荐。
- [ ] 多语言支持 (UI 和论文摘要翻译)。
- [ ] 将历史分析结果存储到数据库 (如 SQLite, PostgreSQL)。
- [ ] 更细致的用户个性化订阅选项 (例如按关键词、作者订阅)。
- [ ] 实时通知系统 (例如通过 Slack, Telegram)。
- [ ] 论文相似度分析，发现相关研究。
- [ ] 自动生成周报或月报形式的研究进展报告。

## 📈 性能优势 (受益于 `uv`)

本项目使用 [uv](https://github.com/astral-sh/uv) 作为包管理器，为您带来显著的性能提升：
- **极速安装**: `uv` 的安装和依赖解析速度远超传统 `pip` 和 `venv` 组合，通常快 10-100 倍。
- **高效缓存**: 全局缓存机制有效减少重复下载和构建。
- **并行处理**: `uv` 在安装和构建包时利用并行处理，进一步加速。
- **更低资源占用**: 相比其他一些工具，`uv` 在操作时内存占用更低。

### 🚀 `uv` 助力开发效率 (通过 `Makefile`)

本项目 `Makefile` 集成了 `uv` 的诸多便利功能，简化开发流程：

#### 脚本运行
```bash
# 运行特定脚本，uv 会确保其依赖在隔离环境中可用
# 例如，若有 scripts/analyze_single_paper.py:
# uv run python scripts/analyze_single_paper.py --arxiv-id 2305.00001
```

#### 项目管理与环境
```bash
# 创建或同步虚拟环境并安装依赖
make dev-setup # 内部使用 uv sync

# 添加/移除依赖 (通过 Makefile 封装 uv 命令)
make add-dep DEP=requests
make remove-dep DEP=requests-cache

# 查看当前项目状态和依赖 (封装 uv 相关命令)
make status
make show-deps
```

#### 性能与缓存
```bash
# 查看 uv 缓存信息
make cache-info

# 运行性能基准测试
make benchmark
```

---
