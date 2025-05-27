#!/usr/bin/env python3
"""
GitHub Actions缓存问题诊断脚本
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


def check_github_status() -> Dict[str, str]:
    """检查GitHub服务状态"""
    print("🔍 检查GitHub服务状态...")
    
    try:
        # 尝试访问GitHub API
        result = subprocess.run(
            ["curl", "-s", "https://www.githubstatus.com/api/v2/status.json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            try:
                status_data = json.loads(result.stdout)
                return {
                    "status": status_data.get("status", {}).get("indicator", "unknown"),
                    "description": status_data.get("status", {}).get("description", "无法获取状态")
                }
            except json.JSONDecodeError:
                return {"status": "unknown", "description": "API响应解析失败"}
        else:
            return {"status": "error", "description": "无法连接到GitHub状态API"}
    
    except Exception as e:
        return {"status": "error", "description": f"检查失败: {str(e)}"}


def analyze_workflow_logs() -> Dict[str, any]:
    """分析工作流日志中的缓存问题"""
    print("📋 分析工作流配置...")
    
    project_root = Path(__file__).parent.parent
    workflows_dir = project_root / ".github" / "workflows"
    
    analysis = {
        "workflows_found": [],
        "cache_configurations": [],
        "potential_issues": []
    }
    
    if not workflows_dir.exists():
        analysis["potential_issues"].append("未找到.github/workflows目录")
        return analysis
    
    # 检查工作流文件
    for workflow_file in workflows_dir.glob("*.yml"):
        analysis["workflows_found"].append(workflow_file.name)
        
        try:
            content = workflow_file.read_text(encoding='utf-8')
            
            # 检查缓存配置
            if "actions/cache@" in content:
                analysis["cache_configurations"].append({
                    "file": workflow_file.name,
                    "has_cache": True,
                    "has_continue_on_error": "continue-on-error" in content,
                    "has_timeout": "timeout" in content
                })
            
            # 检查潜在问题
            if "enable-cache: true" in content and "continue-on-error" not in content:
                analysis["potential_issues"].append(
                    f"{workflow_file.name}: uv缓存启用但无容错处理"
                )
            
            if "actions/cache@" in content and "continue-on-error" not in content:
                analysis["potential_issues"].append(
                    f"{workflow_file.name}: 使用缓存但无容错处理"
                )
                
        except Exception as e:
            analysis["potential_issues"].append(f"读取{workflow_file.name}失败: {str(e)}")
    
    return analysis


def get_cache_recommendations() -> List[str]:
    """获取缓存优化建议"""
    return [
        "🔧 添加 continue-on-error: true 到缓存步骤",
        "⏱️ 为缓存操作设置合理的超时时间",
        "🔄 实现重试机制处理临时网络问题", 
        "📦 考虑使用分离的缓存恢复和保存步骤",
        "🚀 为关键步骤添加fallback机制",
        "📊 增加详细的日志记录便于诊断",
        "⚡ 考虑禁用缓存如果问题持续存在"
    ]


def check_recent_failures() -> Dict[str, any]:
    """检查最近的失败情况"""
    print("🔍 检查最近的运行情况...")
    
    # 这里可以扩展为检查GitHub API获取最近的运行记录
    # 目前提供基本的检查逻辑
    
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "src" / "logs"
    
    recent_info = {
        "has_local_logs": logs_dir.exists(),
        "log_files": [],
        "suggestions": []
    }
    
    if logs_dir.exists():
        log_files = list(logs_dir.glob("*.log"))
        recent_info["log_files"] = [f.name for f in log_files[-5:]]  # 最近5个日志
        
        if not log_files:
            recent_info["suggestions"].append("没有找到本地日志文件")
        else:
            recent_info["suggestions"].append(f"找到{len(log_files)}个日志文件")
    else:
        recent_info["suggestions"].append("本地logs目录不存在")
    
    return recent_info


def main():
    """主函数"""
    print("🔍 GitHub Actions缓存问题诊断工具")
    print("=" * 60)
    print(f"🕐 诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 检查GitHub服务状态
    github_status = check_github_status()
    print("📡 GitHub服务状态:")
    print(f"   状态: {github_status['status']}")
    print(f"   描述: {github_status['description']}")
    print()
    
    # 2. 分析工作流配置
    workflow_analysis = analyze_workflow_logs()
    print("📋 工作流分析:")
    print(f"   找到工作流: {len(workflow_analysis['workflows_found'])}")
    for wf in workflow_analysis['workflows_found']:
        print(f"     - {wf}")
    
    print(f"   缓存配置: {len(workflow_analysis['cache_configurations'])}")
    for cache_config in workflow_analysis['cache_configurations']:
        print(f"     - {cache_config['file']}: 缓存={cache_config['has_cache']}, "
              f"容错={cache_config['has_continue_on_error']}, "
              f"超时={cache_config['has_timeout']}")
    
    if workflow_analysis['potential_issues']:
        print("   ⚠️ 潜在问题:")
        for issue in workflow_analysis['potential_issues']:
            print(f"     - {issue}")
    print()
    
    # 3. 检查最近运行情况
    recent_info = check_recent_failures()
    print("📊 最近运行情况:")
    print(f"   本地日志: {'存在' if recent_info['has_local_logs'] else '不存在'}")
    if recent_info['log_files']:
        print("   最近日志文件:")
        for log_file in recent_info['log_files']:
            print(f"     - {log_file}")
    for suggestion in recent_info['suggestions']:
        print(f"   💡 {suggestion}")
    print()
    
    # 4. 提供解决建议
    print("💡 缓存优化建议:")
    recommendations = get_cache_recommendations()
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    print()
    
    # 5. 快速修复选项
    print("🚀 快速修复选项:")
    print("   1. 运行 'make fix-cache-issues' 使用交互式修复工具")
    print("   2. 手动切换到优化版本工作流")
    print("   3. 临时禁用缓存使用最小版本")
    print("   4. 等待GitHub服务恢复正常")
    print()
    
    # 6. 总结
    print("📝 诊断总结:")
    if github_status['status'] != 'none':
        print("   ⚠️ GitHub服务可能存在问题，建议等待恢复")
    
    if workflow_analysis['potential_issues']:
        print("   🔧 工作流配置需要优化")
        print("   💡 建议运行 'make fix-cache-issues' 进行修复")
    else:
        print("   ✅ 工作流配置看起来正常")
        print("   💡 问题可能是临时的网络或服务问题")
    
    print("\n🔗 相关资源:")
    print("   - GitHub状态页面: https://www.githubstatus.com/")
    print("   - Actions文档: https://docs.github.com/en/actions")
    print("   - 缓存文档: https://docs.github.com/en/actions/using-workflows/caching-dependencies")


if __name__ == "__main__":
    main() 