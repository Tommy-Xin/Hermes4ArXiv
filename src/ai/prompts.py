#!/usr/bin/env python3
"""
AI提示词管理模块
集中管理各种AI分析任务的提示词
"""

from typing import Dict, List
import arxiv
import logging


class PromptManager:
    """提示词管理器"""
    
    @staticmethod
    def get_system_prompt(analysis_type: str = "comprehensive") -> str:
        """
        获取系统提示词
        
        Args:
            analysis_type: 分析类型 (comprehensive, quick, detailed)
        
        Returns:
            系统提示词
        """
        prompts = {
            "comprehensive": PromptManager._get_comprehensive_system_prompt(),
            "quick": PromptManager._get_quick_system_prompt(),
            "detailed": PromptManager._get_detailed_system_prompt(),
        }
        
        return prompts.get(analysis_type, prompts["comprehensive"])
    
    @staticmethod
    def _get_comprehensive_system_prompt() -> str:
        """获取综合分析系统提示词"""
        return """你是一位世界顶级的学术论文分析专家，拥有计算机科学博士学位，专精于人工智能、机器学习、深度学习等前沿领域。你具备以下特质：

🎓 **专业背景**：
- 在顶级期刊和会议发表过多篇高影响因子论文
- 对AI/ML领域的最新发展有深刻理解
- 能够快速识别论文的创新点和技术价值

🔍 **分析能力**：
- 善于从技术、应用、理论三个维度评估论文
- 能够准确判断研究的实用性和前瞻性
- 擅长用通俗易懂的语言解释复杂概念

📝 **表达风格**：
- 使用专业但不失生动的中文表达
- 善于运用类比和比喻帮助理解
- 注重逻辑清晰和结构完整

**分析任务**：请按照以下六个维度深度分析论文，每个维度都要体现你的专业洞察：

**1. ⭐ 质量评估**
- 给出论文的整体质量评分（1-5星，可用半星）
- 评估创新程度（突破性/渐进性/跟随性）
- 评估技术严谨性（严谨/良好/一般）
- 评估实用价值（高/中/低）
- 简述你的整体评价和推荐理由

**2. 🎯 核心贡献**
- 用1-2句话精准概括论文的主要创新点
- 突出与现有工作的差异化优势
- 评估创新的技术难度和突破性

**3. 🔧 技术方法**
- 详细解析核心算法、架构或方法论
- 分析技术路线的合理性和先进性
- 指出关键技术细节和实现要点

**4. 🧪 实验验证**
- 评估实验设计的科学性和完整性
- 分析数据集选择和评估指标的合理性
- 解读关键实验结果和性能提升

**5. 💡 影响意义**
- 分析对学术界和工业界的潜在影响
- 评估在实际应用中的可行性和价值
- 预测可能催生的后续研究方向

**6. 🔮 局限展望**
- 客观指出研究的局限性和不足
- 分析可能的改进方向和扩展空间
- 预测未来发展趋势和挑战

**输出要求**：
- 每个维度控制在80-120字，总长度400-600字
- 使用专业术语但保持可读性
- 突出关键信息，避免冗余表述
- 保持客观中立，基于事实分析"""

    @staticmethod
    def _get_quick_system_prompt() -> str:
        """获取快速分析系统提示词"""
        return """你是一位经验丰富的AI研究员，需要快速而准确地分析学术论文。

请按照以下结构简洁分析：

1. **质量评估**：整体评分（1-5星）和简要评价
2. **核心贡献**：一句话概括主要创新
3. **技术亮点**：关键技术方法
4. **实验结果**：主要性能表现
5. **应用价值**：实际应用潜力
6. **发展前景**：未来改进方向

要求：
- 每点30-50字，总长度200-300字
- 突出重点，语言简洁
- 专业准确，易于理解"""

    @staticmethod
    def _get_detailed_system_prompt() -> str:
        """获取详细分析系统提示词"""
        return """你是一位资深的学术评审专家，需要对论文进行深度技术分析。

请提供详细的技术评估：

1. **质量评估**：整体评分（1-5星）、创新程度、技术严谨性、实用价值的详细评估
2. **创新性分析**：技术创新的深度和广度
3. **方法论评估**：算法设计的科学性和完整性
4. **实验分析**：实验设计、数据集、基线对比的充分性
5. **技术影响**：对相关技术领域的推动作用
6. **实用性评估**：工程实现的可行性和应用前景
7. **研究局限**：当前工作的不足和改进空间

要求：
- 每点100-150字，总长度600-900字
- 深入技术细节，提供专业见解
- 平衡优缺点，客观评价"""

    @staticmethod
    def get_user_prompt(paper: arxiv.Result, analysis_type: str = "comprehensive") -> str:
        """
        获取用户提示词
        
        Args:
            paper: 论文对象
            analysis_type: 分析类型
        
        Returns:
            用户提示词
        """
        # 提取作者信息 - 优先使用正常路径，异常时记录警告
        authors_str = '未知'
        if hasattr(paper, 'authors') and paper.authors:
            try:
                # 正常情况：直接使用 author.name
                author_names = [author.name for author in paper.authors]
                authors_str = ', '.join(author_names[:5])  # 最多显示5个作者
                if len(author_names) > 5:
                    authors_str += f" 等{len(author_names)}人"
            except AttributeError as e:
                # 异常情况：Author对象结构不正常（不应该发生）
                logger = logging.getLogger(__name__)
                logger.warning(f"⚠️ 检测到异常的Author对象结构: {e}")
                try:
                    # 备用方案：str()转换
                    author_names = [str(author) for author in paper.authors[:5]]
                    authors_str = ', '.join(author_names)
                    if len(paper.authors) > 5:
                        authors_str += f" 等{len(paper.authors)}人"
                    logger.info(f"✅ 使用str()转换成功获取作者信息")
                except Exception as e2:
                    logger.error(f"❌ 无法获取作者信息: {e2}")
                    authors_str = f'作者信息异常 ({len(paper.authors)} 位作者)'
        
        # 格式化发布时间 - 优先使用正常路径
        published_date = '未知'
        if hasattr(paper, 'published') and paper.published:
            try:
                published_date = paper.published.strftime('%Y年%m月%d日')
            except (AttributeError, ValueError) as e:
                logger = logging.getLogger(__name__)
                logger.warning(f"⚠️ 发布时间格式异常: {e}")
                published_date = str(paper.published)
        elif hasattr(paper, 'published'):
            # published字段存在但为None（不应该发生）
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ 检测到published字段为None")
        
        # 处理摘要长度
        summary = paper.summary.strip()
        if len(summary) > 1500:  # 如果摘要太长，截取前1500字符
            summary = summary[:1500] + "..."
        
        # 基础提示词模板
        base_prompt = f"""请分析以下ArXiv论文：

📄 **论文标题**：{paper.title}

👥 **作者信息**：{authors_str}

🏷️ **研究领域**：{', '.join(paper.categories)}

📅 **发布时间**：{published_date}

📝 **论文摘要**：
{summary}

🔗 **论文链接**：{paper.entry_id}

---

请基于以上信息，按照系统提示的结构进行深度分析。注意：
- 重点关注技术创新和实际应用价值
- 结合当前AI/ML领域的发展趋势
- 提供专业而易懂的分析见解"""

        # 根据分析类型添加特定要求
        if analysis_type == "quick":
            base_prompt += "\n\n⚡ **特别要求**：请提供简洁而精准的分析，突出最核心的要点。"
        elif analysis_type == "detailed":
            base_prompt += "\n\n🔬 **特别要求**：请提供深入的技术分析，包含详细的方法论评估和实验分析。"
        
        return base_prompt

    @staticmethod
    def get_fallback_prompt() -> str:
        """获取降级提示词（当API调用失败时使用）"""
        return """抱歉，AI分析服务暂时不可用。以下是基于论文标题和摘要的基础信息：

**论文概述**：这是一篇关于{categories}领域的研究论文，由{authors}等研究者发表。

**研究内容**：论文主要探讨了{title}相关的技术问题。

**技术价值**：该研究在相关领域具有一定的学术价值和应用潜力。

**建议**：建议读者查阅原文获取详细的技术内容和实验结果。

---
*注：本分析为自动生成的基础信息，详细技术分析请参考原文。*"""

    @staticmethod
    def get_error_analysis(error_msg: str) -> str:
        """获取错误分析信息"""
        return f"""**分析状态**：AI分析暂时不可用

**错误信息**：{error_msg}

**建议操作**：
1. 检查网络连接状态
2. 验证API密钥配置
3. 确认API服务可用性
4. 稍后重试分析

**论文价值**：尽管自动分析不可用，该论文仍值得关注。建议：
- 查阅论文原文了解详细内容
- 关注论文的引用情况和后续发展
- 结合相关领域的最新进展进行理解

---
*系统将在下次运行时重新尝试分析此论文。*"""

    @staticmethod
    def format_analysis_for_html(analysis_text: str) -> str:
        """
        将分析文本格式化为HTML
        
        Args:
            analysis_text: 原始分析文本
        
        Returns:
            格式化的HTML文本
        """
        if not analysis_text:
            return ""
        
        # 分割成段落
        lines = analysis_text.strip().split('\n')
        html_sections = []
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是新的分析维度
            if any(marker in line for marker in ['🎯', '🔧', '🧪', '💡', '🔮', '**1.', '**2.', '**3.', '**4.', '**5.']):
                # 保存上一个section
                if current_section and current_content:
                    html_sections.append(PromptManager._create_analysis_section(current_section, current_content))
                
                # 开始新的section
                current_section = line
                current_content = []
            else:
                # 添加到当前section的内容
                current_content.append(line)
        
        # 添加最后一个section
        if current_section and current_content:
            html_sections.append(PromptManager._create_analysis_section(current_section, current_content))
        
        return '\n'.join(html_sections)
    
    @staticmethod
    def _create_analysis_section(title: str, content: List[str]) -> str:
        """创建分析section的HTML"""
        # 提取emoji和标题
        if '🎯' in title:
            emoji = '🎯'
            section_title = '1. 核心贡献'
        elif '🔧' in title:
            emoji = '🔧'
            section_title = '2. 技术方法'
        elif '🧪' in title:
            emoji = '🧪'
            section_title = '3. 实验验证'
        elif '💡' in title:
            emoji = '💡'
            section_title = '4. 影响意义'
        elif '🔮' in title:
            emoji = '🔮'
            section_title = '5. 局限展望'
        else:
            # 尝试从标题中提取
            emoji = '📝'
            section_title = title.replace('*', '').strip()
        
        # 合并内容
        content_text = ' '.join(content).strip()
        
        # 处理文本格式
        content_text = PromptManager._format_text_content(content_text)
        
        return f'''<div class="analysis-section">
    <div class="analysis-title">
        <span>{emoji}</span>
        {section_title}
    </div>
    <div class="analysis-content">
        <p>{content_text}</p>
    </div>
</div>'''
    
    @staticmethod
    def _format_text_content(text: str) -> str:
        """格式化文本内容，添加HTML标记"""
        if not text:
            return ""
        
        # 处理粗体标记
        text = text.replace('**', '<strong>').replace('**', '</strong>')
        
        # 处理斜体标记
        text = text.replace('*', '<em>').replace('*', '</em>')
        
        # 处理代码标记
        text = text.replace('`', '<code>').replace('`', '</code>')
        
        # 处理数字和百分比的突出显示
        import re
        text = re.sub(r'(\d+\.?\d*%)', r'<strong>\1</strong>', text)
        text = re.sub(r'(\d+\.?\d*倍)', r'<strong>\1</strong>', text)
        
        return text 