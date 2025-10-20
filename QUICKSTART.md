# 快速开始指南

## 🎯 立即修复和部署（3步）

### 步骤1：更新依赖

如果您在本地运行，需要先更新依赖：

```bash
# 清理旧的缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# 更新依赖
uv sync
```

### 步骤2：配置API密钥

#### 方案A：使用智谱GLM-4.6（推荐）

**优势：200K输入 + 128K输出，完美支持完整论文分析**

1. 访问 https://open.bigmodel.cn/
2. 注册并获取API密钥
3. 在GitHub仓库添加Secret：
   - 进入：Settings → Secrets and variables → Actions
   - 点击：New repository secret
   - 名称：`GLM_API_KEY`
   - 值：你的API密钥

#### 方案B：继续使用DeepSeek

如果您已经有DeepSeek的API密钥，无需任何修改，系统会自动使用它。

### 步骤3：推送更新并运行

```bash
# 提交所有更改
git add .
git commit -m "🔧 修复：支持智谱GLM，优化邮件模板，修复模块导入问题"
git push

# 手动触发一次运行测试
# 进入GitHub仓库 → Actions → Daily Paper Analysis → Run workflow
```

## 📧 邮件模板预览

新的邮件模板采用简洁设计：
- ✅ 清晰的标题和元信息
- ✅ 简洁的分类标签
- ✅ 易读的分析内容
- ✅ 优化的移动端显示
- ✅ 更快的加载速度

## 🔍 问题排查

### 问题1：还是出现 src.db 错误

**解决方案：**
```bash
# 彻底清理Python缓存
find . -type d -name "__pycache__" | xargs rm -rf
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# 重新提交
git add .
git commit -m "清理Python缓存"
git push
```

### 问题2：API调用失败

**检查清单：**
1. ✅ API密钥是否正确配置在GitHub Secrets中
2. ✅ API账户是否有足够余额
3. ✅ 密钥名称是否正确（`GLM_API_KEY` 或 `DEEPSEEK_API_KEY`）

### 问题3：没有收到邮件

**检查清单：**
1. ✅ 检查垃圾邮件文件夹
2. ✅ 确认邮件配置正确
3. ✅ 查看GitHub Actions运行日志

## 📊 运行日志查看

1. 进入GitHub仓库
2. 点击 Actions 标签
3. 选择最新的运行记录
4. 查看详细日志输出

## 🎉 成功标志

如果一切正常，您应该看到：
- ✅ GitHub Actions运行成功（绿色✓）
- ✅ 收到邮件推送
- ✅ 邮件内容简洁美观
- ✅ 论文分析质量良好

## 💡 进阶配置

查看 [高级配置指南](ADVANCED_CONFIG.md) 了解更多自定义选项。

## 🆘 需要帮助？

- 查看 [完整更新日志](CHANGELOG.md)
- 提交 [GitHub Issue](https://github.com/your-username/arxiv_paper_tracker/issues)
- 查看 GitHub Actions 运行日志
