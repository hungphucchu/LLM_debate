from .base_agent import BaseAgent

class DebaterAgent(BaseAgent):
    def __init__(self, client, role="Debater"):
        super().__init__(client)
        self.role = role

    def generate_initial_position(self, question, template):
        prompt = template.format(question=question)
        return self.get_response(prompt)

    def generate_round_argument(self, question, transcript, template):
        prompt = template.format(question=question, transcript=transcript)
        return self.get_response(prompt)
