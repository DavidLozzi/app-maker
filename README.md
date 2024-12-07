# Repo Converter

Messing around making a little GPT agent to do some work for me.

## Prerequisites

1. Uses an APIM for OpenAI access, and basic REST calls. See `gpt.py` if you want to use another LLM or library.

## Set up

### Install libraries

`python -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements`

### Environment File

Copy `.env.example` to `.env` and fill in your details.

## Using the agent

`python -m app.main path_to_repo mode`

See `mode_to_prompts` in `main.py` for possible modes.

## Debugging

The debugger is configured to test modes.
