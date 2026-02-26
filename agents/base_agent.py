import re

class BaseAgent:
    def __init__(self, client):
        self.client = client

    def get_response(self, prompt, **kwargs):
        result = self.client.query_llm(prompt, **kwargs)
        if "error" in result:
            raise Exception(f"API Error: {result['error']}")
        return result

    def extract_answer(self, text):
        # Prioritize the specific format "Answer is yes" or "Answer is no"
        match = re.search(r"Answer is\s*(yes|no)", text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
            
        # Fallback for "Answer: yes/no"
        match = re.search(r"Answer:\s*(Yes|No)", text, re.IGNORECASE)
        if match:
            return match.group(1).capitalize()
            
        # Fallback for any standalone "Yes" or "No" in the last 100 characters
        tail = text[-100:]
        matches = re.findall(r"\b(Yes|No)\b", tail, re.IGNORECASE)
        if matches:
            return matches[-1].capitalize()
            
        return None
