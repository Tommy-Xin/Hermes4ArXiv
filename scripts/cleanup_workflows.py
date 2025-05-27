#!/usr/bin/env python3
"""
工作流清理脚本
帮助用户选择性删除不需要的工作流文件
"""

import os
import shutil
from pathlib import Path

def print_banner():
    """打印横幅"""
    print("🧹 GitHub Actions 工作流清理工具")
    print("=" * 50)
    print("帮助您删除不需要的工作流，节省 GitHub Actions 资源")
    print()

def analyze_workflows():
    """分析当前工作流"""
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print("❌ 未找到 .github/workflows 目录")
        return []
    
    workflows = []
    for file in workflows_dir.glob('*.yml'):
        workflows.append(file)
    
    return workflows

def show_workflow_info():
    """显示工作流信息"""
    print("📋 当前工作流分析:")
    print("-" * 30)
    
    workflows_info = {
        'daily_paper_analysis.yml': {
            'name': '📚 每日论文分析',
            'purpose': '核心功能 - 每天自动分析论文并发送邮件',
            'recommendation': '✅ 必须保留',
            'reason': '这是项目的主要功能'
        },
        'setup-template.yml': {
            'name': '🚀 配置向导',
            'purpose': '帮助新用户验证配置和测试',
            'recommendation': '✅ 建议保留',
            'reason': '对新用户和故障排除很有用'
        },
        'test.yml': {
            'name': '🧪 自动化测试',
            'purpose': '多平台、多版本测试 (9个矩阵任务)',
            'recommendation': '🔧 个人使用可删除',
            'reason': '消耗较多资源，个人使用意义不大'
        },
        'quality.yml': {
            'name': '🔍 代码质量检查',
            'purpose': '代码格式、类型检查、安全扫描',
            'recommendation': '🔧 个人使用可删除',
            'reason': '主要用于代码贡献和团队协作'
        }
    }
    
    workflows = analyze_workflows()
    
    for workflow in workflows:
        filename = workflow.name
        if filename in workflows_info:
            info = workflows_info[filename]
            print(f"📄 {info['name']} ({filename})")
            print(f"   用途: {info['purpose']}")
            print(f"   建议: {info['recommendation']}")
            print(f"   原因: {info['reason']}")
            print()

def get_user_choice():
    """获取用户选择"""
    print("🎯 清理选项:")
    print("1. 保留所有工作流（不做任何更改）")
    print("2. 删除测试工作流（test.yml）")
    print("3. 删除质量检查工作流（quality.yml）")
    print("4. 删除测试和质量检查工作流（推荐个人使用）")
    print("5. 自定义选择")
    print()
    
    while True:
        choice = input("请选择 (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("❌ 无效选择，请输入 1-5")

def delete_workflow(filename):
    """删除工作流文件"""
    workflow_path = Path('.github/workflows') / filename
    if workflow_path.exists():
        # 创建备份
        backup_dir = Path('.github/workflows_backup')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filename
        shutil.copy2(workflow_path, backup_path)
        
        # 删除原文件
        workflow_path.unlink()
        print(f"✅ 已删除 {filename}")
        print(f"📁 备份保存在: {backup_path}")
        return True
    else:
        print(f"⚠️  文件不存在: {filename}")
        return False

def custom_selection():
    """自定义选择"""
    workflows = analyze_workflows()
    optional_workflows = ['test.yml', 'quality.yml']
    
    print("🔧 可选删除的工作流:")
    for i, workflow in enumerate(optional_workflows, 1):
        if Path('.github/workflows') / workflow in workflows:
            print(f"{i}. {workflow}")
    
    print("\n请输入要删除的工作流编号（用逗号分隔，如: 1,2）:")
    selection = input("选择: ").strip()
    
    if not selection:
        print("❌ 未选择任何工作流")
        return []
    
    try:
        indices = [int(x.strip()) for x in selection.split(',')]
        selected_workflows = []
        for idx in indices:
            if 1 <= idx <= len(optional_workflows):
                selected_workflows.append(optional_workflows[idx-1])
            else:
                print(f"⚠️  无效编号: {idx}")
        return selected_workflows
    except ValueError:
        print("❌ 输入格式错误")
        return []

def execute_cleanup(choice):
    """执行清理"""
    workflows_to_delete = []
    
    if choice == '1':
        print("✅ 保留所有工作流")
        return
    elif choice == '2':
        workflows_to_delete = ['test.yml']
    elif choice == '3':
        workflows_to_delete = ['quality.yml']
    elif choice == '4':
        workflows_to_delete = ['test.yml', 'quality.yml']
    elif choice == '5':
        workflows_to_delete = custom_selection()
    
    if not workflows_to_delete:
        print("❌ 未选择要删除的工作流")
        return
    
    print(f"\n🗑️  准备删除以下工作流: {', '.join(workflows_to_delete)}")
    confirm = input("确认删除？(y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ 取消删除")
        return
    
    deleted_count = 0
    for workflow in workflows_to_delete:
        if delete_workflow(workflow):
            deleted_count += 1
    
    print(f"\n🎉 清理完成！删除了 {deleted_count} 个工作流")
    
    if deleted_count > 0:
        print("\n💡 后续步骤:")
        print("1. 提交更改: git add . && git commit -m '🧹 清理不需要的工作流'")
        print("2. 推送到 GitHub: git push")
        print("3. 检查 Actions 页面确认工作流已删除")

def show_resource_savings():
    """显示资源节省信息"""
    print("\n💰 资源节省说明:")
    print("-" * 30)
    print("删除 test.yml 可节省:")
    print("  - 每次推送: 9个任务 × 约5分钟 = 45分钟")
    print("  - 每月估计: 约200-500分钟（取决于推送频率）")
    print()
    print("删除 quality.yml 可节省:")
    print("  - 每次推送: 2个任务 × 约3分钟 = 6分钟")
    print("  - 每月估计: 约30-100分钟")
    print()
    print("GitHub Actions 免费额度:")
    print("  - 公共仓库: 无限制")
    print("  - 私有仓库: 每月2000分钟")

def main():
    """主函数"""
    print_banner()
    show_workflow_info()
    show_resource_savings()
    
    choice = get_user_choice()
    execute_cleanup(choice)

if __name__ == "__main__":
    main() 