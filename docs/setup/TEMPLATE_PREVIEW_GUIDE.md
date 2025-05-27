# 📧 邮件模板预览指南

本指南介绍如何预览Hermes4ArXiv的HTML邮件模板效果。

## ⚠️ 重要说明

**GitHub限制**：由于GitHub的安全限制，README中无法直接预览HTML模板效果。因此我们提供了本地预览方案，让您在开发环境中完美查看模板效果。

## 🎯 预览方式

### 方式一：生成静态HTML文件（推荐）

```bash
# 生成预览文件
make preview-template

# 或直接运行脚本
cd src && python preview_template.py
```

**特点**：
- ✅ 快速生成，无需服务器
- ✅ 可以保存预览文件
- ✅ 支持自动打开浏览器（在支持的环境中）

### 方式二：HTTP服务器预览

```bash
# 启动预览服务器
make preview-server

# 或直接运行脚本
cd src && python preview_server.py
```

**特点**：
- ✅ 真实的HTTP环境
- ✅ 自动端口检测（8000-8009）
- ✅ 支持实时刷新
- ✅ 更接近真实邮件客户端效果

## 🔧 使用说明

### 基本用法

1. **生成预览**：
   ```bash
   make preview-template
   ```

2. **查看结果**：
   - 预览文件位置：`src/template_preview.html`
   - 在浏览器中打开该文件即可查看效果

### 高级用法

1. **启动预览服务器**：
   ```bash
   make preview-server
   ```

2. **访问预览**：
   - 服务器地址：`http://localhost:8000`
   - 预览页面：`http://localhost:8000/template_preview.html`

3. **停止服务器**：
   - 按 `Ctrl+C` 停止服务器

### 命令行参数

```bash
# 跳过自动打开浏览器
python src/preview_template.py --no-browser
python src/preview_server.py --no-browser
```

## 📱 预览内容

预览包含以下模拟数据：

### 📊 邮件概览
- **日期**：当前日期
- **论文数量**：3篇示例论文
- **研究领域**：cs.CV, cs.AI, cs.CL, cs.LG, quant-ph, q-bio.BM

### 📄 示例论文
1. **Hard Negative Contrastive Learning for Fine-Grained Geometric Understanding**
   - 多模态模型几何理解
   - 完整的五维AI分析

2. **Efficient Neural Architecture Search for Transformer-based Language Models**
   - 神经架构搜索优化
   - 性能提升数据展示

3. **Quantum-Enhanced Machine Learning for Drug Discovery**
   - 量子机器学习应用
   - 跨学科研究展示

## 🎨 模板特色

### 🏛️ 古典神话风格
- **赫尔墨斯主题**：智慧信使的神话元素
- **优雅配色**：紫色渐变主题
- **诗意化表达**：古典化的术语和描述

### 📱 响应式设计
- **桌面优化**：完美的大屏显示效果
- **移动适配**：手机和平板友好
- **邮件兼容**：主流邮件客户端支持

### ✨ 交互效果
- **悬停动画**：卡片悬停效果
- **渐变背景**：动态色彩变化
- **图标装饰**：丰富的视觉元素

## 🔧 自定义预览

### 修改模拟数据

编辑 `src/preview_template.py` 中的 `papers_data` 变量：

```python
papers_data = [
    {
        "title": "您的论文标题",
        "authors": "作者列表",
        "published": "发布日期",
        "categories": ["研究领域"],
        "url": "论文链接",
        "pdf_url": "PDF链接",
        "analysis": "AI分析内容（HTML格式）"
    }
]
```

### 修改模板样式

编辑 `src/templates/email_template.html` 文件：
- CSS样式在 `<style>` 标签内
- HTML结构使用Jinja2模板语法
- 修改后重新生成预览即可看到效果

## 🐛 常见问题

### Q: 预览文件生成失败？
**A**: 检查以下项目：
- 确保在项目根目录运行命令
- 检查 `src/templates/email_template.html` 文件是否存在
- 确保安装了 `jinja2` 依赖

### Q: 浏览器无法自动打开？
**A**: 这是正常现象，特别是在WSL或服务器环境中：
- 手动复制文件路径到浏览器
- 或使用预览服务器方式：`make preview-server`

### Q: HTTP服务器启动失败？
**A**: 可能的原因：
- 端口被占用：脚本会自动尝试其他端口
- 权限问题：确保有读写权限
- 防火墙阻止：检查本地防火墙设置

### Q: 预览效果与实际邮件不同？
**A**: 这是正常现象：
- 不同邮件客户端的CSS支持不同
- 预览使用现代浏览器渲染
- 实际邮件可能有额外的安全限制

## 💡 开发建议

1. **模板开发流程**：
   ```bash
   # 1. 修改模板
   vim src/templates/email_template.html
   
   # 2. 生成预览
   make preview-template
   
   # 3. 查看效果
   # 在浏览器中打开 src/template_preview.html
   
   # 4. 重复调整
   ```

2. **样式调试**：
   - 使用浏览器开发者工具
   - 实时修改CSS查看效果
   - 将满意的样式复制回模板文件

3. **兼容性测试**：
   - 在不同浏览器中测试
   - 使用邮件客户端预览工具
   - 发送测试邮件验证效果

---

🏛️ **愿赫尔墨斯的智慧指引您创造出完美的邮件模板！** 