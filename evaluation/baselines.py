import random
from agents import BaseAgent
from config.prompts import DIRECT_QA_PROMPT, SELF_CONSISTENCY_PROMPT

class BaselineEvaluator(BaseAgent):
    def __init__(self, client):
        super().__init__(client)

    def direct_qa(self, question):
        prompt = DIRECT_QA_PROMPT.format(question=question)
        return self.get_response(prompt)

    def self_consistency(self, question, n=3):
        prompt = SELF_CONSISTENCY_PROMPT.format(question=question)
        responses = []
        for _ in range(n):
            res = self.get_response(prompt, temperature=0.7)
            responses.append(res['text'])
        
        # Simple majority vote logic (extracting Yes/No)
        votes = {"Yes": 0, "No": 0}
        for res in responses:
            if "Yes" in res:
                votes["Yes"] += 1
            elif "No" in res:
                votes["No"] += 1
        
        majority_vote = "Yes" if votes["Yes"] >= votes["No"] else "No"
        return {
            "votes": votes,
            "majority_vote": majority_vote,
            "responses": responses
        }
