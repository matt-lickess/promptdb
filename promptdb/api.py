import sys
from typing import Dict, Any

import requests


def query_chatgpt(api_key: str, prompt: str) -> Dict[str, Any]:
    """Query the ChatGPT API to generate an SQL query based on user input and database schema."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error: Failed to connect to ChatGPT API. {e}")
        sys.exit(1)
