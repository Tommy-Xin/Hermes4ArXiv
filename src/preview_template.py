#!/usr/bin/env python3
"""
HTML模板预览生成器
用于预览邮件模板的效果
"""

import datetime
import webbrowser
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def create_preview():
    """创建HTML模板预览"""
    
    try:
        # 设置模板环境
        templates_dir = Path(__file__).parent / "templates"
        if not templates_dir.exists():
            print(f"❌ 模板目录不存在: {templates_dir}")
            return None
            
        env = Environment(loader=FileSystemLoader(str(templates_dir)))
        
        try:
            template = env.get_template("email_template.html")
        except Exception as e:
            print(f"❌ 无法加载模板文件: {e}")
            return None
        
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
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>🧪</span>
        3. 实验验证
    </div>
    <div class="analysis-content">
        <p>在BERT、GPT等多个主流架构上验证了方法的有效性。实验表明，搜索得到的架构在保持相似性能的前提下，参数量减少了<strong>35%</strong>，推理速度提升了<strong>2.1倍</strong>。</p>
    </div>
</div>"""
            },
            {
                "title": "Quantum-Enhanced Machine Learning for Drug Discovery: A Comprehensive Survey",
                "authors": "周九, 吴十, 郑十一, Sarah Wilson, Michael Brown",
                "published": "2025年05月24日",
                "categories": ["quant-ph", "cs.LG", "q-bio.BM"],
                "url": "https://arxiv.org/abs/2305.11111",
                "pdf_url": "https://arxiv.org/pdf/2305.11111.pdf",
                "analysis": """<div class="analysis-section">
    <div class="analysis-title">
        <span>🎯</span>
        1. 核心贡献
    </div>
    <div class="analysis-content">
        <p>首次系统性地综述了<strong>量子增强机器学习</strong>在药物发现领域的应用。文章深入分析了量子计算在分子模拟、药物-靶点相互作用预测等关键任务中的优势和挑战。</p>
    </div>
</div>
<div class="analysis-section">
    <div class="analysis-title">
        <span>🔧</span>
        2. 技术方法
    </div>
    <div class="analysis-content">
        <p>详细介绍了<em>变分量子特征器</em>、量子核方法、以及混合量子-经典神经网络等前沿技术。特别关注了NISQ时代量子设备的实际应用可能性。</p>
    </div>
</div>"""
            }
        ]
        
        template_data = {
            "date": today,
            "paper_count": len(papers_data),
            "categories": "cs.CV, cs.AI, cs.CL, cs.LG, quant-ph, q-bio.BM",
            "papers": papers_data,
            "github_repo_url": "https://github.com/your-username/arxiv_paper_tracker"
        }
        
        # 渲染模板
        html_content = template.render(**template_data)
        
        # 保存预览文件
        preview_file = Path(__file__).parent / "template_preview.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ HTML模板预览已生成: {preview_file}")
        print(f"📄 文件大小: {preview_file.stat().st_size / 1024:.1f} KB")
        
        # 获取绝对路径用于浏览器
        file_url = f"file://{preview_file.absolute()}"
        print(f"🌐 浏览器访问地址: {file_url}")
        
        return preview_file, file_url
        
    except Exception as e:
        print(f"❌ 生成预览时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def open_in_browser(file_url):
    """在浏览器中打开预览文件"""
    try:
        print("🚀 正在尝试打开浏览器...")
        webbrowser.open(file_url)
        print("✅ 已在默认浏览器中打开预览")
    except Exception as e:
        print(f"⚠️ 无法自动打开浏览器: {e}")
        print("💡 请手动复制上面的地址到浏览器中查看")

def main():
    """主函数"""
    print("🏛️ Hermes4ArXiv 邮件模板预览生成器")
    print("=" * 50)
    
    result = create_preview()
    if result is None:
        print("❌ 预览生成失败")
        sys.exit(1)
    
    preview_file, file_url = result
    
    # 询问是否打开浏览器
    if len(sys.argv) > 1 and sys.argv[1] == "--no-browser":
        print("🔧 跳过浏览器打开（使用了 --no-browser 参数）")
    else:
        try:
            response = input("\n🌐 是否在浏览器中打开预览？(Y/n): ").strip().lower()
            if response in ['', 'y', 'yes', '是']:
                open_in_browser(file_url)
            else:
                print("💡 您可以手动打开上面的文件地址查看预览")
        except KeyboardInterrupt:
            print("\n👋 已取消")
        except EOFError:
            # 在非交互环境中自动打开
            open_in_browser(file_url)

if __name__ == "__main__":
    main() 