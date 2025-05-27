# ArXiv论文追踪与分析器

一个基于 GitHub Actions 的自动化工具，每天自动追踪和分析 arXiv 最新论文，并通过邮件发送美化的分析报告。该工具采用模块化架构，支持多种AI API和美化的输出格式。

> 🚀 **新用户？** 查看 [快速开始总结](docs/setup/QUICK_START_SUMMARY.md) 了解 5 分钟配置流程！

## ✨ 新功能特点

### 🏗️ 模块化架构
- **配置管理**: 集中管理所有配置项，便于维护
- **日志系统**: 统一的日志记录，支持文件和控制台输出
- **ArXiv客户端**: 专门的论文搜索和下载模块
- **AI分析器**: 支持多种AI API的可扩展分析框架
- **输出格式化**: 支持多种输出格式（Markdown、HTML）
- **邮件发送**: 专业的邮件发送模块，支持错误通知

### 🎨 美化的输出格式
- **精美的HTML邮件模板**: 响应式设计，支持移动端
- **改进的Markdown格式**: 更清晰的结构和排版
- **统计信息**: 自动生成论文统计摘要
- **分类标签**: 美观的论文类别标签显示

### 🤖 增强的AI分析
- **优化的提示词**: 更专业和结构化的分析结果
- **多AI支持**: 预留OpenAI、Claude等API接口
- **错误重试**: 智能重试机制，提高成功率
- **分析质量**: 5个维度的深度分析

### ⚡ 并行处理优化
- **多线程分析**: 并行处理论文分析，显著缩短运行时间
- **智能负载均衡**: 自动计算最优工作线程数
- **成本优化**: 减少GitHub Actions运行时间，节省计费费用
- **性能监控**: 详细的性能统计和优化建议

### 🔧 改进的可靠性
- **配置验证**: 启动时验证所有必要配置
- **错误处理**: 完善的错误处理和通知机制
- **组件测试**: 内置连接测试功能
- **日志记录**: 详细的运行日志

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
│   ├── papers/                # 临时PDF存储目录
│   ├── logs/                  # 日志文件目录
│   └── conclusion.md          # 分析结果文件
├── .github/
│   └── workflows/
│       └── daily_paper_analysis.yml
├── requirements.txt
└── README.md
```

## 🔐 安全保障

### ✅ 您的密钥完全安全
- **GitHub Secrets 企业级加密**: 密钥在 GitHub 服务器上加密存储
- **完全私有**: 只有您能设置和查看这些密钥
- **日志自动屏蔽**: 密钥值在日志中自动显示为 `***`
- **Fork 隔离**: 其他人 Fork 您的项目时不会获得您的密钥

### 🚫 其他人无法访问您的配置
- 其他人使用此项目需要配置**自己的密钥**
- 您的 API 费用和邮箱完全私有
- 代码开源，配置私有

## 🚀 快速部署（推荐）

### 方式一: 交互式快速开始（最简单）
```bash
# 1. Fork 并克隆项目
git clone https://github.com/你的用户名/arxiv_paper_tracker.git
cd arxiv_paper_tracker

# 2. 运行快速开始向导
make quick-start
```

快速开始向导将：
- 🔐 引导您设置 Gmail 两步验证和应用专用密码
- 📝 收集所有必需的配置信息
- 🔧 生成 GitHub Secrets 设置命令
- 🧪 运行配置验证测试

### 方式二: 手动部署到 GitHub Actions
1. **Fork 此仓库** 到您的 GitHub 账号
2. **配置 Secrets**: Settings → Secrets and variables → Actions
3. **运行设置向导**: Actions → 🚀 一键设置 ArXiv 论文追踪器

**📋 配置指南**：
- [📖 用户部署指南](docs/setup/DEPLOY_FOR_USERS.md) - 完整部署流程
- [📧 Gmail 配置指南](docs/setup/GMAIL_SETUP_GUIDE.md) - Gmail 专用配置（推荐）
- [🧪 完整测试指南](docs/development/TESTING_GUIDE.md) - 本地和 GitHub Actions 测试
- [⚡ 并行优化指南](docs/development/PARALLEL_OPTIMIZATION_GUIDE.md) - 性能优化和成本节省
- [🔐 安全说明](docs/setup/SECURITY.md) - 安全保障说明

### 方式二: 本地开发

#### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/arxiv_paper_tracker.git
cd arxiv_paper_tracker
```

### 2. 安装 uv（如果尚未安装）
```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. 安装依赖
```bash
# 生产环境
uv sync --frozen

# 开发环境（包含测试和开发工具）
uv sync --all-extras --dev
```

### 4. 配置环境变量

在 GitHub 仓库设置中添加以下 Secrets：

#### 必需配置
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `SMTP_SERVER`: 邮件服务器地址（如：smtp.qq.com）
- `SMTP_PORT`: 邮件服务器端口（如：587）
- `SMTP_USERNAME`: 邮箱账号
- `SMTP_PASSWORD`: 邮箱授权码
- `EMAIL_FROM`: 发件人邮箱
- `EMAIL_TO`: 收件人邮箱（多个邮箱用逗号分隔）

#### 可选配置
可以在 `src/config.py` 中修改以下设置：
- `CATEGORIES`: 论文类别（默认：AI、机器学习、计算语言学）
- `MAX_PAPERS`: 最大论文数量（默认：50）
- `SEARCH_DAYS`: 搜索最近几天的论文（默认：2天）

## 📧 邮件模板预览

新的HTML邮件模板包含：
- 🎨 现代化的响应式设计
- 📊 论文统计概览
- 🏷️ 美观的分类标签
- 📱 移动端友好的布局
- 🔗 直接链接到原文

## 🔄 使用方法

### 自动运行
- GitHub Actions 每天早上 8 点（北京时间）自动运行
- 自动发送邮件报告
- 自动保存分析结果到仓库

### 手动触发
1. 进入仓库的 Actions 页面
2. 选择 "Daily Paper Analysis" 工作流
3. 点击 "Run workflow"

### 本地测试

#### 使用 Makefile（推荐）
```bash
# 查看所有可用命令
make help

# 设置开发环境
make dev-setup

# 运行组件测试
make test-components

# 运行完整测试套件
make test

# 运行主程序
make run

# 代码格式化
make format

# 代码检查
make lint
```

#### 手动运行
```bash
# 组件测试
cd src && uv run python test_components.py

# 完整运行
cd src && uv run python main.py

# 运行测试
uv run pytest tests/ -v

# 性能基准测试
make benchmark-quick    # 快速测试
make benchmark         # 标准测试
make benchmark-full    # 完整测试

# 代码格式化
uv run black src tests
uv run isort src tests
```

## 🛠️ 扩展开发

### 添加新的AI分析器
1. 在 `ai_analyzer.py` 中继承 `AIAnalyzer` 基类
2. 实现 `analyze_paper` 方法
3. 在 `AnalyzerFactory` 中注册新分析器

### 自定义邮件模板
1. 修改 `templates/email_template.html`
2. 使用 Jinja2 模板语法
3. 支持自定义CSS样式

### 添加新的输出格式
1. 在 `output_formatter.py` 中添加新的格式化方法
2. 支持JSON、XML等格式

## 📊 分析结果示例

每篇论文的分析包含：

1. **核心贡献**: 主要创新点和贡献
2. **技术方法**: 详细的技术方法和算法
3. **实验验证**: 实验设置、数据集和结果
4. **影响意义**: 对领域的潜在影响
5. **局限展望**: 研究局限性和未来方向

## 🔍 故障排除

### 常见问题
1. **邮件发送失败**: 检查SMTP配置和授权码
2. **API调用失败**: 检查DeepSeek API密钥和余额
3. **论文下载失败**: 网络问题，程序会自动重试

### 日志查看
- 控制台日志：实时查看运行状态
- 文件日志：`src/logs/` 目录下的日志文件
- GitHub Actions日志：在Actions页面查看详细日志

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发建议
1. 遵循现有的代码结构和命名规范
2. 添加适当的日志记录
3. 编写必要的错误处理
4. 更新相关文档

## 📄 许可证

MIT License

## 🐳 Docker 部署

### 使用 Docker Compose
```bash
# 创建 .env 文件并配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f arxiv-tracker

# 停止服务
docker-compose down
```

### 单独使用 Docker
```bash
# 构建镜像
docker build -t arxiv-paper-tracker .

# 运行容器
docker run -d \
  --name arxiv-tracker \
  -e DEEPSEEK_API_KEY=your_key \
  -e SMTP_SERVER=smtp.example.com \
  -e EMAIL_TO=your@email.com \
  -v $(pwd)/src/papers:/app/src/papers \
  arxiv-paper-tracker
```

## 🧪 测试与质量保证

### 测试覆盖率
```bash
# 运行测试并生成覆盖率报告
make test-cov

# 查看 HTML 覆盖率报告
open htmlcov/index.html
```

### 代码质量检查
```bash
# 运行所有质量检查
make ci-test

# 单独运行各项检查
make lint          # 代码风格检查
make type-check    # 类型检查
make security      # 安全检查
```

### Pre-commit Hooks
```bash
# 安装 pre-commit hooks
make pre-commit-install

# 手动运行所有检查
make pre-commit-run
```

## 🔧 开发工具

### 依赖管理
```bash
# 添加新依赖
uv add package_name

# 添加开发依赖
uv add --dev package_name

# 更新所有依赖
make update-deps

# 查看依赖树
uv tree
```

### 性能分析
```bash
# 使用 uv 的内置性能分析
uv run --with line_profiler python -m line_profiler src/main.py

# 内存使用分析
uv run --with memory_profiler python -m memory_profiler src/main.py
```

## 🔮 未来计划

- [ ] 支持更多AI API（OpenAI、Claude等）
- [ ] Web界面展示
- [ ] 论文关系图谱可视化
- [ ] 智能论文推荐
- [ ] 多语言支持
- [ ] 数据库存储历史记录
- [ ] 用户个性化订阅
- [ ] 实时通知系统
- [ ] 论文相似度分析
- [ ] 自动生成研究报告

## 📈 性能优势

使用 [uv](https://github.com/astral-sh/uv) 包管理器带来的性能提升：

- **安装速度**: 比 pip 快 10-100 倍
- **依赖解析**: 更快的依赖冲突检测和解决
- **缓存机制**: 全局缓存减少重复下载
- **并行处理**: 并行安装和构建包
- **内存效率**: 更低的内存占用

### 🚀 uv 高级功能

#### 脚本功能
```bash
# 运行独立脚本（自动管理依赖）
uv run scripts/analyze_papers.py --max-papers 10
uv run scripts/benchmark.py
uv run scripts/project_status.py
```

#### 工具管理
```bash
# 安装全局工具
make install-tools

# 列出已安装工具
make list-tools
```

#### Python 版本管理
```bash
# 查看可用 Python 版本
make python-versions

# 安装特定 Python 版本
make install-python VERSION=3.11
```

#### 项目管理
```bash
# 添加/移除依赖
make add-dep DEP=requests
make remove-dep DEP=requests

# 查看依赖树
make show-deps

# 项目状态报告
make status
```

#### 性能监控
```bash
# 缓存信息
make cache-info

# 性能基准测试
make benchmark
```

---

**注意**: 该项目已完全重构，采用现代化的 uv 包管理器和模块化架构，提供更好的性能、代码结构和扩展性。 