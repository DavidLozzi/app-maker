import httpx
import json
import logging
import os
import regex

log = logging.getLogger("app")


all_tokens = 0

APIM_O1_URL = os.getenv("APIM_O1_URL")
APIM_O1_KEY = os.getenv("APIM_O1_KEY")
APIM_4O_URL = os.getenv("APIM_4O_URL")
APIM_4O_KEY = os.getenv("APIM_4O_KEY")


async def call_gpt_4o(messages, json_format=False):
    payload_json = {
        "messages": messages,
        "stop": "",
        "temperature": 0.2,
        "max_tokens": 4000,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stream": False,
    }
    if json_format:
        payload_json["response_format"] = {"type": "json_object"}

    payload = json.dumps(payload_json)
    headers = {"api-key": APIM_4O_KEY, "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(APIM_4O_URL, headers=headers, data=payload)

        if response.status_code != 200:
            log.error(f"call_gpt_4o error: {response.status_code}: {response.text}")
    return response.json()


async def call_gpt_o1(messages):
    global all_tokens
    headers = {"api-key": APIM_O1_KEY, "Content-Type": "application/json"}

    payload = {
        "messages": messages,
        "max_completion_tokens": 25000,
    }
    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            APIM_O1_URL, headers=headers, data=json.dumps(payload)
        )
        if response.status_code != 200:
            log.error(f"call_gpt_o1 error: {response.status_code}: {response.text}")
            return None

        resp_json = response.json()
        tokens = resp_json["usage"]["total_tokens"]
        all_tokens += tokens
        log.info(f"Tokens used: {tokens}, Total tokens used: {all_tokens}")
        print(resp_json["choices"][-1]["message"]["content"])

        return resp_json


async def gpt_o1_json(messages=[]):
    try:
        messages[0]["role"] = "user"
        response = await call_gpt_o1(messages)

        json_match = r"{(?:[^{}]|(?R))*}"
        match = regex.search(
            json_match,
            response["choices"][-1]["message"]["content"],
            regex.DOTALL | regex.VERBOSE,
        )
        print(match.group(0))
        return match.group(0)
    except Exception as e:
        error = f"gpt_json: {str(e)}"
        log.error(error)
        raise Exception(error)
