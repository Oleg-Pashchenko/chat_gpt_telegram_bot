import logging

import openai
from app import secure_data


def make_openai_request(question: str) -> str:
    openai.api_key = secure_data.OPENAI_API_KEY
    openai_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=1000,
        timeout=30
    )
    try:
        result = openai_response["choices"][0]["text"].strip()
    except Exception as e:
        logging.error(f"Error: {e}. Program couldn't get message from openai.")
        result = "Server Error!"
    return result


