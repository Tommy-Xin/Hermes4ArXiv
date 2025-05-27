#!/usr/bin/env python3
"""
文档整理脚本
将所有文档移动到docs文件夹，并识别和清理冗余文档
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Set


class DocumentOrganizer:
    """文档整理器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.docs_dir = project_root / "docs"
        
        # 确保docs目录存在
        self.docs_dir.mkdir(exist_ok=True)
        
        # 定义文档分类
        self.doc_categories = {
            "setup": [
                "DEPLOY_FOR_USERS.md",
                "GMAIL_SETUP_GUIDE.md", 
                "QUICK_START_SUMMARY.md",
                "SECURITY.md"
            ],
            "development": [
                "TESTING_GUIDE.md",
                "PARALLEL_OPTIMIZATION_GUIDE.md",
                "PARALLEL_OPTIMIZATION_SUMMARY.md"
            ],
            "extensions": [
                "EXTENSIONS_SUMMARY.md",
                "QUICK_START_EXTENSIONS.md", 
                "EXTENSION_ROADMAP.md"
            ],
            "project": [
                "PROJECT_CLEANUP_SUMMARY.md",
                "PROJECT_COMPLETION_SUMMARY.md"
            ]
        }
        
        # 需要保留在根目录的文档
        self.keep_in_root = {
            "README.md",
            "env.example",
            "Makefile",
            "pyproject.toml",
            "docker-compose.yml",
            "Dockerfile",
            ".pre-commit-config.yaml",
            ".gitignore"
        }

    def analyze_documents(self) -> Dict[str, List[str]]:
        """分析当前文档结构"""
        print("🔍 分析当前文档结构...")
        
        # 获取所有markdown文件
        md_files = list(self.project_root.glob("*.md"))
        
        analysis = {
            "total_docs": len(md_files),
            "categorized": [],
            "uncategorized": [],
            "duplicates": [],
            "existing_in_docs": []
        }
        
        # 检查docs目录中已有的文件
        existing_docs = list(self.docs_dir.glob("*.md"))
        analysis["existing_in_docs"] = [f.name for f in existing_docs]
        
        # 分类文档
        all_categorized = set()
        for category, files in self.doc_categories.items():
            all_categorized.update(files)
            
        for md_file in md_files:
            if md_file.name in self.keep_in_root:
                continue
                
            if md_file.name in all_categorized:
                analysis["categorized"].append(md_file.name)
            else:
                analysis["uncategorized"].append(md_file.name)
        
        # 检查重复文档
        for doc in analysis["categorized"]:
            if doc in analysis["existing_in_docs"]:
                analysis["duplicates"].append(doc)
        
        return analysis

    def identify_redundant_docs(self) -> List[str]:
        """识别冗余文档"""
        print("🔍 识别冗余文档...")
        
        redundant_docs = []
        
        # 检查内容相似的文档
        similar_pairs = [
            ("QUICK_START_SUMMARY.md", "DEPLOY_FOR_USERS.md"),
            ("EXTENSIONS_SUMMARY.md", "QUICK_START_EXTENSIONS.md"),
            ("PROJECT_CLEANUP_SUMMARY.md", "PROJECT_COMPLETION_SUMMARY.md"),
            ("PARALLEL_OPTIMIZATION_GUIDE.md", "PARALLEL_OPTIMIZATION_SUMMARY.md")
        ]
        
        for doc1, doc2 in similar_pairs:
            path1 = self.project_root / doc1
            path2 = self.project_root / doc2
            
            if path1.exists() and path2.exists():
                # 简单的内容重复检查
                content1 = path1.read_text(encoding='utf-8')
                content2 = path2.read_text(encoding='utf-8')
                
                # 如果一个文档的内容包含在另一个中，标记为冗余
                if len(content1) < len(content2) and content1[:200] in content2:
                    redundant_docs.append(doc1)
                elif len(content2) < len(content1) and content2[:200] in content1:
                    redundant_docs.append(doc2)
        
        return redundant_docs

    def create_docs_structure(self):
        """创建docs目录结构"""
        print("📁 创建docs目录结构...")
        
        # 创建子目录
        subdirs = ["setup", "development", "extensions", "project", "archive"]
        for subdir in subdirs:
            (self.docs_dir / subdir).mkdir(exist_ok=True)
            
        print(f"✅ 创建了以下子目录: {', '.join(subdirs)}")

    def move_documents(self, dry_run: bool = True):
        """移动文档到相应目录"""
        print(f"📦 {'模拟' if dry_run else '执行'}文档移动...")
        
        moved_files = []
        
        for category, files in self.doc_categories.items():
            target_dir = self.docs_dir / category
            
            for filename in files:
                source_path = self.project_root / filename
                target_path = target_dir / filename
                
                if source_path.exists():
                    if dry_run:
                        print(f"  📄 {filename} -> docs/{category}/")
                    else:
                        shutil.move(str(source_path), str(target_path))
                        print(f"  ✅ 移动: {filename} -> docs/{category}/")
                    moved_files.append(filename)
        
        return moved_files

    def archive_redundant_docs(self, redundant_docs: List[str], dry_run: bool = True):
        """归档冗余文档"""
        if not redundant_docs:
            print("✅ 没有发现冗余文档")
            return
            
        print(f"🗄️ {'模拟' if dry_run else '执行'}冗余文档归档...")
        
        archive_dir = self.docs_dir / "archive"
        
        for filename in redundant_docs:
            source_path = self.project_root / filename
            target_path = archive_dir / filename
            
            if source_path.exists():
                if dry_run:
                    print(f"  📦 {filename} -> docs/archive/")
                else:
                    shutil.move(str(source_path), str(target_path))
                    print(f"  ✅ 归档: {filename} -> docs/archive/")

    def create_docs_index(self):
        """创建文档索引"""
        print("📋 创建文档索引...")
        
        index_content = """# 文档索引

本目录包含ArXiv论文追踪器项目的所有文档。

## 📁 目录结构

### 🚀 setup/ - 部署和配置
- `DEPLOY_FOR_USERS.md` - 完整部署指南
- `GMAIL_SETUP_GUIDE.md` - Gmail配置指南
- `QUICK_START_SUMMARY.md` - 5分钟快速开始
- `SECURITY.md` - 安全保障说明

### 🔧 development/ - 开发和优化
- `TESTING_GUIDE.md` - 测试指南
- `PARALLEL_OPTIMIZATION_GUIDE.md` - 并行优化指南
- `PARALLEL_OPTIMIZATION_SUMMARY.md` - 并行优化总结

### 🚀 extensions/ - 扩展功能
- `EXTENSIONS_SUMMARY.md` - 扩展功能总结
- `QUICK_START_EXTENSIONS.md` - 扩展功能快速开始
- `EXTENSION_ROADMAP.md` - 扩展功能路线图

### 📊 project/ - 项目管理
- `PROJECT_CLEANUP_SUMMARY.md` - 项目清理总结
- `PROJECT_COMPLETION_SUMMARY.md` - 项目完成总结

### 🗄️ archive/ - 归档文档
存放已过时或冗余的文档。

## 🔗 快速链接

- **新用户**: 从 [快速开始](setup/QUICK_START_SUMMARY.md) 开始
- **部署**: 查看 [部署指南](setup/DEPLOY_FOR_USERS.md)
- **Gmail配置**: 参考 [Gmail设置](setup/GMAIL_SETUP_GUIDE.md)
- **性能优化**: 阅读 [并行优化指南](development/PARALLEL_OPTIMIZATION_GUIDE.md)
- **扩展功能**: 探索 [扩展路线图](extensions/EXTENSION_ROADMAP.md)

## 📝 文档维护

文档按功能分类组织，便于查找和维护。如需添加新文档，请放入相应的分类目录。
"""
        
        index_path = self.docs_dir / "README.md"
        index_path.write_text(index_content, encoding='utf-8')
        print(f"✅ 创建文档索引: {index_path}")

    def update_root_readme(self):
        """更新根目录README中的文档链接"""
        print("📝 更新根目录README...")
        
        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            print("⚠️ README.md不存在，跳过更新")
            return
            
        content = readme_path.read_text(encoding='utf-8')
        
        # 更新文档链接
        replacements = {
            "DEPLOY_FOR_USERS.md": "docs/setup/DEPLOY_FOR_USERS.md",
            "GMAIL_SETUP_GUIDE.md": "docs/setup/GMAIL_SETUP_GUIDE.md", 
            "TESTING_GUIDE.md": "docs/development/TESTING_GUIDE.md",
            "PARALLEL_OPTIMIZATION_GUIDE.md": "docs/development/PARALLEL_OPTIMIZATION_GUIDE.md",
            "SECURITY.md": "docs/setup/SECURITY.md",
            "QUICK_START_SUMMARY.md": "docs/setup/QUICK_START_SUMMARY.md"
        }
        
        for old_link, new_link in replacements.items():
            content = content.replace(f"]({old_link})", f"]({new_link})")
            content = content.replace(f"](/{old_link})", f"]({new_link})")
        
        readme_path.write_text(content, encoding='utf-8')
        print("✅ 更新了README中的文档链接")

    def run_organization(self, dry_run: bool = True):
        """运行完整的文档整理流程"""
        print("🚀 开始文档整理流程")
        print("=" * 50)
        
        # 1. 分析当前文档
        analysis = self.analyze_documents()
        print(f"📊 文档分析结果:")
        print(f"  - 总文档数: {analysis['total_docs']}")
        print(f"  - 已分类: {len(analysis['categorized'])}")
        print(f"  - 未分类: {len(analysis['uncategorized'])}")
        print(f"  - docs中已有: {len(analysis['existing_in_docs'])}")
        
        if analysis['uncategorized']:
            print(f"  - 未分类文档: {', '.join(analysis['uncategorized'])}")
        
        # 2. 识别冗余文档
        redundant_docs = self.identify_redundant_docs()
        if redundant_docs:
            print(f"🔍 发现冗余文档: {', '.join(redundant_docs)}")
        
        # 3. 创建目录结构
        self.create_docs_structure()
        
        # 4. 移动文档
        moved_files = self.move_documents(dry_run)
        
        # 5. 归档冗余文档
        self.archive_redundant_docs(redundant_docs, dry_run)
        
        # 6. 创建索引
        if not dry_run:
            self.create_docs_index()
            self.update_root_readme()
        
        print("=" * 50)
        if dry_run:
            print("✅ 模拟运行完成！使用 --execute 参数执行实际操作")
        else:
            print("✅ 文档整理完成！")
            print(f"📁 文档已整理到 docs/ 目录")
            print(f"📋 查看 docs/README.md 了解新的文档结构")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="整理项目文档")
    parser.add_argument("--execute", action="store_true", help="执行实际操作（默认为模拟运行）")
    parser.add_argument("--project-root", type=Path, default=Path.cwd().parent, help="项目根目录")
    
    args = parser.parse_args()
    
    organizer = DocumentOrganizer(args.project_root)
    organizer.run_organization(dry_run=not args.execute)


if __name__ == "__main__":
    main() 