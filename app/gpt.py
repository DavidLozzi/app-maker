import time
from openai import OpenAI


all_tokens = []


def gpt_messages(messages=[], in_json=False):
    global all_tokens
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
    print(f"Calling OpenAI with {len(messages)} messages")
    response = client.chat.completions.create(**params)
    print(
        f"Finished in {time.time() - start}s. Used {response.usage.total_tokens} tokens"
    )
    all_tokens.append(response.usage)
    print(f"Total Tokens Used: {sum([u.total_tokens for u in all_tokens])}")
    return response.choices[0].message.content
