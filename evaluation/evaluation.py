import json
import os
import re
from orchestrator import DebateOrchestrator
from .baselines import BaselineEvaluator
from client.api_basics import LLMClient
from config.config import RESULTS_DIR
from config.prompts import STRATEGY_QA_SAMPLE

class ExperimentRunner:
    def __init__(self):
        self.client = LLMClient()
        self.orchestrator = DebateOrchestrator(self.client)
        self.baseline = BaselineEvaluator(self.client)
        self.results = []

    def run_all_experiments(self, samples=5, include_jury=True):
        print(f"Running experiments on {samples} samples...")
        
        for i, entry in enumerate(STRATEGY_QA_SAMPLE[:samples]):
            question = entry["question"]
            ground_truth = entry["answer"]
            difficulty = entry.get("difficulty", "N/A")
            
            # 1. Direct QA Baseline
            direct_qa_res = self.baseline.direct_qa(question)
            direct_ans = self.orchestrator.debater_a.extract_answer(direct_qa_res['text'])
            
            # 2. Self-Consistency Baseline
            sc_res = self.baseline.self_consistency(question, n=3)
            sc_ans = sc_res['majority_vote']
            
            # 3. Debate Pipeline (including single judge and jury)
            debate_res = self.orchestrator.run_debate(question, ground_truth, include_jury=include_jury)
            
            # Single Judge Result
            judge_text = debate_res['judgment']['text']
            judge_ans = self.orchestrator.judge.extract_answer(judge_text)
            
            # Jury Panel Result (Bonus)
            jury_ans = None
            disagreement = 0
            if include_jury:
                jury_ans = debate_res['jury_result']['majority_vote']
                disagreement = debate_res['jury_result']['disagreement_score']
            
            # Evaluate Accuracy
            self.results.append({
                "id": i,
                "question": question,
                "ground_truth": ground_truth,
                "difficulty": difficulty,
                "direct_qa": {"answer": direct_ans, "correct": direct_ans == ground_truth},
                "self_consistency": {"answer": sc_ans, "correct": sc_ans == ground_truth},
                "single_judge": {"answer": judge_ans, "correct": judge_ans == ground_truth},
                "jury_panel": {"answer": jury_ans, "correct": jury_ans == ground_truth, "disagreement": disagreement}
            })
            
            # Save individual log
            self.orchestrator.save_log(debate_res, f"debate_{i}.json")

        self._summarize_and_save()

    def _summarize_and_save(self):
        total = len(self.results)
        summary = {
            "total": total,
            "direct_qa_accuracy": sum(1 for r in self.results if r["direct_qa"]["correct"]) / total,
            "self_consistency_accuracy": sum(1 for r in self.results if r["self_consistency"]["correct"]) / total,
            "single_judge_accuracy": sum(1 for r in self.results if r["single_judge"]["correct"]) / total,
            "jury_panel_accuracy": sum(1 for r in self.results if r["jury_panel"]["correct"]) / total,
            "analysis": {
                "jury_vs_single": {
                    "jury_improved": sum(1 for r in self.results if r["jury_panel"]["correct"] and not r["single_judge"]["correct"]),
                    "single_better": sum(1 for r in self.results if r["single_judge"]["correct"] and not r["jury_panel"]["correct"])
                },
                "disagreement_by_difficulty": {}
            }
        }
        
        # Calculate disagreement correlations
        for diff in ["Easy", "Medium", "Hard"]:
            relevant = [r for r in self.results if r["difficulty"] == diff]
            if relevant:
                avg_disagreement = sum(r["jury_panel"]["disagreement"] for r in relevant) / len(relevant)
                summary["analysis"]["disagreement_by_difficulty"][diff] = avg_disagreement

        summary_path = os.path.join(RESULTS_DIR, "summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"Summary saved to {summary_path}")
        return summary
