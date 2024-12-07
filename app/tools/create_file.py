import os
import logging

log = logging.getLogger("app")


def create_file(file_path, tool):
    try:
        file_name = tool["params"][0]
        file_contents = tool["params"][1]
        file_full_path = os.path.join(file_path, file_name.replace("./", ""))
        os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        with open(file_full_path, "w") as file:
            file.write(file_contents)
        return {"action": tool, "output": f"File '{file_name}' created successfully."}
    except Exception as e:
        error = f"Error creating file '{file_name}': {str(e)}"
        log.error(f"create_file: {error}")
        return {"action": tool, "error": error}
