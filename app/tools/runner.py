import json
from app.messages import system_message, user_message
from app.tools.run_command import run_command
from app.tools.get_file_contents import get_file_contents
from app.tools.create_file import create_file
from app.tools.run_python import run_python
from app.tools.human_in_middle import human_in_middle
from app.prompts.create_project import (
    prereq_action_plan_prompt,
    create_the_action_plan_prompt,
    summarize_action_plan_prompt,
)
from app.gpt import gpt_messages
import logging

log = logging.getLogger("app")


def run_tool(tool, source_path):
    log.info(f"Running Command: {tool['tool']}::{tool['params']}")
    target_path = f"{source_path}/target"
    if tool["tool"] == "run_command":
        result = run_command(tool["params"], source_path)
    elif tool["tool"] == "get_file_contents":
        result = get_file_contents(source_path, tool["params"])
    elif tool["tool"] == "create_file":
        result = create_file(target_path, tool["params"][0], tool["params"][1])
    elif tool["tool"] == "run_python":
        result = run_python(tool["params"])
    elif tool["tool"] == "human_in_middle":
        result = human_in_middle(tool["params"])

    log.info(f"Result: {result}")
    return f"Output from tool '{tool['tool']}' with params '{tool['params']}':\n{result}\n\n"


def perform_action(task, task_output, step_output, output_path):
    log.info(task["action"])
    user_prefix = ""
    if task_output:
        user_prefix = f"Previous Tasks:\n{task_output}\n\n"
    messages = [
        system_message(create_the_action_plan_prompt()),
        user_message(
            f"{user_prefix}YOUR NEXT TASK\nName: {task['action']}\nDetails: {task['details']}"
        ),
    ]
    response = gpt_messages(messages=messages, in_json=True)
    log.info("\n*****\n  Perform the Action:")
    log.info(response)
    log.info("\n\n")
    response = json.loads(response)
    for tool in response["tools"]:
        step_output += run_tool(tool, output_path)
    return step_output


def get_existing_summaries(all_action_plans):
    summaries = "\n\n".join(
        [
            f'Summary of Action Plan: {ap["action_plan"]}\n{ap["summary"]}'
            for ap in all_action_plans
            if "summary" in ap
        ]
    )
    return summaries


def get_prerequisites(action_plan, prefix, all_action_plans, target_path):
    log.info(action_plan["action_plan"])
    summaries = get_existing_summaries(all_action_plans)
    if summaries:
        summaries = f"ACTION PLAN SUMMARIES:\n{summaries}"
    messages = [
        system_message(prereq_action_plan_prompt()),
        user_message(
            f"{prefix}{summaries}ACTION PLAN\nName: {action_plan['action_plan']}\nDetails: {action_plan['details']}"
        ),
    ]
    response = gpt_messages(messages=messages, in_json=True)
    log.info("\n*****\nPrerequisites Action Plan:")
    log.info(response)

    tools = json.loads(response)
    if "actions" in tools and len(tools["actions"]) > 0:
        for tool in tools["actions"]:
            tool["output"] = run_tool(tool, target_path)

    return tools


def create_detailed_action_plan(action_plan, prefix, prereqs, all_action_plans):
    log.info(action_plan["action_plan"])
    summaries = get_existing_summaries(all_action_plans)
    if summaries:
        summaries = f"ACTION PLAN SUMMARIES:\n{summaries}"

    user_msg = f"{prefix}{summaries}PREREQUISITES:\n{prereqs}\n\nACTION PLAN\nName: {action_plan['action_plan']}\nDetails: {action_plan['details']}"

    messages = [
        system_message(create_the_action_plan_prompt()),
        user_message(user_msg),
    ]
    response = gpt_messages(messages=messages, in_json=True)
    log.info("\n*****\nAction Plan:")
    log.info(response)
    return response


def create_action_plan_summary(
    prereqs, action_plan, action_plan_name, all_action_plans
):
    log.info(f"Summarizing {action_plan}")
    summaries = get_existing_summaries(all_action_plans)
    if summaries:
        summaries = f"ACTION PLAN SUMMARIES:\n{summaries}"

    messages = [
        system_message(summarize_action_plan_prompt()),
        user_message(
            f"{prereqs}{summaries}\n\nACTION PLAN\nName:{action_plan_name}\n{action_plan}"
        ),
    ]
    response = gpt_messages(messages=messages, in_json=True)
    log.info(f"\n*****\Summary for {action_plan_name}:")
    log.info(response)
    log.info("\n\n")
    return json.loads(response)["summary"]
