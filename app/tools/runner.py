from app.tools.run_command import run_command
from app.tools.get_file_contents import get_file_contents
from app.tools.create_file import create_file
from app.tools.run_python import run_python
from app.tools.human_in_middle import human_in_middle
from app.tools.create_image import create_image
import csv
import logging
import os

log = logging.getLogger("app")


def flatten_result(result):
    flat_result = {}
    for key, value in result.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flat_result[f"{key}_{sub_key}"] = sub_value
        else:
            flat_result[key] = value
    return flat_result


def output_to_csv(file_path, result):
    flat_result = flatten_result(result)
    keys = flat_result.keys()
    output_path = os.path.join(file_path, "tools_output.csv")
    with open(output_path, "a", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writerow(flat_result)


async def run_tool(tool, source_path):
    log.info(f"Running Command: {tool['tool']}::{tool['params']}")
    if tool["tool"] == "run_command":
        result = run_command(source_path, tool)
    elif tool["tool"] == "get_file_contents":
        result = get_file_contents(source_path, tool)
    elif tool["tool"] == "create_file":
        result = create_file(source_path, tool)
    elif tool["tool"] == "run_python":
        result = run_python(source_path, tool)
    elif tool["tool"] == "human_in_middle":
        result = human_in_middle(tool)
    elif tool["tool"] == "create_image":
        log.info("*** TBD Creating Image")
        result = await create_image(source_path, tool)
    elif tool["tool"] == "clear_previous":
        log.info("*** TBD Clearing Previous Output")

    log.debug(f"Result: {result}")

    output_to_csv(source_path, result)

    return result


previous_attempts = []


async def run_tools(tools, source_path):
    step_outputs = []
    for tool in tools:
        step_outputs.append(await run_tool(tool, source_path))
    return step_outputs
