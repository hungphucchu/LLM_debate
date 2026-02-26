# LLM Debate with Judge Pipeline: Building Adversarial Multi-Agent Reasoning Systems

**Course**: CS-6263 Natural Language Processing
**Author**: Hung Chu  

---

## 1. Methodology

### System Architecture
The system is designed as a modular multi-agent pipeline composed of three distinct roles:
1.  **Debater A (Proponent)**: Assigned to defend a position.
2.  **Debater B (Opponent)**: Assigned to challenge the proponent, identify logical fallacies, and present counterevidence.
3.  **Judge (Single or Panel)**: An impartial observer that reviews the full debate transcript and renders a final verdict.

The architecture is implemented in Python, using a custom `LLMClient` (OpenAI-compatible) to interface with a Llama-3.1-70B model. The code is structured into modular packages: `agents/` for agent definitions, `client/` for API interactions, `config/` for hyperparameters and prompts, and `evaluation/` for benchmarking.

### Debate Protocol
The pipeline follows a structured 4-phase protocol:
*   **Phase 1: Initialization**: Both debaters generate independent initial positions without seeing each other's responses. If they agree immediately, the system records a consensus and skips to Phase 3.
*   **Phase 2: Multi-Round Debate**: A 3-round exchange where Debater A presents an argument, and Debater B responds with a rebuttal. Each agent receives the full transcript of all previous rounds. An **adaptive stopping criterion** is implemented: if both agents converge to the same answer for two consecutive rounds, the debate ends early.
*   **Phase 3: Judgment**: The Judge (or a Jury Panel of 3) reviews the transcript. The judge must provide a Chain-of-Thought (CoT) analysis, identify the strongest/weakest arguments, and state a final answer ("Answer is yes/no") with a confidence score (1-5).
*   **Phase 4: Evaluation**: The system compares the judge's verdict against the ground truth and calculates accuracy across Direct QA, Self-Consistency, and Debate methods.

### Model Choices & Configuration
*   **Model**: `Llama-3.1-70B-Instruct-custom`.
*   **Temperature**: 0.7 (to allow for creative reasoning while maintaining logical consistency).
*   **Max Tokens**: 1024.
*   **Dataset**: A curated sample from **StrategyQA**, testing multi-hop temporal and commonsense reasoning.

---

## 2. Experiments

### Experimental Setup
We compared three primary reasoning methods:
1.  **Direct QA (Baseline)**: The model answers the question directly with CoT prompting.
2.  **Self-Consistency (Baseline)**: The model answers 3 times independently; the final answer is decided by a majority vote.
3.  **Debate Pipeline**: The full adversarial multi-agent protocol described above.
4.  **Jury Panel (Bonus)**: A 3-member jury that deliberates by seeing each other's initial verdicts before rendering a final vote.

### Quantitative Results
The following table summarizes the performance on a 5-sample StrategyQA subset:

| Method | Accuracy | Avg. Confidence | Notes |
| :--- | :--- | :--- | :--- |
| **Direct QA** | 60% | N/A | High speed, lower reasoning depth. |
| **Self-Consistency (N=3)** | 60% | N/A | Improved stability but same accuracy. |
| **Debate (Single Judge)** | 60% | 4.2/5 | Deep reasoning, but judge sometimes swayed by logic. |
| **Jury Panel (3 Agents)** | 0%* | 3.8/5 | *See Analysis for failure mode. |

### Disagreement vs. Difficulty
The jury panel exhibited higher disagreement on "Hard" questions (e.g., T-Rex vs. Stegosaurus), where initial verdicts often split (2-1). On "Easy" questions (Mars survival), the panel reached consensus more rapidly.

---

## 3. Analysis

### Qualitative Transcript Analysis
**Case 1: The "Roman Empire vs. Mayan" Debate (Failure)**
In this run, both debaters initially agreed on "Yes" but were plagued by **hallucinations**. Debater A claimed the Romans "expanded into Central America," which is historically false. Because both agents shared the same hallucinated premise, the "Adversarial" benefit was lost. This illustrates a key limitation: **adversarial debate only works if at least one agent has access to the correct facts.**

**Case 2: The "T-Rex vs. Stegosaurus" Debate (Success)**
This debate was highly effective. Debater A argued that both were dinosaurs and lived in the "Mesozoic Era." Debater B successfully pinpointed the flaw: the Mesozoic spans 180 million years, and these two lived in different periods (Jurassic vs. Cretaceous). The Judge correctly identified Debater B's temporal evidence as the "Strongest Argument" and reversed the initial plausible but wrong conclusion.

### Theoretical Connections (Irving et al., 2018)
Our findings support Irving et al.'s prediction that debate can help a human (or judge LLM) evaluate claims they aren't experts in. However, we observed that when both agents are "factually impoverished," they tend to reinforce each other's errors—a phenomenon we term **"Hallucination Convergence."**

---

## 4. Prompt Engineering

### Design Process & Iterations
The prompt design underwent three major iterations:
1.  **Iteration 1 (Generic)**: Initial prompts just asked the agents to "debate." This resulted in polite agreement rather than rigorous challenge.
2.  **Iteration 2 (Role Framing)**: We added explicit "Proponent" and "Opponent" personas. Debater B was instructed to "identify specific logical flaws." This significantly improved the adversarial nature of Phase 2.
3.  **Iteration 3 (Format Constraints)**: We found the Judge often gave long-winded answers without a clear binary choice. We implemented a strict output constraint: `Finally state your answer in exactly this format: 'Answer is yes' or 'Answer is no'`. This allowed for automated evaluation.

### Key Decisions
*   **CoT Instructions**: Every prompt includes "Use Chain-of-Thought reasoning." This was critical for the Judge to weigh the *logic* of the arguments rather than just the *confidence* of the tone.
*   **Deliberation Framing**: For the Jury, we used a two-step prompt. Step 1: Independent verdict. Step 2: "Has your position changed based on your peers?" This second step allowed for the "deliberation" required by the bonus prompt.

### Tools and Academic Integrity
This project was developed using **Cursor IDE** and **Gemini-3-flash-preview** as a coding assistant. These tools were used for generating boilerplate code, modularizing the directory structure, and drafting the initial technical descriptions in this report. All reasoning logic, prompt templates, and qualitative analysis were verified and refined by the author to ensure alignment with assignment requirements.

---

## Appendix: Full Prompts

### Debater A (Proponent) - Initialization
```
You are Debater A (Proponent). 
The question is: {question}
Your goal is to argue in favor of a specific answer to this question. 
State your initial position clearly, provide a brief logical reasoning for your position, and finally state your answer in exactly this format: 'Answer is yes' or 'Answer is no'.
```

### Debater B (Opponent) - Round Rebuttal
```
You are Debater B (Opponent). 
Question: {question}
Current Debate Transcript: {transcript}

Your primary goal is to argue against Debater A's position. As the Opponent, you MUST:
1. Identify specific logical flaws or factual errors in Debater A's reasoning.
2. Present counterevidence to refute Debater A's claims.
3. Defend your own position and explain why it is more likely to be correct.
```

### Jury Deliberation Prompt
```
You are Juror {juror_id} in a 3-member judicial panel. 
You have seen the debate, and now you can see the initial verdicts of your fellow jurors.
Reflect on their reasoning. Has your position changed? 
Provide your final, definitive verdict and conclude with exactly 'Answer is yes' or 'Answer is no'.
```
