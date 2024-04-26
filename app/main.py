import argparse
import json
import os
from dotenv import load_dotenv

from app.gpt import gpt_messages
from app.prompts import (
    assessment_prompt,
    perform_the_action_prompt,
)
from app.messages import system_message, user_message
from app.tools.runner import run_tool
from app.utils.file_system import get_folder_inventory, delete_subfolder

load_dotenv()

parser = argparse.ArgumentParser(
    description="List files in a directory in hierarchical format."
)
parser.add_argument("path", type=str, help="The root directory path")

args = parser.parse_args()


def remove_system_message(messages):
    messages.pop(0)


def get_file_contents(file_name):
    with open(f"{args.path}/{file_name}", "r") as file:
        if file_name == ".env":
            params = ""
            for line in file:
                if line.strip() and not line.startswith("#"):
                    param = line.split("=")[0].strip()
                    params += f"{param}=<REDACTED>\n"
            return params
        else:
            return file.read()


def format_file_as_string(file):
    return f"FileName: {file['file']}\nContents:\n```{get_file_contents(file['file'])}```\n\n"


def create_file(file):
    print(f"Creating File: {file['file']}")
    file_path = f"output/{file['file']}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(file["contents"])


def convert_app(messages):
    print("\n\nConvert the app!")
    response = gpt_messages(messages=messages, in_json=True)
    print(f"\nConversion:\n\n{response}")

    files = json.loads(response)
    if isinstance(files, list):
        for file in files:
            create_file(file)
    else:
        create_file(files)


def perform_action(task, task_output, step_output):
    print(task["action"])
    user_prefix = ""
    if task_output:
        user_prefix = f"Previous Tasks:\n{task_output}\n\n"
    messages = [
        system_message(perform_the_action_prompt()),
        user_message(
            f"{user_prefix}YOUR NEXT TASK\nName: {task['action']}\nDetails: {task['details']}"
        ),
    ]
    response = """{
    "tools": [
    {
      "tool": "run_command",
      "params": ["ls -R"]
    }
    ],
    "actions": [],
    "outputs": []
  }"""
    response = gpt_messages(messages=messages, in_json=True)
    print("\n*****\n  Perform the Action:")
    print(response)
    print("\n\n")
    response = json.loads(response)
    for tool in response["tools"]:
        step_output += run_tool(tool, args.path)
    return step_output


def doit():
    delete_subfolder(args.path, "target")
    delete_subfolder(args.path, "venv")
    folder_struct = get_folder_inventory(args.path)
    messages = [
        system_message(assessment_prompt()),
        user_message(f"Here's my repo's folder structure:\n\n{folder_struct}"),
    ]
    response = """{
  "actions": [
  {
    "action": "review_directory",
    "details": "Ensure all files and their purposes are correctly understood before proceeding.",
    "order": 1
  },
  {
    "action": "create_environment",
    "details": "Set up a new Python virtual environment to ensure dependencies are isolated.",
    "order": 2
  },
  {
    "action": "install_dependencies",
    "details": "Identify and install Python equivalents of Node.js dependencies listed in package.json.",
    "order": 3
  },
  {
    "action": "convert_js_to_py",
    "details": "Translate index.js to a Python script, focusing on equivalent libraries and syntax.",
    "order": 4
  },
  {
    "action": "convert_json",
    "details": "Review openAIReponse.json to ensure it's compatible with the new Python script.",
    "order": 5
  },
  {
    "action": "update_readme",
    "details": "Modify README.md to reflect the new Python setup and usage instructions.",
    "order": 6
  },
  {
    "action": "create_gitignore",
    "details": "Update .gitignore for Python standards, including the virtual environment and bytecode files.",
    "order": 7
  },
  {
    "action": "remove_js_files",
    "details": "Delete the original Node.js files (index.js, package-lock.json, package.json) after successful conversion and testing.",
    "order": 8
  },
  {
    "action": "handle_env_variables",
    "details": "Convert .env file usage to Python, using python-dotenv or a similar library.",
    "order": 9
  },
  {
    "action": "final_test",
    "details": "Perform comprehensive testing to ensure the Python version functions as expected, including environment variable loading and API responses.",
    "order": 10
  },
  {
    "action": "commit_changes",
    "details": "Commit the changes to the repository, including the deletion of Node.js files and addition of Python files.",
    "order": 11
  }
  ]
}"""
    response = gpt_messages(messages=messages, in_json=True)
    print(f"\n*****\nActions:\n\n{response}")

    tasks = json.loads(response)["actions"]
    tasks = sorted(tasks, key=lambda task: task["order"])
    current_step = int(tasks[0]["order"])
    last_step = int(tasks[-1]["order"])
    task_output = f"Repo files and folders:\n{json.dumps(folder_struct)}\n\n"
    while current_step <= last_step:
        step_output = ""
        for task in [task for task in tasks if task["order"] == current_step]:
            if int(task["order"]) == current_step:
                step_output = perform_action(task, task_output, step_output)
        current_step += 1
        task_output += step_output
    return


if __name__ == "__main__":
    doit()


#     return
#     messages.append(assistant_message(response))

#     remove_system_message(messages)
#     messages.insert(0, system_message(assess_the_application()))

#     get_files = True
#     cnt = 0
#     while get_files:
#         cnt += 1
#         response = gpt_messages(messages=messages, in_json=True)
#         print("\n*****\n  Ask for Files:")
#         messages.append(assistant_message(response))

#         try:
#             files = json.loads(response)
#             if len(files) == 0:
#                 print("\n\n  Nothing received\n\n")
#                 get_files = False
#                 break

#             if "summary" in files:
#                 print(f"Summary of what the app does: {files['summary']}")
#                 get_files = False
#                 break

#             file_contents = ""
#             if isinstance(files, list):
#                 for file in files:
#                     print(f"  File: {file['file']}")
#                     file_contents += format_file_as_string(file)
#             else:
#                 if "file" in files:
#                     print(f"  File: {files['file']}")
#                     file_contents += format_file_as_string(files)

#             print(f"  Sending File Contents:{file_contents[:100]}")

#             messages.append(user_message(file_contents))

#             # if cnt == 3:
#             #     break
#         except json.JSONDecodeError as e:
#             print(f"JSON Error: {e}")
#         except Exception as e:
#             print(f"Error: {e}")

#     remove_system_message(messages)
#     messages.insert(0, system_message(convert_the_app()))
#     convert_app(messages)


# if __name__ == "__main__":
#     doit()
