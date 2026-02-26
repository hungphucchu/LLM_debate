import json
import os
from agents import DebaterAgent, JudgeAgent
from config.prompts import DEBATER_A_INIT, DEBATER_B_INIT, DEBATER_A_ROUND, DEBATER_B_ROUND
from config.config import DEBATE_ROUNDS, LOG_DIR
from agents.jury import JuryPanel

class DebateOrchestrator:
    def __init__(self, client):
        self.debater_a = DebaterAgent(client, role="Debater A (Proponent)")
        self.debater_b = DebaterAgent(client, role="Debater B (Opponent)")
        self.judge = JudgeAgent(client)
        self.jury = JuryPanel(client)
        self.transcript = []

    def run_debate(self, question, ground_truth="Unknown", include_jury=False):
        print(f"Starting debate on question: {question}")
        self.transcript = []
        
        init_a = self.debater_a.generate_initial_position(question, DEBATER_A_INIT)
        init_b = self.debater_b.generate_initial_position(question, DEBATER_B_INIT)
        
        self.transcript.append({"round": 0, "agent": "Debater A", "response": init_a})
        self.transcript.append({"round": 0, "agent": "Debater B", "response": init_b})

        ans_a = self.debater_a.extract_answer(init_a['text'])
        ans_b = self.debater_b.extract_answer(init_b['text'])

        # Check if both debaters arrived at the same "Yes" or "No" conclusion
        if ans_a in ["Yes", "No"] and ans_b in ["Yes", "No"] and ans_a == ans_b:
            print(f"Phase 1 Consensus reached: Both answered {ans_a}. Skipping to Phase 3.")
            return self._finalize_debate(question, ground_truth, consensus=ans_a, include_jury=include_jury)

        # Multi-Round Debate
        consecutive_agreement_rounds = 0
        for r in range(1, DEBATE_ROUNDS + 1):
            print(f"Round {r}...")
            full_transcript_str = self._format_transcript()
            
            arg_a = self.debater_a.generate_round_argument(question, full_transcript_str, DEBATER_A_ROUND)
            self.transcript.append({"round": r, "agent": "Debater A", "response": arg_a})
            
            full_transcript_str = self._format_transcript()
            arg_b = self.debater_b.generate_round_argument(question, full_transcript_str, DEBATER_B_ROUND)
            self.transcript.append({"round": r, "agent": "Debater B", "response": arg_b})

            ans_a = self.debater_a.extract_answer(arg_a['text'])
            ans_b = self.debater_b.extract_answer(arg_b['text'])

            if ans_a in ["Yes", "No"] and ans_b in ["Yes", "No"] and ans_a == ans_b:
                consecutive_agreement_rounds += 1
                if consecutive_agreement_rounds >= 2:
                    print(f"Phase 2 Consensus reached: Both answered {ans_a} for 2 rounds. Ending early.")
                    break
            else:
                consecutive_agreement_rounds = 0

        return self._finalize_debate(question, ground_truth, include_jury=include_jury)

    def _finalize_debate(self, question, ground_truth, consensus=None, include_jury=False):
        # Judgment
        print("Rendering judgment...")
        full_transcript_str = self._format_transcript()
        judgment = self.judge.evaluate_debate(question, full_transcript_str, ground_truth)
        
        result = {
            "question": question,
            "ground_truth": ground_truth,
            "consensus": consensus,
            "transcript": self.transcript,
            "judgment": judgment
        }

        # Jury Panel
        if include_jury:
            jury_result = self.jury.deliberate(question, full_transcript_str)
            result["jury_result"] = jury_result

        return result

    def _format_transcript(self):
        return "\n\n".join([f"{item['agent']} (Round {item['round']}):\n{item['response']['text']}" for item in self.transcript])

    def save_log(self, result, filename):
        log_path = os.path.join(LOG_DIR, filename)
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Log saved to {log_path}")
