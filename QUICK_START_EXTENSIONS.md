# 🚀 扩展功能快速开始指南

本指南将帮助您快速开始实施 ArXiv 论文追踪器的扩展功能。

## 📋 前提条件

确保您已经完成了基础项目的设置：

```bash
# 检查基础环境
make validate-env
make test-components
make status
```

## 🎯 第一阶段：多 AI API 支持 (推荐优先实施)

### 1. 快速设置

```bash
# 一键设置多 AI 支持
make setup-multi-ai
```

这个命令会：
- 检查当前 API 密钥配置
- 测试各个 AI 提供商连接
- 生成配置建议
- 创建多 AI 分析器代码

### 2. 配置 API 密钥

根据脚本输出，在 `.env` 文件中添加：

```bash
# 必需 (已有)
DEEPSEEK_API_KEY=sk-your-deepseek-key

# 可选 - 添加更多 AI 提供商
OPENAI_API_KEY=sk-your-openai-key
CLAUDE_API_KEY=sk-ant-your-claude-key
GEMINI_API_KEY=your-gemini-key

# 多 AI 配置
ANALYSIS_STRATEGY=fallback
AI_FALLBACK_ORDER=deepseek,openai,claude
```

### 3. 测试多 AI 功能

```bash
# 测试所有 AI 提供商
make test-ai-providers

# 运行基准测试
make benchmark
```

### 4. 集成到主程序

更新 `src/main.py` 使用新的多 AI 分析器：

```python
# 在 main.py 中替换原有的分析器
from ai_analyzer_v2 import MultiAIAnalyzer

# 初始化多 AI 分析器
config_dict = config.__dict__
analyzer = MultiAIAnalyzer(config_dict)

# 使用降级策略分析
for paper in papers:
    try:
        analysis = await analyzer.analyze_with_fallback(paper)
        print(f"✅ 使用 {analysis['provider']} 分析完成")
    except Exception as e:
        logger.error(f"分析失败: {e}")
```

## 🌐 第二阶段：Web 界面开发

### 1. 设置 Web 开发环境

```bash
# 安装 Web 开发依赖
make setup-web-dev
```

### 2. 创建基础 Web 应用

```bash
# 创建 Web 应用目录结构
mkdir -p web/{backend,frontend,static,templates}

# 创建 FastAPI 应用
cat > web/backend/main.py << 'EOF'
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

app = FastAPI(title="ArXiv 论文追踪器", version="2.0.0")

# 静态文件和模板
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/papers/recent")
async def get_recent_papers():
    # 这里集成现有的论文获取逻辑
    return {"papers": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

### 3. 运行 Web 应用

```bash
# 启动 Web 服务
cd web/backend && uv run python main.py

# 访问 http://localhost:8000
```

## 💾 第三阶段：数据库集成

### 1. 设置数据库环境

```bash
# 安装数据库依赖
make setup-database
```

### 2. 创建数据库模型

```bash
# 创建数据库目录
mkdir -p src/database

# 创建模型文件
cat > src/database/models.py << 'EOF'
from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Paper(Base):
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True)
    arxiv_id = Column(String(50), unique=True, nullable=False)
    title = Column(Text, nullable=False)
    authors = Column(ARRAY(String))
    categories = Column(ARRAY(String))
    summary = Column(Text)
    published_date = Column(DateTime)
    analysis_result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
EOF
```

### 3. 配置数据库连接

```bash
# 添加数据库配置到 .env
echo "DATABASE_URL=postgresql://user:password@localhost/arxiv_tracker" >> .env
```

## 🤖 第四阶段：智能推荐系统

### 1. 设置推荐系统

```bash
# 安装推荐系统依赖
make setup-recommendation
```

### 2. 创建推荐引擎

```bash
# 创建推荐系统目录
mkdir -p src/recommendation

# 创建基础推荐器
cat > src/recommendation/recommender.py << 'EOF'
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PaperRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.paper_vectors = None
        self.papers = []
    
    def fit(self, papers):
        """训练推荐模型"""
        self.papers = papers
        texts = [f"{paper.title} {paper.summary}" for paper in papers]
        self.paper_vectors = self.vectorizer.fit_transform(texts)
    
    def recommend(self, query_paper, top_k=5):
        """推荐相似论文"""
        if self.paper_vectors is None:
            return []
        
        query_text = f"{query_paper.title} {query_paper.summary}"
        query_vector = self.vectorizer.transform([query_text])
        
        similarities = cosine_similarity(query_vector, self.paper_vectors)[0]
        top_indices = np.argsort(similarities)[-top_k-1:-1][::-1]
        
        return [self.papers[i] for i in top_indices]
EOF
```

## 📈 第五阶段：趋势分析

### 1. 设置图分析环境

```bash
# 安装图分析依赖
make setup-graph-analysis
```

### 2. 创建趋势分析器

```bash
# 创建分析目录
mkdir -p src/analysis

# 创建趋势分析器
cat > src/analysis/trend_analyzer.py << 'EOF'
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import networkx as nx

class TrendAnalyzer:
    def __init__(self):
        self.keyword_history = defaultdict(list)
        self.author_networks = nx.Graph()
    
    def analyze_keywords(self, papers, time_window=30):
        """分析关键词趋势"""
        recent_date = datetime.now() - timedelta(days=time_window)
        recent_papers = [p for p in papers if p.published_date >= recent_date]
        
        # 提取关键词
        all_keywords = []
        for paper in recent_papers:
            # 简单的关键词提取（实际应用中可以使用更复杂的NLP）
            keywords = paper.title.lower().split() + paper.summary.lower().split()
            all_keywords.extend(keywords)
        
        # 统计频率
        keyword_counts = Counter(all_keywords)
        return keyword_counts.most_common(20)
    
    def build_collaboration_network(self, papers):
        """构建作者合作网络"""
        for paper in papers:
            authors = paper.authors
            # 为每对作者添加边
            for i in range(len(authors)):
                for j in range(i+1, len(authors)):
                    if self.author_networks.has_edge(authors[i], authors[j]):
                        self.author_networks[authors[i]][authors[j]]['weight'] += 1
                    else:
                        self.author_networks.add_edge(authors[i], authors[j], weight=1)
        
        return self.author_networks
EOF
```

## 🔧 完整开发环境设置

如果您想一次性设置所有扩展功能的开发环境：

```bash
# 设置完整开发环境（这会安装所有依赖）
make setup-full-dev
```

## 📊 测试扩展功能

### 运行各种测试

```bash
# 测试推荐系统
make test-recommendation

# 测试趋势分析
make test-trend-analysis

# 测试图谱构建
make test-graph-builder

# 运行完整测试套件
make test
```

## 🚀 部署扩展功能

### GitHub Actions 集成

更新 `.github/workflows/daily_paper_analysis_enhanced.yml` 以包含扩展功能：

```yaml
# 在分析作业中添加扩展功能测试
- name: Test extended features
  run: |
    echo "🧪 测试扩展功能..."
    make test-ai-providers
    make test-recommendation
    make test-trend-analysis
```

### 环境变量配置

在 GitHub Secrets 中添加新的环境变量：

```
# 多 AI 支持
OPENAI_API_KEY=sk-your-openai-key
CLAUDE_API_KEY=sk-ant-your-claude-key
GEMINI_API_KEY=your-gemini-key

# 分析策略
ANALYSIS_STRATEGY=fallback
AI_FALLBACK_ORDER=deepseek,openai,claude

# 数据库配置 (如果使用)
DATABASE_URL=postgresql://user:password@host/db
```

## 📈 监控和优化

### 性能监控

```bash
# 运行性能基准测试
make benchmark

# 查看缓存使用情况
make cache-info

# 生成项目状态报告
make status
```

### 日志分析

```bash
# 查看扩展功能日志
tail -f src/logs/multi_ai.log
tail -f src/logs/recommendation.log
tail -f src/logs/trend_analysis.log
```

## 🎯 下一步计划

### 短期目标 (1-2周)
1. ✅ 完成多 AI API 支持
2. 🔄 实现基础 Web 界面
3. 📊 添加简单的趋势分析

### 中期目标 (1个月)
1. 💾 集成数据库存储
2. 🤖 完善推荐系统
3. 🕸️ 构建论文关系图谱

### 长期目标 (3个月)
1. 📱 开发移动端应用
2. 🌍 添加多语言支持
3. 👥 构建社区功能

## 💡 开发建议

### 最佳实践
1. **渐进式开发**: 一次专注一个扩展功能
2. **测试驱动**: 每个功能都要有对应的测试
3. **文档更新**: 及时更新 README 和文档
4. **性能监控**: 定期运行基准测试

### 常见问题
1. **依赖冲突**: 使用 `uv tree` 检查依赖关系
2. **内存使用**: 大型模型可能需要更多内存
3. **API 限制**: 注意各个 AI 提供商的调用限制

---

**开始您的扩展功能开发之旅吧！** 🚀

如有任何问题，请参考 `EXTENSION_ROADMAP.md` 获取详细的技术实现方案。 