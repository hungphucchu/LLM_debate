import time
import random
from openai import OpenAI, APIError, APIConnectionError, RateLimitError, AuthenticationError
from config.config import BASE_URL, API_KEY, MODEL_NAME

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
            timeout=30.0
        )
    # Sends a prompt to the LLM and returns a dictionary with response text, token usage, and latency.
    def query_llm(self, prompt, temperature=0.7, max_tokens=500, max_retries=3, **kwargs):
        retries = 0
        while retries <= max_retries:
            try:
                start_time = time.time()
                response = self.client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                duration = time.time() - start_time
                
                return {
                    "text": response.choices[0].message.content,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "response_time": duration
                }

            except AuthenticationError as e:
                return {"error": f"Authentication Error: {e}"}
            except RateLimitError as e:
                print(f"Rate limit hit. Retrying...")
            except (APIConnectionError, APIError) as e:
                print(f"Transient error occurred: {e}. Retrying...")
            except Exception as e:
                return {"error": f"An unexpected error occurred: {e}"}

            wait_time = (2 ** retries) + random.uniform(0, 1)
            print(f"Waiting {wait_time:.2f} seconds before retry {retries + 1}/{max_retries}...")
            time.sleep(wait_time)
            retries += 1

        return {"error": "Error: Maximum retries exceeded."}
