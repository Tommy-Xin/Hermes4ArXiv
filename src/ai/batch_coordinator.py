#!/usr/bin/env python3
"""
批量分析协调器
管理论文批次处理和两阶段分析流程。
"""

import logging
import re
from collections import defaultdict
from typing import Dict, Any, List

from src.ai.analyzer import DeepSeekAnalyzer
from src.config import Config
from src.db.db_manager import DBManager
from src.ai.prompts import PromptManager

logger = logging.getLogger(__name__)


class BatchCoordinator:
    """批量分析协调器，负责编排整个分析流程。"""

    def __init__(self, config: Config, db_manager: DBManager, analyzer: DeepSeekAnalyzer):
        self.config = config
        self.db_manager = db_manager
        self.analyzer = analyzer

    def run_batch_analysis(self, papers_to_process: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        运行批量分析。如果启用了两阶段分析，则执行新流程，否则执行旧的直接分析流程。
        """
        use_stage_analysis = self.config.get('STAGE_ANALYSIS.ENABLED', False)

        if not use_stage_analysis:
            logger.info("Two-stage analysis is disabled. Running legacy direct batch analysis.")
            return self._run_legacy_batch_analysis(papers_to_process)

        logger.info("Starting two-stage analysis pipeline.")

        # Stage 1: Sliding Window Ranking
        papers_with_scores = self._run_stage1_ranking(papers_to_process)
        if not papers_with_scores:
            logger.warning("Stage 1 ranking resulted in no papers. Aborting.")
            return []

        # Stage 2: Filtering and Deep Analysis
        final_results = self._run_stage2_deep_analysis(papers_with_scores)
        
        logger.info("Two-stage analysis pipeline finished.")
        return final_results

    def _run_stage1_ranking(self, all_papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行第一阶段：滑动窗口排名。返回带有聚合分数的论文列表。
        """
        window_size = self.config.get('STAGE_ANALYSIS.STAGE1.WINDOW_SIZE', 10)
        step_size = self.config.get('STAGE_ANALYSIS.STAGE1.STEP_SIZE', 5)
        
        if step_size <= 0:
            logger.error("Sliding window step_size must be positive. Defaulting to 1.")
            step_size = 1

        logger.info(f"Stage 1: Creating sliding window batches (size: {window_size}, step: {step_size}).")
        
        paper_chunks = []
        for i in range(0, len(all_papers), step_size):
            chunk = all_papers[i : i + window_size]
            if chunk:
                # Ensure we don't add chunks that are too small if the last window is tiny
                # This could happen if len(all_papers) is just over a step boundary
                if len(paper_chunks) > 0 and len(chunk) < window_size / 2:
                    # Append to the previous chunk to avoid a very small last batch
                    paper_chunks[-1].extend(chunk)
                    break
                paper_chunks.append(chunk)

        stage1_scores = defaultdict(list)
        for i, chunk in enumerate(paper_chunks):
            logger.info(f"Processing chunk {i+1}/{len(paper_chunks)}...")
            try:
                ranking_results = self.analyzer.rank_papers_in_batch(chunk)
                for result in ranking_results:
                    paper_id = result.get('paper_id')
                    score = result.get('score')
                    if paper_id and isinstance(score, (int, float)):
                        stage1_scores[paper_id].append(float(score))
            except Exception as e:
                logger.error(f"Error ranking chunk {i+1}: {e}", exc_info=True)

        final_scores = {paper_id: max(scores) for paper_id, scores in stage1_scores.items() if scores}
        
        papers_with_scores = []
        for paper in all_papers:
            paper_id = paper.get('paper_id')
            score = final_scores.get(paper_id)
            paper['stage1_score'] = score if score is not None else 0.0
            papers_with_scores.append(paper)

        papers_with_scores.sort(key=lambda p: p.get('stage1_score', 0.0), reverse=True)
        
        logger.info(f"Stage 1: Completed ranking for {len(final_scores)} papers.")
        return papers_with_scores

    def _run_stage2_deep_analysis(self, papers_with_scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行第二阶段：筛选并对顶尖论文进行深度分析。
        """
        promotion_threshold = self.config.get('STAGE_ANALYSIS.STAGE1.PROMOTION_SCORE_THRESHOLD', 3.5)
        max_to_analyze = self.config.get('STAGE_ANALYSIS.STAGE2.MAX_PAPERS_TO_ANALYZE', 20)

        promoted_papers = [p for p in papers_with_scores if p.get('stage1_score', 0.0) >= promotion_threshold]
        top_papers_to_analyze = promoted_papers[:max_to_analyze]

        logger.info(f"Stage 2: {len(top_papers_to_analyze)} papers promoted for deep analysis (threshold: >={promotion_threshold}, max: {max_to_analyze}).")

        filtered_out_papers = [p for p in papers_with_scores if p not in top_papers_to_analyze]
        for paper in filtered_out_papers:
            self.db_manager.update_paper_analysis(
                paper_id=paper['paper_id'],
                analysis_text=f"Filtered out at Stage 1 with score: {paper.get('stage1_score', 0.0):.2f}",
                quality_score=paper.get('stage1_score', 0.0),
                html_analysis="<p>This paper was not selected for detailed analysis based on its initial ranking score.</p>",
                status='filtered'
            )
        if filtered_out_papers:
            logger.info(f"Updated status for {len(filtered_out_papers)} filtered papers.")

        if not top_papers_to_analyze:
            return []

        try:
            batch_analysis_text = self.analyzer.analyze_papers_batch(top_papers_to_analyze)
            parsed_results = self._parse_batch_analysis(batch_analysis_text, top_papers_to_analyze)
            
            analyzed_papers_with_details = []
            for paper in top_papers_to_analyze:
                paper_id = paper['paper_id']
                if paper_id in parsed_results:
                    analysis_content = parsed_results[paper_id]
                    self.db_manager.update_paper_analysis(
                        paper_id=paper_id,
                        analysis_text=analysis_content['raw'],
                        quality_score=paper.get('stage1_score', 0.0),
                        html_analysis=analysis_content['html'],
                        status='analyzed'
                    )
                    paper['analysis'] = analysis_content['raw']
                    paper['html_analysis'] = analysis_content['html']
                    analyzed_papers_with_details.append(paper)
            return analyzed_papers_with_details
        except Exception as e:
            logger.error(f"An error occurred during Stage 2 deep analysis: {e}", exc_info=True)
            return []

    def _run_legacy_batch_analysis(self, papers_to_process: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        原始的、直接的批量分析方法。
        """
        batch_size = self.config.get("BATCH_SIZE", 5)
        paper_chunks = [papers_to_process[i:i + batch_size] for i in range(0, len(papers_to_process), batch_size)]
        
        all_analyzed_papers = []
        for chunk in paper_chunks:
            try:
                logger.info(f"Analyzing a legacy batch of {len(chunk)} papers.")
                analysis_text = self.analyzer.analyze_papers_batch(chunk)
                parsed_results = self._parse_batch_analysis(analysis_text, chunk)
                
                for paper_id, content in parsed_results.items():
                    paper = next((p for p in chunk if p['paper_id'] == paper_id), None)
                    if paper:
                        self.db_manager.update_paper_analysis(
                            paper_id=paper_id, analysis_text=content['raw'],
                            quality_score=None, html_analysis=content['html'], status='analyzed'
                        )
                        paper.update(content)
                        all_analyzed_papers.append(paper)
            except Exception as e:
                logger.error(f"Error processing legacy batch: {e}", exc_info=True)
        return all_analyzed_papers

    def _parse_batch_analysis(self, batch_text: str, papers_in_batch: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
        """
        解析批量分析文本，返回一个包含每个论文分析结果的字典。
        """
        paper_ids = [p['paper_id'] for p in papers_in_batch]
        results = {}
        
        if not batch_text or not paper_ids:
            return results

        split_pattern = r'Paper ID\s*:\s*(' + '|'.join(re.escape(pid) for pid in paper_ids) + ')'
        parts = re.split(split_pattern, batch_text)
        
        if len(parts) < 3:
            logger.warning(f"Could not split batch analysis text. Text: '{batch_text[:200]}...'")
            return {}

        for i in range(1, len(parts), 2):
            paper_id = parts[i]
            content_with_header = parts[i+1]
            # The actual analysis content starts after the header part (Title, Abstract, etc.)
            # A simple way is to find the end of the abstract marker '---'
            content_parts = re.split(r'---\s*\n', content_with_header, maxsplit=1)
            raw_content = content_parts[-1].strip()
            
            html_analysis = PromptManager.format_analysis_for_html(raw_content)
            results[paper_id] = {'raw': raw_content, 'html': html_analysis}
            logger.info(f"Successfully parsed analysis for paper {paper_id}.")

        return results 