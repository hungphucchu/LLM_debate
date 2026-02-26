import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluation.evaluation import ExperimentRunner

def main():
    parser = argparse.ArgumentParser(description="LLM Debate + Judge Pipeline Experiment Runner")
    parser.add_argument(
        "--includeJury", 
        action="store_true", 
        help="Include the Multi-Agent Jury Panel (Bonus) in the experiments"
    )
    args = parser.parse_args()

    print("Welcome to the LLM Debate + Judge Pipeline Experiment Runner.")
    if args.includeJury:
        print("Note: Multi-Agent Jury Panel is ENABLED.")
    else:
        print("Note: Multi-Agent Jury Panel is DISABLED.")

    runner = ExperimentRunner()
    runner.run_all_experiments(samples=5, include_jury=args.includeJury)

if __name__ == "__main__":
    main()
