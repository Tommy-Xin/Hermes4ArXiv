.PHONY: help install install-dev test test-cov lint format type-check security clean run test-components

help: ## 显示帮助信息
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装生产依赖
	uv sync --frozen

install-dev: ## 安装开发依赖
	uv sync --all-extras --dev

test: ## 运行测试
	uv run pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	uv run pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

lint: ## 运行代码检查
	uv run black --check src tests
	uv run isort --check-only src tests
	uv run flake8 src tests

format: ## 格式化代码
	uv run black src tests
	uv run isort src tests

type-check: ## 运行类型检查
	uv run mypy src

security: ## 运行安全检查
	uv run bandit -r src
	uv run safety check

clean: ## 清理临时文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

run: ## 运行主程序
	cd src && uv run python main.py

test-components: ## 运行组件测试
	cd src && uv run python test_components.py

pre-commit-install: ## 安装 pre-commit hooks
	uv run pre-commit install

pre-commit-run: ## 运行 pre-commit 检查
	uv run pre-commit run --all-files

build: ## 构建包
	uv build

publish: ## 发布到 PyPI (需要配置 token)
	uv publish

dev-setup: install-dev pre-commit-install ## 完整的开发环境设置

ci-test: lint type-check security test ## CI 测试流程

update-deps: ## 更新依赖
	uv lock --upgrade

# uv 脚本功能
run-script: ## 运行独立脚本 (用法: make run-script SCRIPT=scripts/analyze_papers.py ARGS="--max-papers 3")
	uv run $(SCRIPT) $(ARGS)

benchmark: ## 运行性能基准测试
	uv run scripts/benchmark.py

quick-analysis: ## 快速论文分析（不使用AI）
	uv run scripts/analyze_papers.py --max-papers 5 --search-days 3

status: ## 显示项目状态报告
	uv run scripts/project_status.py

validate-env: ## 验证环境变量配置
	uv run scripts/validate_env.py

# uv 工具管理
install-tools: ## 安装常用开发工具
	uv tool install ruff
	uv tool install black
	uv tool install mypy
	uv tool install pytest

list-tools: ## 列出已安装的工具
	uv tool list

# uv 环境管理
create-env: ## 创建新的虚拟环境
	uv venv --python 3.12

activate-env: ## 显示激活环境的命令
	@echo "运行以下命令激活环境:"
	@echo "source .venv/bin/activate"

python-versions: ## 显示可用的 Python 版本
	uv python list

install-python: ## 安装指定 Python 版本 (用法: make install-python VERSION=3.11)
	uv python install $(VERSION)

# 项目管理
add-dep: ## 添加依赖 (用法: make add-dep DEP=requests)
	uv add $(DEP)

add-dev-dep: ## 添加开发依赖 (用法: make add-dev-dep DEP=pytest)
	uv add --dev $(DEP)

remove-dep: ## 移除依赖 (用法: make remove-dep DEP=requests)
	uv remove $(DEP)

show-deps: ## 显示依赖树
	uv tree

# 扩展功能开发
setup-multi-ai: ## 设置多 AI API 支持
	uv run scripts/setup_multi_ai.py

test-ai-providers: ## 测试所有 AI 提供商连接
	uv run scripts/setup_multi_ai.py

setup-web-dev: ## 设置 Web 开发环境
	uv add fastapi uvicorn jinja2 python-multipart
	uv add --dev pytest-asyncio httpx

setup-database: ## 设置数据库支持
	uv add sqlalchemy asyncpg alembic
	uv add --dev pytest-postgresql

setup-recommendation: ## 设置推荐系统依赖
	uv add scikit-learn numpy pandas transformers
	uv add --dev jupyter notebook

setup-graph-analysis: ## 设置图分析依赖
	uv add networkx pyvis matplotlib plotly
	uv add --dev graphviz

setup-mobile-dev: ## 设置移动端开发环境
	@echo "请参考 EXTENSION_ROADMAP.md 中的移动端开发指南"
	@echo "需要安装 React Native CLI 和相关工具"

# 扩展功能测试
test-recommendation: ## 测试推荐系统
	uv run scripts/test_recommendation.py

test-trend-analysis: ## 测试趋势分析
	uv run scripts/test_trend_analysis.py

test-graph-builder: ## 测试图谱构建
	uv run scripts/test_graph_builder.py

# 开发环境设置
setup-full-dev: setup-multi-ai setup-web-dev setup-database setup-recommendation setup-graph-analysis ## 设置完整开发环境

# 扩展功能部署
deploy-web: ## 部署 Web 界面
	@echo "构建 Web 应用..."
	cd web && npm run build
	@echo "部署到 GitHub Pages..."

deploy-api: ## 部署 API 服务
	@echo "构建 API 容器..."
	docker build -t arxiv-tracker-api .
	@echo "部署 API 服务..."

# 性能和缓存
cache-info: ## 显示缓存信息
	@echo "缓存目录:"
	uv cache dir
	@echo "缓存内容:"
	ls -la $$(uv cache dir) 2>/dev/null || echo "缓存目录为空"

clean-cache: ## 清理 uv 缓存
	uv cache clean

# 发布相关
check-build: ## 检查构建配置
	uv build --check

build-wheel: ## 构建 wheel 包
	uv build --wheel

build-sdist: ## 构建源码包
	uv build --sdist 