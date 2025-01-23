import logging
import os

log = logging.getLogger("app")


def get_file_contents(file_path, tool):
    contents = ""
    file_names = tool["params"]
    for file_name in file_names:
        full_path = os.path.join(file_path, file_name.replace("./", ""))
        try:
            with open(full_path, "r") as file:
                contents += f"File: {file_name}\nContents:\n{file.read()}\n\n"
        except FileNotFoundError as e:
            contents += f"FileNotFoundError: {full_path}::{str(e)}"
            log.error(f"get_file_contents: {contents}")
        except Exception as e:
            contents += f"Exception: {full_path}::{str(e)}"
            log.error(f"get_file_contents: {contents}")

    result = {"action": tool, "output": contents}
    return result
