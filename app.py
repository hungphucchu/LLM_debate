from flask import Flask, render_template, request, jsonify
from orchestrator import DebateOrchestrator
from client.api_basics import LLMClient
import os

app = Flask(__name__)
client = LLMClient()
orchestrator = DebateOrchestrator(client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_debate', methods=['POST'])
def run_debate():
    data = request.json
    question = data.get('question')
    ground_truth = data.get('ground_truth', 'Unknown')
    include_jury = data.get('include_jury', False)
    
    result = orchestrator.run_debate(question, ground_truth, include_jury=include_jury)
    return jsonify(result)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)
