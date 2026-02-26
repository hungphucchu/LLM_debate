from .base_agent import BaseAgent
from config.prompts import JUDGE_PROMPT

class JudgeAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client)

    def evaluate_debate(self, question, transcript, ground_truth):
        prompt = JUDGE_PROMPT.format(question=question, transcript=transcript, ground_truth=ground_truth)
        return self.get_response(prompt)
