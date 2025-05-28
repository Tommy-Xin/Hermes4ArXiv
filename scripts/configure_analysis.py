#!/usr/bin/env python3
"""
ArXiv论文分析配置助手 - GitHub Actions专用
快速配置部署到GitHub Actions的参数
"""

import sys
from pathlib import Path

def main():
    """交互式配置主函数"""
    
    print("🚀 ArXiv 论文分析器 - GitHub Actions配置助手")
    print("=" * 60)
    print("快速配置，3分钟部署到GitHub Actions！")
    
    # 用户需求调研
    print("\n📊 请回答几个问题，帮您选择最佳配置：")
    
    # 问题1：论文数量
    print("\n1. 您通常需要分析多少篇论文？")
    print("   a) 10-30篇（日常跟踪，推荐）")
    print("   b) 50-80篇（深度调研）") 
    print("   c) 100+篇（全面分析）")
    
    paper_count = input("请选择 (a/b/c): ").lower().strip()
    
    # 问题2：分析深度需求
    print("\n2. 您更偏好哪种分析风格？")
    print("   a) 简洁明了，快速浏览核心信息")
    print("   b) 全面平衡，适中的详细程度（推荐）") 
    print("   c) 深度详细，丰富技术分析")
    
    detail_need = input("请选择 (a/b/c): ").lower().strip()
    
    # 问题3：研究领域
    print("\n3. 主要关注的研究领域？")
    print("   a) AI核心（AI + 机器学习 + NLP）")
    print("   b) AI扩展（+ 计算机视觉 + 信息检索）")
    print("   c) 全计算机科学（理论 + 系统 + 应用）")
    
    field = input("请选择 (a/b/c): ").lower().strip()
    
    # 生成推荐配置
    config = generate_simple_config(paper_count, detail_need, field)
    
    print("\n" + "="*60)
    print("🎯 推荐的GitHub Secrets配置：")
    print("="*60)
    
    print(f"\n📋 GitHub Secrets配置项：")
    print("（在仓库Settings → Secrets and variables → Actions中添加）")
    print()
    
    # 必需配置
    print("🔑 必需配置（必须添加）：")
    print("   DEEPSEEK_API_KEY=sk-your-deepseek-api-key")
    print("   SMTP_USERNAME=your-email@gmail.com") 
    print("   SMTP_PASSWORD=your-app-password")
    print("   EMAIL_TO=recipient@gmail.com")
    
    # 可选优化配置
    print(f"\n⚙️ 可选优化配置：")
    for key, value in config.items():
        print(f"   {key}={value}")
    
    print(f"\n💡 配置说明：")
    print(f"   • 分析类型：{get_analysis_description(config['ANALYSIS_TYPE'])}")
    print(f"   • 研究领域：{get_field_description(config['CATEGORIES'])}")
    print(f"   • 预估成本：{estimate_cost(config)}")
    
    print(f"\n📝 部署步骤：")
    print("   1. Fork 本仓库到您的GitHub账号")
    print("   2. 在Settings → Secrets中添加上述配置")
    print("   3. 启用Actions，系统将每日自动运行")
    
    # 生成配置文件
    print("\n📄 是否生成完整的环境变量参考文件？")
    if input("输入 y 生成参考文件: ").lower().strip() == 'y':
        generate_reference_file(config)
        print("✅ 参考文件已生成：github_secrets_reference.md")

def generate_simple_config(paper_count, detail_need, field):
    """生成简化配置"""
    
    config = {}
    
    # 分析类型
    if detail_need == 'a':
        config["ANALYSIS_TYPE"] = "quick"
    elif detail_need == 'c':
        config["ANALYSIS_TYPE"] = "detailed"
    else:
        config["ANALYSIS_TYPE"] = "comprehensive"
    
    # 论文数量
    if paper_count == 'a':
        config["MAX_PAPERS"] = "30"
    elif paper_count == 'c':
        config["MAX_PAPERS"] = "120"
    else:
        config["MAX_PAPERS"] = "60"
    
    # 研究领域
    if field == 'a':
        config["CATEGORIES"] = "cs.AI,cs.LG,cs.CL"
    elif field == 'b':
        config["CATEGORIES"] = "cs.AI,cs.LG,cs.CL,cs.CV,cs.IR"
    else:
        config["CATEGORIES"] = "cs.AI,cs.LG,cs.CL,cs.CV,cs.DC,cs.DS"
    
    # 性能优化
    config["ENABLE_PARALLEL"] = "true"
    if int(config["MAX_PAPERS"]) > 50:
        config["MAX_WORKERS"] = "6"
    else:
        config["MAX_WORKERS"] = "4"
    
    return config

def get_analysis_description(analysis_type):
    """获取分析类型描述"""
    descriptions = {
        "quick": "简洁分析，200-300字，突出核心要点",
        "comprehensive": "全面分析，400-600字，平衡详细度", 
        "detailed": "深度分析，600-900字，丰富技术细节"
    }
    return descriptions.get(analysis_type, "未知类型")

def get_field_description(categories):
    """获取研究领域描述"""
    if "cs.DC" in categories:
        return "全计算机科学领域"
    elif "cs.CV" in categories:
        return "AI扩展领域（含CV和IR）"
    else:
        return "AI核心领域（AI、ML、NLP）"

def estimate_cost(config):
    """预估API成本"""
    papers = int(config["MAX_PAPERS"])
    analysis_type = config["ANALYSIS_TYPE"]
    
    base_cost = {
        "quick": 0.008,
        "comprehensive": 0.012,
        "detailed": 0.016
    }
    
    cost = papers * base_cost.get(analysis_type, 0.012)
    return f"约 ¥{cost:.2f} / 次运行"

def generate_reference_file(config):
    """生成GitHub Secrets参考文件"""
    
    content = f"""# GitHub Secrets 配置参考
根据配置助手生成的推荐配置

## 🔑 必需配置（必须添加到GitHub Secrets）

### DeepSeek API配置
```
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
```
获取地址：https://platform.deepseek.com/

### 邮件配置
```
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password  
EMAIL_TO=recipient@gmail.com
```
Gmail设置指南：docs/setup/GMAIL_SETUP_GUIDE.md

## ⚙️ 推荐的优化配置（可选）

### 分析配置
```
ANALYSIS_TYPE={config['ANALYSIS_TYPE']}
MAX_PAPERS={config['MAX_PAPERS']}
CATEGORIES={config['CATEGORIES']}
```

### 性能配置
```
ENABLE_PARALLEL={config['ENABLE_PARALLEL']}
MAX_WORKERS={config['MAX_WORKERS']}
```

## 📝 部署步骤

1. **Fork仓库**：将本仓库Fork到您的GitHub账号
2. **配置Secrets**：在仓库Settings → Secrets and variables → Actions中添加上述配置
3. **启用Actions**：GitHub Actions将每日北京时间8:00自动运行
4. **查看结果**：检查邮箱接收分析报告

## 📚 更多配置选项

详细配置说明：ADVANCED_CONFIG.md
DeepSeek配置：docs/setup/DEEPSEEK_SETUP_GUIDE.md
Gmail设置：docs/setup/GMAIL_SETUP_GUIDE.md
"""
    
    with open("github_secrets_reference.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main() 