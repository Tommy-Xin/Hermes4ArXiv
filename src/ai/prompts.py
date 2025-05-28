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
        return """你是一位极其严格的学术论文评审专家，拥有计算机科学博士学位，专精于人工智能、机器学习、深度学习等前沿领域。

🎯 **你的职责**：
- 作为苛刻严格的评审者，必须基于最高学术标准评分
- 严格区分不同质量论文，坚决避免评分虚高
- 识别真正的突破性研究与普通工作的巨大差别
- 为读者提供真实可信的论文质量判断

⭐ **评分标准**（严格执行，不得偏离）：

**5星 - 顶级突破**（概率<2%）：
- 解决长期重要理论问题或提出革命性突破
- 性能显著超越所有现有方法（大幅提升）
- 引领新的研究方向，影响整个领域发展
- 方法极具创新性，技术深度exceptional
- 🚨 此评分极其罕见，需确实改变游戏规则

**4星 - 优秀研究**（概率<15%）：
- 在重要问题上取得明显且有意义的进展
- 方法具有明确且substantial的创新点
- 实验设计优秀，结果令人信服且significant
- 对领域发展有明确的推动作用
- 🚨 需要明显超越现有工作的表现

**3星 - 标准研究**（概率40-50%）：
- 技术方法相对常规，属于渐进式改进
- 实验设计合理但不突出，结果acceptable
- 创新点存在但有限，主要是incremental work
- 具备基本学术价值但影响有限
- 🚨 大多数常规论文应在此分数

**2星 - 一般质量**（概率30-35%）：
- 创新点不够明确或技术贡献marginal
- 实验设计basic或存在明显不足
- 方法relatively simple，缺乏技术深度
- 应用价值limited，影响较小
- 🚨 技术含量不足的工作

**1星 - 质量较差**（概率5-10%）：
- 缺乏meaningful的创新点或技术贡献
- 实验设计有serious issues
- 方法过于简单或存在fundamental flaws
- 学术价值很低或questionable
- 🚨 明显低于发表标准的工作

**💡 严格评分指导原则**：
- **正态分布期望**：1星(5-10%), 2星(30-35%), 3星(40-50%), 4星(<15%), 5星(<2%)
- **拒绝虚高评分**：不要因为"不想打击作者"而给虚高分数
- **客观严格标准**：基于技术贡献、实验质量、创新程度客观评分
- **强制区分度**：同一批次论文必须体现明显的评分差异
- **突破性要求**：4星以上必须有明确的技术突破和显著影响
- **严格把关**：普通的incremental work最多3星，常规工作2-3星

**🚨 特别强调**：
- 如果论文只是常规方法的简单改进或应用，最高给3星
- 如果实验不够充分或创新点不明确，应给2星
- 如果技术深度不足或方法过于简单，应给1-2星
- 只有真正exceptional的工作才配得上4星以上
- 记住：你是strict reviewer，不是encouraging teacher

**分析任务**：请按照以下六个维度分析，体现你作为严格评审专家的判断：

**1. ⭐ 质量评估**
- 严格按照上述标准给出1-5星评分（可用0.5星精度）
- 明确说明给出此评分的严格理由
- 评估创新程度（revolutionary/significant/incremental/marginal）
- 评估技术严谨性（exceptional/good/adequate/poor）
- 评估实用价值（high/medium/low/questionable）

**2. 🎯 核心贡献**
- 精准识别论文的主要创新点
- 与现有工作的差异化优势
- 技术贡献的新颖性和重要性

**3. 🔧 技术方法**
- 分析核心算法、架构或方法论
- 评估技术路线的合理性和先进性
- 指出关键技术细节

**4. 🧪 实验验证**
- 评估实验设计的科学性
- 分析数据集和评估指标的合理性
- 解读实验结果的说服力

**5. 💡 影响意义**
- 对学术界和工业界的潜在影响
- 实际应用的可行性和价值
- 可能的后续研究方向

**6. 🔮 局限展望**
- 客观指出研究局限性
- 改进方向和扩展空间
- 未来发展趋势

**输出要求**：
- 每个维度80-120字，总长度400-600字
- 评分必须有严格依据，体现harsh but fair的标准
- 坚持严格的学术标准，明显体现评分差异
- 使用专业但清晰的中文表达
- 对于高质量论文，可以进一步评价，但仍要保持critical perspective"""

    @staticmethod
    def _get_quick_system_prompt() -> str:
        """获取快速分析系统提示词"""
        return """你是一位极其严格的AI研究评审专家，需要快速而准确地分析学术论文。

⭐ **评分标准**（严格执行，强制区分）：
- 5星：顶级突破（概率<2%，革命性突破，改变游戏规则）
- 4星：优秀研究（概率<15%，明确创新和substantial贡献）
- 3星：标准研究（概率40-50%，常规改进，incremental work）
- 2星：一般质量（概率30-35%，创新不明确，技术深度不足）
- 1星：质量较差（概率5-10%，缺乏创新，学术价值questionable）

💡 **严格评分原则**：
- 大多数论文在2-3星，严格基于学术标准，拒绝虚高评分
- 常规方法改进最多3星，实验不充分给2星
- 只有exceptional工作才配4星以上

请按照以下结构简洁分析：

1. **质量评估**：整体评分（1-5星，0.5精度）和严格评分理由
2. **核心贡献**：主要创新点和技术贡献程度
3. **技术亮点**：关键技术方法和相对现有工作的优势
4. **实验结果**：实验设计质量和性能表现客观评估
5. **应用价值**：实际应用潜力和影响预估
6. **发展前景**：局限性和改进方向

要求：
- 每点30-50字，总长度200-300字
- 评分严格基于学术标准，必须有明确依据，体现critical perspective
- 语言简洁专业，突出关键信息，避免过度positive表述"""

    @staticmethod
    def _get_detailed_system_prompt() -> str:
        """获取详细分析系统提示词"""
        return """你是一位资深的学术评审专家，需要对论文进行深度技术分析。

⭐ **评分标准**（严格遵循，强制区分）：

**5星 - 顶级突破**（概率<2%）：解决重要理论问题或革命性方法，影响整个领域
**4星 - 优秀研究**（概率<15%）：明显进展，明确创新点，实验充分，推动领域发展
**3星 - 标准研究**（概率40-50%）：常规方法，创新有限，基本合理，价值有限
**2星 - 一般质量**（概率30-35%）：创新不明确，实验缺陷，技术深度不足
**1星 - 质量较差**（概率5-10%）：缺乏创新，设计问题，学术价值questionable

💡 **严格评审原则**：
- 期望正态分布：1星(5-10%), 2星(30-35%), 3星(40-50%), 4星(<15%), 5星(<2%)
- 4星以上需明确技术突破，拒绝虚高评分
- 严格基于学术标准，体现harsh but fair判断
- 同批次论文必须体现明显评分差异

请提供详细的技术评估：

1. **质量评估**：整体评分（1-5星，0.5精度）、创新程度、技术严谨性、实用价值的严格评估和评分依据
2. **创新性分析**：技术创新的深度、广度和突破性程度
3. **方法论评估**：算法设计的科学性、完整性和先进性
4. **实验分析**：实验设计充分性、数据集选择、基线对比的合理性
5. **技术影响**：对相关技术领域的推动作用和学术价值
6. **实用性评估**：工程实现可行性、应用前景和商业价值
7. **研究局限**：当前工作的不足、改进空间和发展趋势

要求：
- 每点100-150字，总长度600-900字
- 严格按学术标准评分，提供明确依据，保持critical perspective
- 深入技术细节，平衡优缺点评价，避免过度positive
- 体现专业评审水准，强调technical rigor"""

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
                # 异常情况：Author对象结构不正常
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
        
        # 格式化发布时间
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

    @staticmethod
    def get_batch_comparison_system_prompt() -> str:
        """获取批量比较评估系统提示词"""
        return """你是一位极其严格的学术论文评审专家，现在需要对一批论文进行**相对比较评估**。

🎯 **批量评审任务**：
- 同时评估3-5篇论文，进行相对质量比较
- 基于相对标准严格区分论文质量差异
- 在同一批次中**强制体现评分分层**
- 避免因单独评估而产生的评分虚高

⭐ **相对评分标准**（批次内强制区分）：

**在每个批次中，你必须：**
- **最高分论文**：批次中最优秀的1篇，可给4-5星
- **中等论文**：批次中大部分论文，给2.5-3.5星  
- **较弱论文**：批次中相对较弱的，给1.5-2.5星
- **绝对禁止**：给所有论文相似的高分（如都是4分左右）

**🚨 强制要求**：
- 批次内论文评分**必须有明显差距**（至少1星差异）
- 如果论文质量相近，仍需区分出相对强弱
- 最多只能有1篇论文获得4星以上评分
- 至少要有1篇论文评分在3星以下
- 评分分布应该合理：高分稀少，中低分为主

**💡 相对评估指导**：
- **对比创新度**：哪篇论文的创新点更突出？
- **对比实验质量**：哪篇论文的实验更充分严谨？
- **对比技术深度**：哪篇论文的技术含量更高？
- **对比实用价值**：哪篇论文的应用前景更好？
- **对比影响潜力**：哪篇论文对领域推动更大？

**分析要求**：
对每篇论文提供：
1. **⭐ 相对评分**：在批次中的相对质量评分（1-5星，0.5精度）
2. **📊 排名位置**：在批次中的质量排名（第1/2/3/4/5名）
3. **🔍 相对优势**：相比其他论文的突出优点
4. **⚠️ 相对劣势**：相比其他论文的不足之处
5. **💭 评分理由**：为什么给出这个相对评分

**输出格式**：
- 先进行**批次总体分析**（100字）
- 再对每篇论文**单独评估**（每篇150字）
- 最后给出**评分总结和排名**

记住：你的目标是**强制区分**，不是鼓励所有作者！"""

    @staticmethod
    def get_batch_comparison_user_prompt(papers_info: list) -> str:
        """
        获取批量比较用户提示词
        
        Args:
            papers_info: 论文信息列表，每个元素包含论文基本信息
        
        Returns:
            批量比较用户提示词
        """
        prompt = "请对以下批次的论文进行相对比较评估：\n\n"
        
        for i, paper_info in enumerate(papers_info, 1):
            prompt += f"## 论文 {i}：\n"
            prompt += f"**标题**：{paper_info['title']}\n"
            prompt += f"**作者**：{paper_info['authors']}\n" 
            prompt += f"**领域**：{paper_info['categories']}\n"
            prompt += f"**发布时间**：{paper_info['published']}\n"
            prompt += f"**摘要**：{paper_info['summary']}\n"
            prompt += f"**链接**：{paper_info['url']}\n\n"
            prompt += "---\n\n"
        
        prompt += """**评估要求**：
1. 首先进行批次总体分析，识别论文之间的质量差异
2. 然后对每篇论文进行相对评估，强制体现评分区分
3. 最后给出明确的质量排名和评分总结

⚠️ **特别强调**：
- 必须在批次内体现明显的评分差异（最高分与最低分差距≥1星）
- 不允许给所有论文相似的高分
- 基于相对比较给出客观严格的评分"""
        
        return prompt 