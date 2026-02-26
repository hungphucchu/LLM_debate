import os

# API Configuration
BASE_URL = "http://10.246.100.230/v1"
API_KEY = "gpustack_095f5cb316bc4b95_fe15f283c2d7de79dd258ca70635bb66"
MODEL_NAME = "Llama-3.1-70B-Instruct-custom"

# Debate Hyperparameters
DEBATE_ROUNDS = 3
TEMPERATURE = 0.7
MAX_TOKENS = 1024

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
