# LLM Debate with Judge Pipeline: Building Adversarial Multi-Agent Reasoning Systems

**Course:** CS-6263 Natural Language Processing  
**Author:** Hung Chu 

---

## 1. Executive Summary & Methodology

This research project explores the efficacy of adversarial multi-agent debate systems in enhancing the reasoning capabilities of Large Language Models (LLMs). By structuring interactions between competing agents and an impartial judge, we aim to mitigate hallucinations and improve the factuality of model outputs.

### System Architecture
The framework is designed as a modular pipeline featuring three specialized agentic roles:
1.  **Debater A (Proponent)**: Tasked with articulating and defending a specific position.
2.  **Debater B (Opponent)**: Tasked with deconstructing the proponent's arguments, identifying logical fallacies, and presenting empirical counterevidence.
3.  **The Judiciary (Judge or Jury)**: An impartial evaluator that synthesizes the debate transcript to render a final, reasoned verdict.

The implementation is written in Python and leverages a custom `LLMClient` to interface with the `Llama-3.1-70B-Instruct` model. The codebase is organized into modular packages (`agents/`, `client/`, `config/`, `evaluation/`) to ensure scalability and maintainability.

### The Debate Protocol
We implemented a structured 4-phase interaction protocol:
*   **Phase 1: Initial Posture**: Agents generate independent positions without prior interaction. If immediate consensus is reached, the system skips to Phase 3.
*   **Phase 2: Dialectical Exchange**: A multi-round (default: 3) debate where agents exchange rebuttals. We implemented an **adaptive termination criterion**: if agents reach a stable consensus for two consecutive rounds, the debate concludes early to preserve computational resources.
*   **Phase 3: Deliberated Judgment**: The Judge (or a 3-member Jury Panel) performs a Chain-of-Thought (CoT) analysis of the transcript, weighing argument strength against factual evidence to provide a final verdict with a confidence score (1-5).
*   **Phase 4: Empirical Evaluation**: Verdicts are benchmarked against ground-truth labels from the **StrategyQA** dataset, measuring accuracy across Direct QA, Self-Consistency, and Debate methodologies.

---

## 2. Empirical Evaluation

### Experimental Framework
Our experiments compared the following reasoning paradigms:
1.  **Direct QA (Baseline)**: Standard zero-shot CoT prompting.
2.  **Self-Consistency (Baseline)**: A majority-vote ensemble of three independent runs.
3.  **Debate Pipeline**: The full adversarial protocol with a single judge.
4.  **Jury Panel (Extension)**: A 3-member judicial panel that undergoes a "peer-review" deliberation phase before voting.

### Quantitative Analysis
The table below summarizes performance across a 5-sample subset of multi-hop reasoning questions:

| Methodology | Accuracy | Avg. Confidence | Observations |
| :--- | :--- | :--- | :--- |
| **Direct QA** | 40% | N/A | High latency-efficiency; prone to logical shortcuts. |
| **Self-Consistency (N=3)** | 80% | N/A | Significant error-correction via statistical consensus. |
| **Debate (Single Judge)** | 60% | 4.4 / 5 | High reasoning depth; judge occasionally biased by "logical tone." |
| **Jury Panel (3 Agents)** | 60% | 4.0 / 5 | Deliberation refined the logic but did not always correct shared hallucinations. |

### Subjective Difficulty vs. Disagreement
Interestingly, we observed a **Disagreement Score of 1.0** on questions categorized as "Easy" (e.g., survival on Mars), while consensus was higher on "Hard" questions. This suggests that "AI Difficulty" is often a function of training data distribution rather than human common sense—models may over-complicate simple truths while converging on complex, albeit incorrect, logic.

---

## 3. Qualitative Analysis & Theoretical Framework

### Case Studies
**Case 1: Adversarial Collapse (Roman vs. Mayan)**
In `debate_0.json`, we observed a critical failure mode: the correct agent (Proponent) was "out-argued" by a more assertive but incorrect Opponent. Instead of maintaining factual integrity, the Proponent conceded to the Opponent's incorrect timeline, leading to a unanimous (and wrong) consensus. We term this **"Adversarial Collapse"**—where social pressure within the model interaction overrides factual accuracy.

**Case 2: Logic-Fact Decoupling (T-Rex vs. Stegosaurus)**
In `debate_4.json`, both agents correctly concluded "No" but based their reasoning on a complete role reversal (claiming T-Rex was a herbivore). This reinforces a key insight: **Judges often reward internal consistency and "form" over external factuality.** The models "won" the argument with the right conclusion but through a completely hallucinated premises.

### Core Observations
1.  **Hallucination Contagion**: Multi-agent systems are not inherently more factual. If agents lack a robust internal knowledge base, they tend to synchronize their errors rather than correct them.
2.  **Form over Substance**: LLM Judges are highly susceptible to well-structured but factually incorrect Chain-of-Thought reasoning.
3.  **The Wisdom of Independence**: Our findings show that Self-Consistency (independent runs) outperformed the socialized Debate pipeline (80% vs 60%). This suggest that for binary reasoning, **independent variety** is often more valuable than **adversarial interaction**.

---

## 4. Prompt Engineering & Design Strategy

### Iterative Design
The prompts were refined through several development cycles:
1.  **Initial (Naive)**: Simply asked for a "debate," which led to excessive politeness and lack of critical engagement.
2.  **Persona-Driven (Adversarial)**: Assigned explicit "Opponent" roles with instructions to "expose logical fallacies." This significantly increased the rigor of the Phase 2 rebuttals.
3.  **Constraint-Optimized (Evaluation)**: Implemented strict formatting (e.g., `Answer is yes/no`) to facilitate automated parsing and quantitative evaluation.

### Academic Integrity & Tooling
This project was developed using **Cursor IDE** and **Gemini-3-flash-preview**. These tools assisted in modularizing the codebase, generating boilerplate functionality, and drafting technical descriptions. All core reasoning logic, experimental design, and qualitative interpretations are the original work of the author.

---

## Appendix: Core Prompt Templates

### Debater B (Opponent) - Rebuttal Logic
```text
You are Debater B (Opponent). 
Question: {question}
Current Transcript: {transcript}

Your goal is to challenge Debater A. You MUST:
1. Identify specific logical flaws or factual errors in A's reasoning.
2. Present counterevidence to refute their claims.
3. Defend your position with Chain-of-Thought logic.
Finalize with: 'Answer is yes' or 'Answer is no'.
```

### Jury Deliberation Logic
```text
You are Juror {juror_id}. You have reviewed the debate and the initial verdicts of your peers.
Reflect on their reasoning. Has your position shifted? 
Provide your final verdict and conclude with: 'Answer is yes' or 'Answer is no'.
```
