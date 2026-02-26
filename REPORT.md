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
One of the more surprising findings was that the jury panel actually struggled most with the questions we'd consider "Easy." For instance, a basic question about survival on Mars resulted in a maximum Disagreement Score (1.0), whereas "Hard" questions actually saw more consensus. 

This points to a clear disconnect between human common sense and "AI difficulty." It seems that for an LLM, difficulty is less about the complexity of the logic and more about the specific distribution of its training data. It felt like the models were often over-analyzing the simple truths until they essentially tripped over their own logic. Ironically, they seemed much more comfortable and united when following a complex, but ultimately flawed, path for the tougher questions.

---

## 3. Qualitative Analysis & Theoretical Framework

### Case Studies
**Case 1: When being loud beats being right (Roman vs. Mayan)**
In `debate_0.json`, we saw a really interesting failure. The Proponent actually started with the right answer, but the Opponent was so assertive with their incorrect timeline that the Proponent just gave up and agreed. It was almost like the model got "bullied" into a wrong consensus. We started calling this **"Adversarial Collapse"**—it's what happens when the social pressure between the models to reach an agreement overrides the actual facts.

**Case 2: Right answer, wrong reasons (T-Rex vs. Stegosaurus)**
In `debate_4.json`, both models correctly said "No," but their logic was totally backwards. They both convinced themselves that the T-Rex was a plant-eater and the Stegosaurus was a carnivore. It was a clear reminder that the Judge often cares more about whether the argument *sounds* consistent and well-structured than if the facts are actually true. They "won" the debate, but only because they both happened to agree on the same hallucinated facts.

### Main Takeaways
1.  **Errors are contagious**: Just putting more models together doesn't automatically make the system more factual. If none of the agents really know the facts, they tend to just echo each other's mistakes rather than correcting them.
2.  **Style over substance**: LLM Judges can be easily fooled. If a debater uses a well-organized "Chain-of-Thought" style, the judge often rewards that logic even if the underlying information is completely wrong.
3.  **Independence is often better**: Surprisingly, letting the models work alone and taking a majority vote (Self-Consistency) worked much better than having them debate (80% vs 60%). For these kinds of "yes/no" questions, it seems like having a few independent opinions is more reliable than letting the models argue and potentially talk each other into a mistake.

---

## 4. Prompt Engineering & Design Strategy

### Iterative Design
The prompts were refined through several development cycles:
1.  **Initial (Naive)**: Simply asked for a "debate," which led to excessive politeness and lack of critical engagement.
2.  **Persona-Driven (Adversarial)**: Assigned explicit "Opponent" roles with instructions to "expose logical fallacies." This significantly increased the rigor of the Phase 2 rebuttals.
3.  **Constraint-Optimized (Evaluation)**: Implemented strict formatting (e.g., `Answer is yes/no`) to facilitate automated parsing and quantitative evaluation.

### Academic Integrity & Tooling
I developed and coded the vast majority of this project myself, using **Cursor IDE** and **Gemini** primarily as assistants to enhance the workflow. These tools were helpful for streamlining the directory structure and generating some of the initial boilerplate code. However, all of the core reasoning logic, the experimental design, and the final qualitative analysis are entirely my own original work.

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
