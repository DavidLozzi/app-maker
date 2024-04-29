import time
import json
from openai import OpenAI
import logging

log = logging.getLogger("app")


all_tokens = []


def gpt_messages(messages=[], in_json=False):
    global all_tokens
    try:
        client = OpenAI()

        params = {
            "model": "gpt-4-turbo-preview",
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": 4000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }

        if in_json:
            params["response_format"] = {"type": "json_object"}

        start = time.time()
        log.info(f"Calling OpenAI with {len(messages)} messages")
        log.debug(f"Messages: {messages}")
        response = client.chat.completions.create(**params)
        log.info(
            f"Finished in {time.time() - start}s. Used {response.usage.total_tokens} tokens"
        )
        all_tokens.append(response.usage.dict())
        log.debug(f"GPT Response: {response.dict()}")
        log.info(f"Total Tokens Used: {sum([u['total_tokens'] for u in all_tokens])}")
        log.debug(f"All Tokens: {all_tokens}")
        return response.choices[0].message.content
    except Exception as e:
        error = f"gpt_messages: {str(e)}"
        log.error(error)
        raise Exception(error)
