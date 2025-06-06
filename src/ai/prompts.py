#!/usr/bin/env python3
"""
AI提示词管理模块
集中管理各种AI分析任务的提示词
"""

import logging
import re
import json
from typing import Dict, List, Any

import arxiv
re

class PromptManager:
    """提示词管理器，所有方法均为静态方法"""

    @staticmethod
    def get_system_prompt() -> str:
        """
        获取系统提示词 (始终返回综合分析版本)
        """
        return PromptManager._get_comprehensive_system_prompt()

    @staticmethod
    def _get_comprehensive_system_prompt() -> str:
        """获取综合分析系统提示词"""
        return """你是一位极其严格的学术论文评审专家，拥有计算机科学博士学位，专精于人工智能、机器学习、深度学习等前沿领域。

🎯 **你的职责**：
- 作为苛刻严格的评审者，必须基于最高学术标准评分
- 严格区分不同质量论文，坚决避免评分虚高
- 识别真正的突破性研究与普通工作的巨大差别
- 为读者提供真实可信的论文质量判断

⭐ **严格评分标准**（强制执行，绝不偏离）：

**5星 - 革命性突破**（概率<1%，极其罕见）：
- 🚀 **理论突破**：解决领域内长期悬而未决的重大理论问题
- 🎯 **方法创新**：提出全新的技术范式，改变解决问题的思路
- 📈 **性能飞跃**：在重要任务上实现质的提升（不是微小改进）
- 🌟 **影响力**：预期引领新的研究方向，影响整个学科发展
- ✅ **技术深度**：方法具有极高的技术复杂度和创新性
- 🔬 **实验严谨**：大规模、多样化的实验验证，结果令人信服
- **📝 评分条件**：必须同时满足以上所有条件才可给5星

**4星 - 重要进展**（概率<5%，高标准）：
- 🎯 **明确贡献**：在重要问题上取得显著且有意义的进展
- 🔧 **方法创新**：提出新颖的技术方法，具有明确的创新点
- 📊 **性能提升**：在标准基准上有substantial且consistent的改进
- 🧪 **实验充分**：实验设计优秀，基线对比全面，结果可信
- 💡 **学术价值**：对领域发展有明确推动作用，值得广泛关注
- **📝 评分条件**：需明显超越现有工作，有clear的技术优势

**3星 - 合格研究**（概率35-45%，标准水平）：
- 🔄 **渐进改进**：在现有方法基础上进行合理的改进或扩展
- 📋 **实验合理**：实验设计基本合理，验证了方法的有效性
- 💻 **技术可行**：方法技术上可行，实现相对直接
- 📈 **有限提升**：性能有一定提升但不显著，改进幅度有限
- 🎓 **学术价值**：具备基本学术价值，但影响力和创新度有限
- **📝 评分条件**：大多数常规研究应该在此分数段

**2星 - 一般质量**（概率35-45%，低于平均）：
- ❓ **创新不足**：创新点不够明确或技术贡献边际化
- ⚠️ **实验问题**：实验设计不够充分，基线对比不全面
- 🔧 **方法简单**：技术方法相对简单，缺乏足够的技术深度
- 📉 **提升有限**：性能改进微小或在某些情况下不一致
- 💼 **应用局限**：应用价值有限，实用性存疑
- **📝 评分条件**：技术贡献不足或实验验证不充分

**1星 - 质量较差**（概率10-15%，明显问题）：
- ❌ **缺乏创新**：缺乏有意义的创新点或技术贡献
- 🚫 **实验缺陷**：实验设计存在严重问题或验证不充分
- 🔴 **方法问题**：方法过于简单或存在根本性缺陷
- 📊 **结果可疑**：实验结果不可信或存在明显问题
- ⭐ **价值存疑**：学术价值很低或应用前景不明
- **📝 评分条件**：明显低于发表标准或存在serious issues

**🎯 严格评分执行准则**：
1. **强制分布要求**：
   - 5星：<1%（只有真正革命性的工作）
   - 4星：<5%（需要明确的重要贡献）
   - 3星：35-45%（大多数合格研究）
   - 2星：35-45%（一般质量工作）
   - 1星：10-15%（存在明显问题）
2. **评分铁律**：
   - **拒绝温和主义**：不要因为"不想打击作者"而给虚高分数
   - **坚持客观标准**：基于技术贡献、实验质量、创新程度严格评分
   - **强制区分度**：必须在不同质量论文间体现明显差异
   - **突破性要求**：4星以上必须有明确且substantial的技术突破
   - **常规工作限制**：普通incremental work最高3星，常规改进2-3星
3. **评分参考对照**：
   - **5星参考**：GPT、Transformer、ResNet等历史性突破论文
   - **4星参考**：BERT、Vision Transformer等重要进展论文
   - **3星参考**：现有方法的合理改进和扩展
   - **2星参考**：创新有限的常规工作
   - **1星参考**：实验不充分或方法有明显缺陷的工作
4. **严格把关要点**：
   - 简单的超参数调优或架构微调 → 最多2星
   - 缺乏充分基线对比的实验 → 降1星
   - 仅在小数据集验证的方法 → 降1星  
   - 创新点不明确的工作 → 最多2星
   - 性能提升微小(<2%)的改进 → 最多3星

**🚨 特别强调**：
你是STRICT REVIEWER，不是encouraging teacher。记住：
- 68%的论文应该在2-3星（符合正态分布）
- 只有exceptional的工作才配得上4星以上
- 普通的incremental work就是普通，不要美化
- 实验不充分就是不充分，不要宽容
- 创新不足就是不足，不要迁就

**分析任务**：请按照以下六个维度进行严格分析：
**1. ⭐ 质量评估**
- 严格按照上述标准给出1-5星评分（可用0.5星精度）
- 明确说明给出此评分的严格理由和对照标准
- 评估创新程度（revolutionary/significant/incremental/marginal/none）
- 评估技术严谨性（exceptional/good/adequate/poor/problematic）
- 评估实用价值（high/medium/low/questionable/none）
**2. 🎯 核心贡献**
- 精准识别论文的主要创新点和技术贡献
- 与现有工作的差异化分析和优势评估
- 技术贡献的新颖性、重要性和深度评价
**3. 🔧 技术方法**
- 分析核心算法、架构或方法论的先进性
- 评估技术路线的合理性、创新性和实现难度
- 指出关键技术细节和与现有方法的区别
**4. 🧪 实验验证**
- 评估实验设计的科学性和充分性
- 分析数据集选择、基线对比、评估指标的合理性
- 解读实验结果的说服力和可信度
**5. 💡 影响意义**
- 客观评估对学术界和工业界的潜在影响
- 分析实际应用的可行性和价值
- 预测可能的后续研究方向和影响范围
**6. 🔮 局限展望**
- 客观指出研究的主要局限性和不足
- 提出具体的改进方向和扩展建议
- 分析未来发展趋势和挑战

**输出要求**：
- 每个维度100-120字，总长度500-700字
- 评分必须有严格依据，体现harsh but fair的专业标准
- 语言专业严谨，避免过度positive的表述
- 突出关键信息，提供客观平衡的评价
- 体现顶级会议reviewer的严格水准

🚨 **强制输出格式要求**：
1. **必须按照6个维度逐一分析**，不得遗漏任何维度
2. **必须在第1个维度明确给出1-5星评分**（可用0.5精度，如3.5星）
3. **每个维度必须以指定emoji开头**（⭐🎯🔧🧪💡🔮）
4. **评分必须基于严格学术标准**，并说明对照的参考基准
5. **如无法确定某个维度内容**，也必须给出"信息不足"的专业判断
6. **输出结构不得改变**，必须严格按照6个维度的顺序输出
7. **内部文本格式**：每个维度的分析内容应为纯文本段落。可以使用 `**加粗**` 或 `*斜体*` 进行简单强调，但**严禁在各维度内部使用任何Markdown标题 (如 `#`, `##`, `###`)、列表标记 (`-`, `*`, `1.`) 或其他复杂Markdown结构。**"""

    @staticmethod
    def get_user_prompt(paper: arxiv.Result) -> str:
        """获取单个论文分析的用户提示词"""
        authors_str = '未知'
        if hasattr(paper, 'authors') and paper.authors:
            try:
                author_names = [author.name for author in paper.authors]
                authors_str = ', '.join(author_names[:5])
                if len(author_names) > 5:
                    authors_str += f" 等{len(author_names)}人"
            except AttributeError as e:
                logger = logging.getLogger(__name__)
                logger.warning(f"Abnormal author object structure: {e}")
                authors_str = "作者信息异常"
        
        published_date = '未知'
        if hasattr(paper, 'published') and paper.published:
            published_date = paper.published.strftime('%Y年%m月%d日')

        summary = paper.summary.strip().replace("\n", " ")
        if len(summary) > 1500:
            summary = summary[:1500] + "..."

        return f"""请分析以下ArXiv论文：
📄 **论文标题**：{paper.title}
👥 **作者信息**：{authors_str}
🏷️ **研究领域**：{', '.join(paper.categories)}
📅 **发布时间**：{published_date}
📝 **论文摘要**：{summary}
🔗 **论文链接**：{paper.entry_id}
---
请基于以上信息，按照系统提示的结构进行深度分析。"""

    @staticmethod
    def format_batch_analysis_prompt(papers: list[Dict[str, Any]]) -> str:
        """格式化深度批量分析的用户提示词"""
        paper_texts = []
        for paper in papers:
            paper_texts.append(
f"""---
**Paper ID**: {paper['paper_id']}
**Title**: {paper['title']}
**Abstract**:
{paper.get('abstract', 'N/A').replace('{', '{{').replace('}', '}}')}
---"""
            )
        return "Please provide a comprehensive 5-point analysis for each of the following papers, formatted clearly with separators.\n" + "\n".join(paper_texts)

    @staticmethod
    def get_stage1_ranking_system_prompt() -> str:
        """获取第一阶段强制排名系统提示词"""
        return """You are an expert AI research assistant. Your task is to perform a relative quality ranking on a small batch of academic papers.
You will be given a list of papers, each with a title and an abstract.
You MUST follow these rules strictly:
1.  **Relative Ranking**: Do not judge each paper in isolation. You MUST compare them against each other to determine their relative novelty, significance, and potential impact.
2.  **Forced Distribution Scoring**: You MUST assign a score to each paper based on its rank within the current batch. The scores must follow this forced distribution:
    -   **Top 10% (e.g., 1 paper in a batch of 10)**: Assign a score between 4.5 and 5.0. These are groundbreaking papers.
    -   **Next 20% (e.g., 2 papers in a batch of 10)**: Assign a score between 3.5 and 4.4. These are significant and interesting papers.
    -   **Middle 40% (e.g., 4 papers in a batch of 10)**: Assign a score between 2.5 and 3.4. These are solid, incremental contributions.
    -   **Bottom 30% (e.g., 3 papers in a batch of 10)**: Assign a score between 1.0 and 2.4. These are minor, less impactful, or flawed papers.
3.  **JSON Output**: You MUST return your analysis as a single JSON object. This object should be a list where each element corresponds to one paper and contains the paper's ID, its assigned score, and a brief justification for the score. Do not include any text outside of the JSON object.

Example for a batch of 10 papers:
[
  {"paper_id": "2401.0001", "score": 4.8, "justification": "Breakthrough approach to a long-standing problem."},
  {"paper_id": "2401.0005", "score": 4.1, "justification": "Significant improvement over SOTA with strong results."},
  {"paper_id": "2401.0008", "score": 3.9, "justification": "Interesting new application of an existing method."},
  {"paper_id": "2401.0002", "score": 3.2, "justification": "Solid incremental work with decent experiments."},
  {"paper_id": "2401.0004", "score": 3.1, "justification": "An okay contribution, but lacks novelty."},
  {"paper_id": "2401.0007", "score": 2.8, "justification": "Incremental work, limited validation."},
  {"paper_id": "2401.0009", "score": 2.5, "justification": "Standard methodology, predictable results."},
  {"paper_id": "2401.0003", "score": 2.1, "justification": "Minor contribution with several limitations."},
  {"paper_id": "2401.0006", "score": 1.8, "justification": "Flawed methodology, results are not convincing."},
  {"paper_id": "2401.0010", "score": 1.5, "justification": "Very limited novelty and weak supporting evidence."}
]
"""

    @staticmethod
    def format_stage1_ranking_prompt(papers: list[Dict[str, Any]]) -> str:
        """格式化第一阶段排名的用户提示词"""
        paper_texts = []
        for paper in papers:
            # 使用 json.dumps 来安全地处理摘要和标题中的特殊字符（如引号）
            abstract = json.dumps(paper.get('abstract', '').replace("\n", " "))
            title = json.dumps(paper.get('title', ''))
            paper_texts.append(
f"""    {{
        "paper_id": "{paper.get('paper_id', 'N/A')}",
        "title": {title},
        "abstract": {abstract}
    }}"""
            )
        return f"Please rank the following papers based on the rules provided in the system prompt. Here is the list of papers:\n[\n{',\\n'.join(paper_texts)}\n]"

    @staticmethod
    def format_analysis_for_html(analysis_text: str) -> str:
        """将AI分析结果格式化为HTML"""
        if not isinstance(analysis_text, str) or not analysis_text.strip():
            return "<p>AI analysis not available.</p>"

        sections = {
            "⭐ 质量评估": "star",
            "🎯 核心贡献": "bullseye",
            "🔧 技术方法": "wrench",
            "🧪 实验验证": "beaker",
            "💡 影响意义": "lightbulb",
            "🔮 局限展望": "crystal-ball"
        }
        
        html_content = ""
        
        # 使用正则表达式按维度分割，同时保留分隔符
        parts = re.split(r'(⭐|🎯|🔧|🧪|💡|🔮)', analysis_text)
        
        # parts[0]是第一个分隔符之前的内容（通常为空），之后是 (分隔符, 内容) 对
        content_parts = [parts[i] + parts[i+1] for i in range(1, len(parts), 2)]

        for part in content_parts:
            for title, icon in sections.items():
                if part.strip().startswith(title):
                    # 移除标题本身和前后的空格
                    content = part.replace(title, "", 1).strip()
                    # 格式化内容
                    formatted_content = PromptManager._format_text_content(content)
                    html_content += f"""
                    <div class="analysis-dimension">
                        <div class="dimension-title">
                            <i class="fas fa-{icon}"></i>
                            <h4>{title.split(' ')[1]}</h4>
                        </div>
                        <p>{formatted_content}</p>
                    </div>
                    """
                    break # 匹配到就处理下一个part
        
        if not html_content:
            # 如果分割失败，提供原始文本作为后备
            return f"<p>{analysis_text.replace('<', '&lt;').replace('>', '&gt;')}</p>"

        return f'<div class="ai-analysis-container">{html_content}</div>'

    @staticmethod
    def _format_text_content(text: str) -> str:
        """格式化文本内容，处理加粗和换行"""
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        # 转换 **加粗** 为 <strong>
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        # 转换 *斜体* 为 <em>
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        # 转换换行符
        text = text.replace('\n', '<br>')
        return text 