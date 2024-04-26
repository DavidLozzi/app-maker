from app.tools.run_command import run_command
from app.tools.get_file_contents import get_file_contents
from app.tools.create_file import create_file
from app.tools.run_python import run_python


def run_tool(tool, source_path):
    print(f"Running Command: {tool['tool']}::{tool['params']}")
    target_path = f"{source_path}/target"
    if tool["tool"] == "run_command":
        result = run_command(tool["params"], source_path)
    elif tool["tool"] == "get_file_contents":
        result = get_file_contents(source_path, tool["params"])
    elif tool["tool"] == "create_file":
        result = create_file(target_path, tool["params"][0], tool["params"][1])
    elif tool["tool"] == "run_python":
        result = run_python(tool["params"])

    print(f"Result: {result}")
    return f"Output from tool '{tool['tool']}' with params '{tool['params']}':\n{result}\n\n"
