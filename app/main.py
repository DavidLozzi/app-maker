import argparse
import asyncio
import json
from dotenv import load_dotenv
from art import text2art  # Import the art library

load_dotenv()

# Generate and print ASCII art
print(text2art("Lozzi's Gen-neer"))

from app.models.output import OutputModel
from app.gpt import gpt_o1_json

from app.prompts.kt import KTPrompts
from app.prompts.tests import TestPrompts
from app.prompts.refactor import RefactorPrompts
from app.prompts.custom import CustomPrompts

from app.tools.get_file_contents import get_file_contents
from app.messages import system_message, user_message
from app.tools.runner import run_tools
from app.utils.file_system import get_folder_inventory
from app.utils.logger import setup_logger

log = setup_logger()

mode_to_prompts = {
    "tests": TestPrompts,
    "kt": KTPrompts,
    "refactor": RefactorPrompts,
    "custom": CustomPrompts,
}

parser = argparse.ArgumentParser(
    description="List files in a directory in hierarchical format."
)
parser.add_argument("path", type=str, help="The root directory path")
parser.add_argument(
    "mode",
    type=str,
    help="Mode to run the tool in. 'tests' for troubleshooting tests. 'create-project' to create a new project",
)
parser.add_argument(
    "custom", type=str, help="Custom requirements for the 'custom' mode", default=""
)

try:
    args = parser.parse_args()
except SystemExit as e:
    if e.code == 2:
        log.error("Error: Invalid arguments")
    else:
        raise


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
Please fix the json object, it should fit the following format: {json.dumps(OutputModel.schema_json())}
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


def get_initial_messages(inital_prompt, initial_user_prompt):
    prefix = get_prefix_user_message(initial_user_prompt)
    messages = [
        system_message(inital_prompt),
        user_message(prefix),
    ]
    return messages


def get_prefix_user_message(initial_user_prompt):
    readme = get_file_contents(
        args.path,
        create_tool("run_command", "gets the contents of the readme", ["README.md"]),
    )
    folder_struct = get_folder_inventory(args.path)
    return initial_user_prompt.format(folder_struct=folder_struct, readme=readme)


async def doit():
    log.info(f"Running in path: {args.path} with mode: {args.mode}")
    if args.mode in mode_to_prompts:
        if args.mode == "custom":
            prompts = mode_to_prompts[args.mode](args.custom)
        else:
            prompts = mode_to_prompts[args.mode]()

        inital_prompt, initial_user_prompt, action_step_complete = prompts.get_prompts()
    else:
        log.error(f"Unknown mode: {args.mode}")
        return

    messages = get_initial_messages(inital_prompt, initial_user_prompt)
    log.info("Running initial prompts")
    response = await gpt_o1_json(messages=messages)

    previous = "# Previous\n"
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
        log.debug(f"Previous:\n{previous}")
        prefix = get_prefix_user_message(initial_user_prompt)
        messages = [
            system_message(action_step_complete),
            user_message(f"{prefix}\n\n{previous}\n# End Previous\n\n"),
        ]
        last_actions = "\n".join(
            [f"{action['tool']} - {action['name']}" for action in actions]
        )
        log.debug(f"Last actions:\n{last_actions}")
        response = await gpt_o1_json(messages=messages)

    return


if __name__ == "__main__":
    asyncio.run(doit())
