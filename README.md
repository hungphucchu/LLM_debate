# LLM Debate + Judge Pipeline

This repository implements a structured multi-agent debate system for complex reasoning tasks, as part of Assignment 2 for the LLM & Agentic Systems course.

## System Architecture

The pipeline consists of modular LLM agents that interact via a structured protocol:
- **Debater A (Proponent)**: Argues in favor of a candidate answer.
- **Debater B (Opponent)**: Explicitly identifies flaws in Debater A's reasoning, presents counterevidence, and defends its own position.
- **Judge (Single)**: Observes the transcript and renders a final verdict with Chain-of-Thought (CoT) reasoning.
- **Jury Panel (Multi-Agent)**: An optional panel of 3+ LLM judges that deliberate (inspired by VERDICT) to provide a more robust majority-voted verdict.

## How to Run

### 1. Prerequisites
Ensure you have Python 3.9+ and the required packages installed:
```bash
pip install -r requirements.txt
```

### 2. Configuration
API settings (BASE_URL, API_KEY), hyperparameters (DEBATE_ROUNDS, TEMPERATURE), and prompt templates are located in the `config/` directory.

### 3. Running Experiments
To run the full experiment suite (Debate vs. Direct QA vs. Self-Consistency) on a sample dataset:
```bash
python main.py
```

To include the **Multi-Agent Jury Panel (Bonus)** in the experiments:
```bash
python main.py --includeJury
```

### 4. Running the Web UI
To launch the interactive debate interface (includes a toggle for the Jury Panel):
```bash
python app.py
```
Then navigate to `http://localhost:5000` in your browser.

## Bonus: Multi-Agent Judge Panel (Jury)
This repository includes an implementation of a 3-member judicial panel inspired by **VERDICT** (Kalra et al., 2025). 
- **Deliberation Protocol**: Jurors first render independent verdicts, then review peer reasoning before providing a final deliberated verdict.
- **Analytics**: The system calculates disagreement scores and correlates them with question difficulty (Easy, Medium, Hard).
- **Consensus**: The final answer is determined by a deliberated majority vote.

## Project Structure
- `agents/`: Modular agent classes (`base_agent.py`, `debater_agent.py`, `judge_agent.py`, `jury.py`).
- `client/`: API client interaction (`api_basics.py`).
- `config/`: Centralized configuration and prompt templates.
- `evaluation/`: Benchmarking and baseline logic (`evaluation.py`, `baselines.py`).
- `orchestrator.py`: Implements the 4-phase debate protocol.
- `app.py`: Simple Flask web interface for live debates.
- `logs/`: Contains JSON logs of every debate transcript.
- `results/`: Contains experiment summaries.
