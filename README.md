# Multi-Agent Adversarial Debate Pipeline

This repository contains the implementation of a structured multi-agent debate framework designed for complex commonsense and temporal reasoning tasks. Developed as part of a graduate-level exploration into LLM reasoning, the system evaluates the impact of adversarial interaction on factual accuracy and logical consistency.

## Overview

The core objective of this project is to benchmark adversarial debate against standard prompting techniques. The system orchestrates a "Trial by Dialectic," where competing agents argue opposing viewpoints while an impartial judge (or multi-agent jury) renders a final verdict based on the quality of the reasoning and evidence presented.

## System Architecture

The pipeline leverages a modular, object-oriented design composed of specialized agents:

*   **Debater A (Proponent)**: Responsible for establishing and defending the primary thesis.
*   **Debater B (Opponent)**: Tasked with critical rebuttal, identifying logical inconsistencies in the proponent’s argument, and providing empirical counter-points.
*   **Adjudicator (Judge)**: Analyzes the full dialectical exchange using Chain-of-Thought (CoT) reasoning to provide a final decision.
*   **Jury Panel (Extension)**: A three-member judicial panel inspired by the **VERDICT** framework (Kalra et al., 2025), utilizing multi-agent deliberation to reach a robust consensus.

## Getting Started

### Prerequisites

The project requires **Python 3.9+**. Install dependencies via the provided requirements file:

```bash
pip install -r requirements.txt
```

### Configuration

System parameters, including API endpoints, model hyperparameters (temperature, max tokens), and role-specific prompt templates, are centralized in the `config/` directory for transparency and ease of experimentation.

### Execution

#### 1. Empirical Benchmarking
To execute the full benchmarking suite (comparing Debate, Direct QA, and Self-Consistency):

```bash
python main.py
```

To enable the **Multi-Agent Jury Panel** (Bonus feature) in the experimental run:

```bash
python main.py --includeJury
```

#### 2. Interactive Web Interface
A Flask-based web application is provided for real-time visualization of the debate process:

```bash
python app.py
```
Access the interface at `http://localhost:5000`.

## Advanced Features: Multi-Agent Jury (VERDICT)

The system implements a sophisticated judicial deliberation protocol:
1.  **Independent Assessment**: Each juror renders an initial, blinded verdict.
2.  **Deliberation**: Jurors review the reasoning of their peers to identify potential biases or overlooked evidence.
3.  **Final Consensus**: A deliberated majority vote determines the final outcome.

The framework also tracks **Disagreement Scores** to analyze how model consensus correlates with human-perceived question difficulty.

## Repository Structure

```text
├── agents/          # Modular agent definitions (Base, Debater, Judge, Jury)
├── client/          # API interaction layer (OpenAI-compatible)
├── config/          # Prompt templates and system hyperparameters
├── evaluation/      # Benchmarking logic and baseline implementations
├── logs/            # Comprehensive JSON transcripts of every debate
├── results/         # Quantitative summary data
├── orchestrator.py  # Main 4-phase debate protocol implementation
└── app.py           # Flask web UI entry point
```
