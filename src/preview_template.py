#!/usr/bin/env python3
"""
HTML模板预览生成器
用于预览邮件模板的效果
"""

import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def create_preview():
    """创建HTML模板预览"""
    
    # 设置模板环境
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("email_template.html")
    
    # 模拟数据
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    # 模拟论文数据
    papers_data = [
        {
            "title": "Hard Negative Contrastive Learning for Fine-Grained Geometric Understanding in Large Multimodal Models",
            "authors": "张三, 李四, 王五, John Smith, Jane Doe, Bob Wilson, Alice Chen",
            "published": "2025年05月26日",
            "categories": ["cs.CV", "cs.AI", "cs.CL"],
            "url": "https://arxiv.org/abs/2305.12345",
            "pdf_url": "https://arxiv.org/pdf/2305.12345.pdf",
            "analysis": """<div class="analysis-section">
    <div class="analysis-title">
        <span>🎯</span>
        1. 核心贡献
    </div>
    <div class="analysis-content">
        <p>本文提出了一种基于<strong>硬负样本对比学习</strong>的方法，显著提升了大型多模态模型在细粒度几何理解任务中的表现。主要创新点包括：设计了新颖的硬负样本挖掘策略，能够自动识别和利用最具挑战性的几何样本进行对比学习。</p>
    </div>
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>🔧</span>
        2. 技术方法
    </div>
    <div class="analysis-content">
        <p>采用了<em>多尺度特征融合</em>架构，结合了视觉Transformer和卷积神经网络的优势。通过引入几何感知的注意力机制，模型能够更好地理解空间关系和几何结构。</p>
    </div>
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>🧪</span>
        3. 实验验证
    </div>
    <div class="analysis-content">
        <p>在多个基准数据集上进行了全面评估，包括GQA、VQA-v2和自建的几何理解数据集。实验结果显示，相比现有方法，准确率提升了<strong>12.3%</strong>，在复杂几何推理任务上表现尤为突出。</p>
    </div>
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>💡</span>
        4. 影响与意义
    </div>
    <div class="analysis-content">
        <p>这项工作为多模态AI在几何理解方面提供了新的思路，对于机器人导航、建筑设计辅助、医学影像分析等应用领域具有重要价值。方法的通用性使其可以轻松集成到现有的多模态框架中。</p>
    </div>
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>🔮</span>
        5. 局限与展望
    </div>
    <div class="analysis-content">
        <p>当前方法在处理极其复杂的3D几何场景时仍有提升空间。未来工作将探索结合物理仿真的几何理解，以及在更大规模数据集上的扩展性验证。</p>
    </div>
</div>"""
        },
        {
            "title": "Efficient Neural Architecture Search for Transformer-based Language Models",
            "authors": "赵六, 钱七, 孙八, Maria Garcia, David Johnson",
            "published": "2025年05月25日", 
            "categories": ["cs.LG", "cs.CL"],
            "url": "https://arxiv.org/abs/2305.67890",
            "pdf_url": "https://arxiv.org/pdf/2305.67890.pdf",
            "analysis": """<div class="analysis-section">
    <div class="analysis-title">
        <span>🎯</span>
        1. 核心贡献
    </div>
    <div class="analysis-content">
        <p>提出了一种高效的神经架构搜索方法，专门针对Transformer语言模型进行优化。通过引入<strong>渐进式搜索策略</strong>和<code>动态剪枝机制</code>，将搜索时间减少了80%以上。</p>
    </div>
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>🔧</span>
        2. 技术方法
    </div>
    <div class="analysis-content">
        <p>核心技术包括：<em>可微分架构搜索</em>、权重共享机制、以及新颖的性能预测网络。方法能够在保持模型性能的同时，显著降低计算成本。</p>
    </div>
</div>"""
        }
    ]
    
    template_data = {
        "date": today,
        "paper_count": len(papers_data),
        "categories": "cs.CV, cs.AI, cs.CL, cs.LG",
        "papers": papers_data,
    }
    
    # 渲染模板
    html_content = template.render(**template_data)
    
    # 保存预览文件
    preview_file = Path(__file__).parent / "template_preview.html"
    with open(preview_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ HTML模板预览已生成: {preview_file}")
    print(f"🌐 在浏览器中打开查看效果: file://{preview_file.absolute()}")
    
    return preview_file

if __name__ == "__main__":
    create_preview() 