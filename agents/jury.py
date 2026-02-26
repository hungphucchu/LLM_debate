from agents.judge_agent import JudgeAgent
from config.prompts import JURY_INITIAL_PROMPT, JURY_DELIBERATION_PROMPT
from config.config import TEMPERATURE

class JuryPanel:
    """
    Bonus: Multi-Agent Judge Panel (Jury)
    Implements a jury of 3 LLM judges that deliberate by seeing each other's initial verdicts.
    """
    def __init__(self, client, size=3):
        self.client = client
        self.size = size
        # We use a helper agent instance to call extract_answer
        self.helper_agent = JudgeAgent(client)

    def deliberate(self, question, transcript):
        print(f"Jury Panel of {self.size} is deliberating...")
        
        # Step 1: Initial individual verdicts
        initial_verdicts = []
        for i in range(self.size):
            prompt = JURY_INITIAL_PROMPT.format(
                juror_id=i+1,
                question=question,
                transcript=transcript
            )
            res = self.client.query_llm(prompt, temperature=TEMPERATURE)
            initial_verdicts.append(res['text'])
        
        # Step 2: Deliberation (each juror sees others' verdicts)
        final_verdicts = []
        for i in range(self.size):
            # Each juror sees the initial verdicts of the others
            others = [(j + 1, initial_verdicts[j]) for j in range(self.size) if j != i]
            prompt = JURY_DELIBERATION_PROMPT.format(
                juror_id=i+1,
                question=question,
                initial_verdict=initial_verdicts[i],
                other_id1=others[0][0],
                other_verdict1=others[0][1],
                other_id2=others[1][0],
                other_verdict2=others[1][1]
            )
            res = self.client.query_llm(prompt, temperature=TEMPERATURE)
            final_verdicts.append(res['text'])

        # Step 3: Majority Vote
        votes = {"Yes": 0, "No": 0}
        extracted_answers = []
        for v in final_verdicts:
            ans = self.helper_agent.extract_answer(v)
            extracted_answers.append(ans)
            if ans in votes:
                votes[ans] += 1
        
        majority_vote = "Yes" if votes["Yes"] >= votes["No"] else "No"
        disagreement_score = 1 if (votes["Yes"] > 0 and votes["No"] > 0) else 0
        
        return {
            "initial_verdicts": initial_verdicts,
            "final_verdicts": final_verdicts,
            "extracted_answers": extracted_answers,
            "votes": votes,
            "majority_vote": majority_vote,
            "disagreement_score": disagreement_score
        }
