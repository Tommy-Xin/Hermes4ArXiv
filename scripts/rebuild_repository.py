#!/usr/bin/env python3
"""
仓库重建脚本
帮助将fork项目转换为独立的新仓库
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict


class RepositoryRebuilder:
    """仓库重建器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backup_dir = project_root.parent / f"{project_root.name}_backup"
        
    def analyze_current_state(self) -> Dict[str, any]:
        """分析当前仓库状态"""
        print("🔍 分析当前仓库状态...")
        
        analysis = {
            "git_status": {},
            "remote_info": {},
            "branch_info": {},
            "file_changes": {},
            "recommendations": []
        }
        
        try:
            # 检查git状态
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
                analysis["git_status"] = {
                    "modified_files": [line[3:] for line in lines if line.startswith(' M')],
                    "untracked_files": [line[3:] for line in lines if line.startswith('??')],
                    "total_changes": len(lines)
                }
            
            # 检查远程仓库信息
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                remotes = {}
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            name, url = parts[0], parts[1]
                            remotes[name] = url
                analysis["remote_info"] = remotes
            
            # 检查分支信息
            result = subprocess.run(
                ["git", "branch", "-a"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                branches = [line.strip().replace('* ', '') for line in result.stdout.strip().split('\n')]
                analysis["branch_info"] = {
                    "all_branches": branches,
                    "current_branch": next((b.replace('* ', '') for b in result.stdout.split('\n') if b.startswith('*')), 'unknown')
                }
            
        except Exception as e:
            print(f"⚠️ 分析过程中出现错误: {e}")
        
        return analysis
    
    def create_backup(self) -> bool:
        """创建当前项目的备份"""
        print("💾 创建项目备份...")
        
        try:
            if self.backup_dir.exists():
                print(f"⚠️ 备份目录已存在: {self.backup_dir}")
                response = input("是否覆盖现有备份？(y/N): ").strip().lower()
                if response != 'y':
                    print("❌ 取消备份操作")
                    return False
                shutil.rmtree(self.backup_dir)
            
            # 复制整个项目目录
            shutil.copytree(self.project_root, self.backup_dir)
            print(f"✅ 备份完成: {self.backup_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 备份失败: {e}")
            return False
    
    def commit_current_changes(self) -> bool:
        """提交当前所有更改"""
        print("📝 提交当前更改...")
        
        try:
            # 添加所有文件
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=True)
            
            # 提交更改
            commit_message = "🚀 项目重构完成 - 准备重建仓库\n\n包含以下主要改进:\n- 模块化架构重构\n- uv包管理器迁移\n- 并行处理优化\n- 缓存问题解决方案\n- 完整的文档体系"
            
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.project_root,
                check=True
            )
            
            print("✅ 更改提交完成")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 提交失败: {e}")
            return False
    
    def remove_fork_connection(self) -> bool:
        """移除fork连接，准备创建独立仓库"""
        print("🔗 移除fork连接...")
        
        try:
            # 移除原始远程仓库
            subprocess.run(["git", "remote", "remove", "origin"], cwd=self.project_root, check=True)
            print("✅ 已移除原始远程仓库连接")
            return True
            
        except subprocess.CalledProcessError:
            print("⚠️ 没有找到origin远程仓库或已经移除")
            return True
    
    def create_new_repository_guide(self) -> str:
        """创建新仓库设置指南"""
        guide_content = """# 新仓库设置指南

## 🚀 在GitHub上创建新仓库

1. **访问GitHub**: https://github.com/new
2. **仓库设置**:
   - 仓库名称: `arxiv-paper-tracker` (或您喜欢的名称)
   - 描述: `基于GitHub Actions的ArXiv论文自动追踪与AI分析工具`
   - 可见性: Public (推荐) 或 Private
   - **不要**初始化README、.gitignore或LICENSE (我们已经有了)

3. **创建后获取仓库URL**: 
   - HTTPS: `https://github.com/您的用户名/仓库名.git`
   - SSH: `git@github.com:您的用户名/仓库名.git`

## 🔗 连接本地仓库到新的远程仓库

```bash
# 添加新的远程仓库
git remote add origin https://github.com/您的用户名/仓库名.git

# 推送所有内容到新仓库
git push -u origin main

# 推送所有分支和标签
git push --all origin
git push --tags origin
```

## 📋 后续配置步骤

### 1. 配置GitHub Secrets
在新仓库中设置以下Secrets (Settings → Secrets and variables → Actions):

**必需配置**:
- `DEEPSEEK_API_KEY`: DeepSeek API密钥
- `SMTP_SERVER`: 邮件服务器 (如: smtp.gmail.com)
- `SMTP_PORT`: 邮件端口 (如: 587)
- `SMTP_USERNAME`: 邮箱用户名
- `SMTP_PASSWORD`: 邮箱应用专用密码
- `EMAIL_FROM`: 发件人邮箱
- `EMAIL_TO`: 收件人邮箱

### 2. 测试工作流
```bash
# 本地验证配置
make validate-env-local

# 手动触发GitHub Actions测试
# 在GitHub仓库页面: Actions → Daily Paper Analysis → Run workflow
```

### 3. 启用GitHub Pages (可选)
如果需要展示文档:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, Folder: /docs

## 🎯 项目特色

您的新仓库包含以下特色功能:
- 🤖 AI驱动的论文分析
- ⚡ 并行处理优化
- 📧 美化的HTML邮件报告
- 🔧 完善的错误处理和重试机制
- 📊 详细的性能监控
- 🛠️ 丰富的开发工具
- 📚 完整的文档体系

## 💡 推广建议

1. **添加项目标签**: AI, ArXiv, GitHub Actions, Python, uv
2. **编写项目介绍**: 突出AI分析和自动化特色
3. **添加演示截图**: 邮件报告、工作流运行等
4. **社区分享**: 可以分享到相关技术社区

---

**恭喜！** 您现在拥有了一个完全独立的、功能强大的ArXiv论文追踪项目！
"""
        
        guide_path = self.project_root / "NEW_REPOSITORY_SETUP_GUIDE.md"
        guide_path.write_text(guide_content, encoding='utf-8')
        return str(guide_path)
    
    def generate_project_summary(self) -> str:
        """生成项目总结"""
        summary = """# ArXiv论文追踪器 - 项目重建总结

## 🎉 项目转换完成

您的项目已成功从fork转换为独立仓库，包含以下重大改进：

### 🏗️ 架构重构
- ✅ 模块化设计，职责分离
- ✅ 现代化uv包管理器
- ✅ 完善的错误处理机制
- ✅ 详细的日志记录系统

### ⚡ 性能优化
- ✅ 并行论文分析处理
- ✅ 智能缓存策略
- ✅ 网络重试机制
- ✅ 资源使用优化

### 🎨 用户体验
- ✅ 美化的HTML邮件模板
- ✅ 响应式设计支持
- ✅ 详细的统计信息
- ✅ 专业的论文分析报告

### 🛠️ 开发体验
- ✅ 丰富的Makefile命令
- ✅ 自动化测试套件
- ✅ 代码质量检查
- ✅ 交互式配置向导

### 📚 文档体系
- ✅ 完整的部署指南
- ✅ 详细的故障排除文档
- ✅ 性能优化指南
- ✅ 扩展开发路线图

### 🔧 工具集合
- ✅ 环境验证脚本
- ✅ 缓存问题诊断工具
- ✅ 性能基准测试
- ✅ 项目状态监控

## 📊 项目统计

- **代码文件**: 20+ Python模块
- **配置文件**: 完整的pyproject.toml配置
- **工作流**: 优化的GitHub Actions
- **文档**: 15+ 详细指南
- **脚本**: 10+ 实用工具
- **测试**: 完整的pytest测试套件

## 🚀 下一步

1. **创建新GitHub仓库**
2. **配置必要的Secrets**
3. **测试工作流运行**
4. **享受自动化论文追踪！**

---

**这是一个完全属于您的独立项目，具有生产级别的质量和功能！**
"""
        
        summary_path = self.project_root / "PROJECT_REBUILD_SUMMARY.md"
        summary_path.write_text(summary, encoding='utf-8')
        return str(summary_path)
    
    def interactive_rebuild(self):
        """交互式重建流程"""
        print("🚀 ArXiv论文追踪器 - 仓库重建向导")
        print("=" * 60)
        
        # 1. 分析当前状态
        analysis = self.analyze_current_state()
        
        print("\n📊 当前仓库状态:")
        print(f"   - 修改的文件: {len(analysis['git_status'].get('modified_files', []))}")
        print(f"   - 未跟踪的文件: {len(analysis['git_status'].get('untracked_files', []))}")
        print(f"   - 当前分支: {analysis['branch_info'].get('current_branch', 'unknown')}")
        
        if analysis['remote_info']:
            print("   - 远程仓库:")
            for name, url in analysis['remote_info'].items():
                print(f"     {name}: {url}")
        
        # 2. 确认重建
        print("\n🔄 重建选项:")
        print("1. 完整重建 - 创建独立仓库 (推荐)")
        print("2. 保持fork关系 - 仅提交更改")
        print("3. 仅备份 - 不做其他操作")
        print("4. 取消操作")
        
        choice = input("\n请选择操作 (1-4): ").strip()
        
        if choice == "1":
            return self._full_rebuild()
        elif choice == "2":
            return self._commit_only()
        elif choice == "3":
            return self._backup_only()
        else:
            print("❌ 操作已取消")
            return False
    
    def _full_rebuild(self) -> bool:
        """执行完整重建"""
        print("\n🚀 开始完整重建流程...")
        
        # 1. 创建备份
        if not self.create_backup():
            return False
        
        # 2. 提交当前更改
        if not self.commit_current_changes():
            print("⚠️ 提交失败，但继续重建流程...")
        
        # 3. 移除fork连接
        if not self.remove_fork_connection():
            return False
        
        # 4. 创建指南
        guide_path = self.create_new_repository_guide()
        summary_path = self.generate_project_summary()
        
        print("\n✅ 重建完成！")
        print(f"📋 设置指南: {guide_path}")
        print(f"📊 项目总结: {summary_path}")
        
        print("\n🎯 下一步操作:")
        print("1. 在GitHub上创建新仓库")
        print("2. 按照设置指南连接远程仓库")
        print("3. 推送代码到新仓库")
        print("4. 配置GitHub Secrets")
        print("5. 测试工作流运行")
        
        return True
    
    def _commit_only(self) -> bool:
        """仅提交更改"""
        print("\n📝 提交当前更改...")
        return self.commit_current_changes()
    
    def _backup_only(self) -> bool:
        """仅创建备份"""
        print("\n💾 创建备份...")
        return self.create_backup()


def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    rebuilder = RepositoryRebuilder(project_root)
    
    print("🔧 ArXiv论文追踪器仓库重建工具")
    print("=" * 50)
    
    # 检查是否在正确的项目目录
    if not (project_root / ".git").exists():
        print("❌ 当前目录不是Git仓库，请在项目根目录运行")
        return
    
    # 运行交互式重建
    success = rebuilder.interactive_rebuild()
    
    if success:
        print("\n🎉 操作完成！")
        print("📚 查看生成的指南文件了解后续步骤")
    else:
        print("\n❌ 操作失败或被取消")


if __name__ == "__main__":
    main() 