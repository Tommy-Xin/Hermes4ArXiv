#!/usr/bin/env python3
"""
工作流测试脚本
验证所有 GitHub Actions 工作流的配置和必要性
"""

import os
import yaml
from pathlib import Path

def analyze_workflow(workflow_path):
    """分析单个工作流文件"""
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = yaml.safe_load(f)
        
        name = workflow.get('name', '未命名')
        triggers = list(workflow.get('on', {}).keys())
        jobs = list(workflow.get('jobs', {}).keys())
        
        return {
            'name': name,
            'file': workflow_path.name,
            'triggers': triggers,
            'jobs': jobs,
            'job_count': len(jobs)
        }
    except Exception as e:
        return {
            'name': '解析失败',
            'file': workflow_path.name,
            'error': str(e)
        }

def check_workflow_necessity():
    """检查工作流的必要性"""
    workflows_dir = Path(__file__).parent.parent / '.github' / 'workflows'
    
    if not workflows_dir.exists():
        print("❌ 未找到 .github/workflows 目录")
        return
    
    workflows = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflows:
        print("❌ 未找到任何工作流文件")
        return
    
    print("🔍 分析工作流配置...")
    print("=" * 80)
    
    workflow_analysis = []
    
    for workflow_path in workflows:
        analysis = analyze_workflow(workflow_path)
        workflow_analysis.append(analysis)
        
        print(f"\n📄 {analysis['file']}")
        print(f"   名称: {analysis['name']}")
        
        if 'error' in analysis:
            print(f"   ❌ 错误: {analysis['error']}")
            continue
            
        print(f"   触发器: {', '.join(analysis['triggers'])}")
        print(f"   作业数: {analysis['job_count']}")
        print(f"   作业: {', '.join(analysis['jobs'])}")
    
    print("\n" + "=" * 80)
    print("📊 工作流总结:")
    
    # 分析必要性
    essential_workflows = []
    optional_workflows = []
    redundant_workflows = []
    
    for analysis in workflow_analysis:
        if 'error' in analysis:
            continue
            
        file_name = analysis['file']
        
        # 核心工作流
        if 'daily_paper_analysis' in file_name and 'enhanced' not in file_name:
            essential_workflows.append(analysis)
        # 设置向导
        elif 'setup' in file_name:
            essential_workflows.append(analysis)
        # 测试工作流
        elif 'test' in file_name:
            optional_workflows.append(analysis)
        # 质量检查
        elif 'quality' in file_name:
            optional_workflows.append(analysis)
        # 其他
        else:
            redundant_workflows.append(analysis)
    
    print(f"\n✅ 核心工作流 ({len(essential_workflows)} 个):")
    for wf in essential_workflows:
        print(f"   - {wf['file']}: {wf['name']}")
    
    print(f"\n🔧 可选工作流 ({len(optional_workflows)} 个):")
    for wf in optional_workflows:
        print(f"   - {wf['file']}: {wf['name']}")
    
    if redundant_workflows:
        print(f"\n⚠️  可能冗余的工作流 ({len(redundant_workflows)} 个):")
        for wf in redundant_workflows:
            print(f"   - {wf['file']}: {wf['name']}")

def check_secrets_usage():
    """检查工作流中使用的 Secrets"""
    workflows_dir = Path(__file__).parent.parent / '.github' / 'workflows'
    
    all_secrets = set()
    
    for workflow_path in workflows_dir.glob('*.yml'):
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找 secrets. 引用
            import re
            secrets_pattern = r'\$\{\{\s*secrets\.([A-Z_]+)\s*\}\}'
            matches = re.findall(secrets_pattern, content)
            all_secrets.update(matches)
            
        except Exception as e:
            print(f"⚠️  读取 {workflow_path.name} 失败: {e}")
    
    print("\n🔐 工作流中使用的 Secrets:")
    required_secrets = [
        'DEEPSEEK_API_KEY',
        'SMTP_SERVER',
        'SMTP_USERNAME', 
        'SMTP_PASSWORD',
        'EMAIL_FROM',
        'EMAIL_TO'
    ]
    
    for secret in sorted(all_secrets):
        status = "✅ 必需" if secret in required_secrets else "❓ 可选"
        print(f"   - {secret}: {status}")

def recommend_optimizations():
    """推荐优化建议"""
    print("\n💡 优化建议:")
    
    recommendations = [
        "1. 保留核心工作流：daily_paper_analysis.yml 和 setup-template.yml",
        "2. 测试工作流 (test.yml) 适合开发阶段，生产环境可选",
        "3. 质量检查工作流 (quality.yml) 适合代码贡献，个人使用可选",
        "4. 确保所有必需的 Secrets 都已在 GitHub 仓库中配置",
        "5. 定期检查工作流运行状态和日志",
        "6. 考虑设置工作流失败通知"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

def main():
    """主函数"""
    print("🔍 GitHub Actions 工作流分析")
    print("=" * 80)
    
    # 检查工作流必要性
    check_workflow_necessity()
    
    # 检查 Secrets 使用情况
    check_secrets_usage()
    
    # 推荐优化建议
    recommend_optimizations()
    
    print("\n🎉 分析完成！")

if __name__ == "__main__":
    main() 