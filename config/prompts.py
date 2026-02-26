# Phase 1: Initialization
DEBATER_A_INIT = """You are Debater A (Proponent). 
The question is: {question}
Your goal is to argue in favor of a specific answer to this question. 
State your initial position clearly, provide a brief logical reasoning for your position, and finally state your answer in exactly this format: 'Answer is yes' or 'Answer is no'.
Do not see the other debater's response yet.
"""

DEBATER_B_INIT = """You are Debater B (Opponent). 
The question is: {question}
As the Opponent, your role is to provide a robust counter-perspective or defend an alternative to the proponent's view. 
State your initial position clearly, provide a brief logical reasoning for your position, and finally state your answer in exactly this format: 'Answer is yes' or 'Answer is no'.
Do not see the other debater's response yet.
"""

# Phase 2: Multi-Round Debate
DEBATER_A_ROUND = """You are Debater A (Proponent). 
Question: {question}
Current Debate Transcript:
{transcript}

Your task is to:
1. Construct a logically coherent argument in favor of your candidate answer.
2. Cite evidence from the problem context if possible.
3. Rebut any counterarguments made by Debater B in the previous round.
Use Chain-of-Thought reasoning to explain your points.
Finally state your answer in exactly this format: 'Answer is yes' or 'Answer is no'.
"""

DEBATER_B_ROUND = """You are Debater B (Opponent). 
Question: {question}
Current Debate Transcript:
{transcript}

Your primary goal is to argue against Debater A's position. As the Opponent, you MUST:
1. Identify specific logical flaws or factual errors in Debater A's reasoning.
2. Present counterevidence to refute Debater A's claims.
3. Defend your own position and explain why it is more likely to be correct.
Use Chain-of-Thought reasoning to explain your points.
Finally state your answer in exactly this format: 'Answer is yes' or 'Answer is no'.
"""

# Phase 3: Judgment
JUDGE_PROMPT = """You are an impartial Judge observing a structured debate.
Question: {question}
Ground Truth (for internal reference): {ground_truth}

Full Debate Transcript:
{transcript}

Your task is to provide a structured evaluation:
1. Provide a Chain-of-Thought analysis of both debaters' arguments.
2. Identify the strongest and weakest arguments from each side.
3. Render a final verdict: Which answer is more likely to be correct? (Finally state 'Answer is yes' or 'Answer is no')
4. Provide a confidence score for your verdict on a scale of 1-5 (State 'Confidence Score: [1-5]').
"""

# Bonus: Jury Deliberation
JURY_INITIAL_PROMPT = """You are Juror {juror_id} in a 3-member judicial panel. 
Review the following debate and provide your initial verdict.

Question: {question}
Full Debate Transcript:
{transcript}

Provide a brief analysis and conclude with exactly 'Answer is yes' or 'Answer is no'.
"""

JURY_DELIBERATION_PROMPT = """You are Juror {juror_id} in a 3-member judicial panel. 
You have seen the debate, and now you can see the initial verdicts of your fellow jurors.

Question: {question}
Your initial verdict: {initial_verdict}

Fellow Juror {other_id1}'s verdict: {other_verdict1}
Fellow Juror {other_id2}'s verdict: {other_verdict2}

Reflect on their reasoning. Has your position changed? 
Provide your final, definitive verdict and conclude with exactly 'Answer is yes' or 'Answer is no'.
"""

# Phase 4: Baselines
DIRECT_QA_PROMPT = """Question: {question}
Provide a direct answer with Chain-of-Thought reasoning. Finally state 'Answer is yes' or 'Answer is no'.
"""

SELF_CONSISTENCY_PROMPT = """Question: {question}
Think step-by-step and provide a direct answer. Finally state 'Answer is yes' or 'Answer is no'.
"""

# Sample StrategyQA dataset subset
STRATEGY_QA_SAMPLE = [
    {
        "question": "Did the Roman Empire exist at the same time as the Mayan civilization?",
        "answer": "Yes",
        "difficulty": "Medium"
    },
    {
        "question": "Can a human survive on Mars without a spacesuit?",
        "answer": "No",
        "difficulty": "Easy"
    },
    {
        "question": "Was George Washington alive during the American Civil War?",
        "answer": "No",
        "difficulty": "Medium"
    },
    {
        "question": "Does the Earth's moon rotate on its axis?",
        "answer": "Yes",
        "difficulty": "Medium"
    },
    {
        "question": "Could a T-Rex have seen a stegosaurus in person?",
        "answer": "No",
        "difficulty": "Hard"
    }
]
