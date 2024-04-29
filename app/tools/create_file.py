import os
import logging

log = logging.getLogger("app")


def create_file(file_path, file_name, file_contents):
    try:
        os.makedirs(file_path, exist_ok=True)
        file_full_path = os.path.join(file_path, file_name.replace("./", ""))
        with open(file_full_path, "w") as file:
            file.write(file_contents)
        return f"File '{file_name}' created successfully."
    except Exception as e:
        error = f"Error creating file '{file_name}': {str(e)}"
        log.error(f"create_file: {error}")
        return error
