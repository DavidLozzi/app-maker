import argparse
import asyncio
import json
from app.models.output import OutputModel
from dotenv import load_dotenv
from app.gpt import gpt_o1_json

import app.prompts.kt as kt
import app.prompts.tests as tests
import app.prompts.refactor as refactor

from app.tools.get_file_contents import get_file_contents
from app.messages import system_message, user_message
from app.tools.runner import run_tools
from app.utils.file_system import get_folder_inventory
from app.utils.logger import setup_logger

log = setup_logger()
load_dotenv()


mode_to_prompts = {
    "tests": tests.get_prompts,
    "kt": kt.get_prompts,
    "refactor": refactor.get_prompts,
}

parser = argparse.ArgumentParser(
    description="List files in a directory in hierarchical format."
)
parser.add_argument("path", type=str, help="The root directory path")
parser.add_argument(
    "mode",
    type=str,
    help="Mode to run the tool in. 'tests' for tshooting tests. 'create-project' to create a new project",
)


args = parser.parse_args()


def remove_system_message(messages):
    messages.pop(0)


def create_tool(tool, name, params, order=1):
    return {
        "tool": tool,
        "name": name,
        "params": params,
        "order": order,
    }


async def clean_json_string(json_string, error):
    busted_string = json_string
    attempt_cnt = 0
    while True:
        attempt_cnt += 1
        messages = [
            user_message(
                f"""The following JSON string is throwing an error when trying to parse it.
Please fix the json object, it should fit the following format: {json.dumps(OutputModel.model_json_schema())}
Error:{error}
JSON string: {busted_string}"""
            )
        ]
        response = await gpt_o1_json(messages=messages)
        try:
            return json.loads(response)
        except Exception as e:
            log.error(f"attempt {attempt_cnt} to fix JSON failed: {e}")
            busted_string = response
            if attempt_cnt > 5:
                return None


async def doit():
    log.info(f"Running in path: {args.path} with mode: {args.mode}")
    if args.mode in mode_to_prompts:
        log.info(f'Running in "{args.mode}" mode')
        inital_prompt, initial_user_prompt, action_step_complete = mode_to_prompts[
            args.mode
        ]()
    else:
        log.error(f"Unknown mode: {args.mode}")
        return

    folder_struct = get_folder_inventory(args.path)

    readme = get_file_contents(
        args.path,
        create_tool("run_command", "gets the contents of the reamd", ["README.md"]),
    )
    prefix = initial_user_prompt.format(folder_struct=folder_struct, readme=readme)
    messages = [
        system_message(inital_prompt),
        user_message(prefix),
    ]
    log.info("Running prompt initial prompts")
    response = await gpt_o1_json(messages=messages)

    previous = "# PREVIOUS COMMANDS\n\n"
    while True:
        try:
            actions = json.loads(response)["actions"]
        except json.JSONDecodeError as e:
            log.warning(f"JSON Decode Error, trying to clean: {e}")
            new_response = await clean_json_string(response, str(e))
            actions = new_response["actions"]

        if not actions:
            break
        task_output = await run_tools(actions, args.path)
        # HANDLE clear_previous action
        previous += f"{json.dumps(task_output)}\n*****\n"
        log.info(previous)
        messages = [
            system_message(action_step_complete),
            user_message(f"{prefix}\n\n{previous}\n# END PREVIOUS COMMANDS\n\n"),
        ]
        last_actions = "\n".join(
            [f"{action['tool']} - {action['name']}" for action in actions]
        )
        log.info(f"Last actions:\n{last_actions}")
        log.info("Calling GPT")
        response = await gpt_o1_json(messages=messages)

    return


if __name__ == "__main__":
    asyncio.run(doit())
