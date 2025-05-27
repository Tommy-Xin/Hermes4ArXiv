#!/usr/bin/env python3
"""
修复 .env 文件中的编码问题
清理Gmail应用专用密码中的不间断空格等特殊字符
"""

import os
import shutil
from pathlib import Path

def clean_string(value):
    """清理字符串中的特殊字符"""
    if not value:
        return value
    # 移除不间断空格和其他不可见字符
    cleaned = value.replace('\xa0', ' ')  # 不间断空格
    cleaned = cleaned.replace('\u2000', ' ')  # en quad
    cleaned = cleaned.replace('\u2001', ' ')  # em quad
    cleaned = cleaned.replace('\u2002', ' ')  # en space
    cleaned = cleaned.replace('\u2003', ' ')  # em space
    cleaned = cleaned.replace('\u2004', ' ')  # three-per-em space
    cleaned = cleaned.replace('\u2005', ' ')  # four-per-em space
    cleaned = cleaned.replace('\u2006', ' ')  # six-per-em space
    cleaned = cleaned.replace('\u2007', ' ')  # figure space
    cleaned = cleaned.replace('\u2008', ' ')  # punctuation space
    cleaned = cleaned.replace('\u2009', ' ')  # thin space
    cleaned = cleaned.replace('\u200A', ' ')  # hair space
    cleaned = cleaned.replace('\u200B', '')   # zero width space
    cleaned = cleaned.replace('\u200C', '')   # zero width non-joiner
    cleaned = cleaned.replace('\u200D', '')   # zero width joiner
    cleaned = cleaned.replace('\u2060', '')   # word joiner
    cleaned = cleaned.replace('\uFEFF', '')   # zero width no-break space
    return cleaned.strip()

def detect_encoding_issues(file_path):
    """检测文件中的编码问题"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            original_line = line.rstrip('\n\r')
            cleaned_line = clean_string(original_line)
            
            if original_line != cleaned_line:
                issues.append({
                    'line_number': i,
                    'original': repr(original_line),
                    'cleaned': repr(cleaned_line),
                    'variable': original_line.split('=')[0] if '=' in original_line else 'unknown'
                })
    
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return []
    
    return issues

def fix_env_file(file_path):
    """修复 .env 文件中的编码问题"""
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 创建备份
    backup_path = file_path.with_suffix('.env.backup')
    shutil.copy2(file_path, backup_path)
    print(f"📁 已创建备份: {backup_path}")
    
    try:
        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 清理每一行
        cleaned_lines = []
        changes_made = False
        
        for i, line in enumerate(lines, 1):
            original_line = line.rstrip('\n\r')
            cleaned_line = clean_string(original_line)
            
            if original_line != cleaned_line:
                print(f"🔧 修复第 {i} 行:")
                print(f"   原始: {repr(original_line)}")
                print(f"   修复: {repr(cleaned_line)}")
                changes_made = True
            
            cleaned_lines.append(cleaned_line + '\n')
        
        if changes_made:
            # 写入修复后的文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
            
            print(f"✅ 文件已修复: {file_path}")
            return True
        else:
            print("✅ 文件没有编码问题")
            # 删除不必要的备份
            backup_path.unlink()
            return True
            
    except Exception as e:
        print(f"❌ 修复文件失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 .env 文件编码问题修复工具")
    print("=" * 50)
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ 未找到 .env 文件")
        print("💡 请先运行 'make setup-local-env' 创建环境文件")
        return
    
    print("🔍 检测编码问题...")
    issues = detect_encoding_issues(env_file)
    
    if not issues:
        print("✅ 未发现编码问题")
        return
    
    print(f"⚠️  发现 {len(issues)} 个编码问题:")
    for issue in issues:
        print(f"   第 {issue['line_number']} 行 ({issue['variable']}):")
        print(f"     原始: {issue['original']}")
        print(f"     建议: {issue['cleaned']}")
    
    print("\n" + "=" * 50)
    
    # 询问是否修复
    response = input("是否自动修复这些问题？(y/N): ").strip().lower()
    
    if response == 'y':
        if fix_env_file(env_file):
            print("\n🎉 修复完成！")
            print("💡 建议运行 'make validate-env-local' 验证修复结果")
        else:
            print("\n❌ 修复失败")
    else:
        print("❌ 取消修复")
        print("💡 您可以手动编辑 .env 文件来修复这些问题")

if __name__ == "__main__":
    main() 