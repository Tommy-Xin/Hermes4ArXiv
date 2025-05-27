#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "psutil>=5.9.0",
# ]
# ///
"""
项目状态报告脚本
显示项目的各种状态信息
"""

import subprocess
import sys
import os
from pathlib import Path
import psutil


def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode == 0
    except Exception as e:
        return str(e), False


def get_project_info():
    """获取项目基本信息"""
    print("📊 项目状态报告")
    print("=" * 50)
    
    # 项目基本信息
    project_root = Path(__file__).parent.parent
    print(f"📁 项目路径: {project_root}")
    print(f"🐍 Python 版本: {sys.version}")
    print(f"💻 操作系统: {sys.platform}")
    print(f"🔧 CPU 核心: {psutil.cpu_count()}")
    print(f"💾 内存: {psutil.virtual_memory().total / 1024**3:.1f} GB")
    print()


def get_uv_info():
    """获取 uv 相关信息"""
    print("⚡ uv 包管理器信息")
    print("-" * 30)
    
    # uv 版本
    version, success = run_command("uv --version")
    if success:
        print(f"📦 uv 版本: {version}")
    else:
        print("❌ uv 未安装或不可用")
        return
    
    # Python 版本管理
    python_list, success = run_command("uv python list")
    if success:
        installed_pythons = [line for line in python_list.split('\n') if 'cpython' in line]
        print(f"🐍 已安装 Python 版本: {len(installed_pythons)} 个")
    
    # 缓存信息
    cache_dir, success = run_command("uv cache dir")
    if success:
        print(f"📂 缓存目录: {cache_dir}")
        try:
            cache_size = sum(f.stat().st_size for f in Path(cache_dir).rglob('*') if f.is_file())
            print(f"💽 缓存大小: {cache_size / 1024**2:.1f} MB")
        except:
            print("💽 缓存大小: 无法计算")
    
    print()


def get_project_dependencies():
    """获取项目依赖信息"""
    print("📚 项目依赖信息")
    print("-" * 30)
    
    # 检查 pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        print("✅ pyproject.toml 存在")
        
        # 检查锁文件
        lock_path = Path(__file__).parent.parent / "uv.lock"
        if lock_path.exists():
            print("✅ uv.lock 存在")
            
            # 统计依赖数量
            tree_output, success = run_command("uv tree")
            if success:
                lines = tree_output.split('\n')
                total_packages = len([line for line in lines if '├──' in line or '└──' in line])
                print(f"📦 总依赖包数: {total_packages}")
        else:
            print("❌ uv.lock 不存在")
    else:
        print("❌ pyproject.toml 不存在")
    
    print()


def get_code_quality():
    """获取代码质量信息"""
    print("🔍 代码质量信息")
    print("-" * 30)
    
    project_root = Path(__file__).parent.parent
    
    # 统计代码行数
    python_files = list(project_root.rglob("*.py"))
    total_lines = 0
    for file in python_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    
    print(f"📄 Python 文件数: {len(python_files)}")
    print(f"📝 总代码行数: {total_lines}")
    
    # 检查测试覆盖率
    if (project_root / "tests").exists():
        test_files = list((project_root / "tests").rglob("test_*.py"))
        print(f"🧪 测试文件数: {len(test_files)}")
    else:
        print("🧪 测试文件数: 0")
    
    # 检查配置文件
    config_files = [
        ".pre-commit-config.yaml",
        "Makefile",

    ]
    
    existing_configs = [f for f in config_files if (project_root / f).exists()]
    print(f"⚙️  配置文件: {', '.join(existing_configs)}")
    
    print()


def get_git_info():
    """获取 Git 信息"""
    print("🔄 Git 版本控制信息")
    print("-" * 30)
    
    # 检查是否是 Git 仓库
    git_status, success = run_command("git status --porcelain")
    if not success:
        print("❌ 不是 Git 仓库")
        return
    
    # 当前分支
    branch, success = run_command("git branch --show-current")
    if success:
        print(f"🌿 当前分支: {branch}")
    
    # 提交统计
    commit_count, success = run_command("git rev-list --count HEAD")
    if success:
        print(f"📝 总提交数: {commit_count}")
    
    # 未提交的更改
    if git_status:
        modified_files = len(git_status.split('\n'))
        print(f"📋 未提交更改: {modified_files} 个文件")
    else:
        print("✅ 工作目录干净")
    
    print()


def get_performance_info():
    """获取性能信息"""
    print("⚡ 性能信息")
    print("-" * 30)
    
    # 检查虚拟环境
    venv_path = Path(__file__).parent.parent / ".venv"
    if venv_path.exists():
        print("✅ 虚拟环境存在")
        
        # 虚拟环境大小
        try:
            venv_size = sum(f.stat().st_size for f in venv_path.rglob('*') if f.is_file())
            print(f"💽 虚拟环境大小: {venv_size / 1024**2:.1f} MB")
        except:
            print("💽 虚拟环境大小: 无法计算")
    else:
        print("❌ 虚拟环境不存在")
    
    # 系统负载
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    print(f"🖥️  CPU 使用率: {cpu_percent:.1f}%")
    print(f"💾 内存使用率: {memory_percent:.1f}%")
    
    print()


def main():
    """主函数"""
    get_project_info()
    get_uv_info()
    get_project_dependencies()
    get_code_quality()
    get_git_info()
    get_performance_info()
    
    print("🎉 状态报告完成!")


if __name__ == "__main__":
    main() 