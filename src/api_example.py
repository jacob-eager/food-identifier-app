import os
import re

import prompts
from src.openai_api_connections import send_request

def parse_recipe(response_text):
    match = re.search(r"RECIPE_START\s*(.*?)\s*RECIPE_END", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

if __name__ == "__main__":
    prompt = prompts.generate_prompt("pho")
    openai_api_key = os.getenv("APIKEY")
    response = send_request(prompt, openai_api_key)

    print(parse_recipe(response))
