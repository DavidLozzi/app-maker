import os
import shutil
from app.tools.run_command import run_command
import logging

log = logging.getLogger("app")


def get_folder_inventory(folder_path):
    exclude_dirs = [
        "excludeFolder",
        "build",
        "bin",
        "venv",
        ".venv",
        ".git",
        "node_modules",
        "__pycache__",
    ]
    exclude_params = " -o ".join([f"-name {d}" for d in exclude_dirs])
    command = (
        f"find . -type d \\( {exclude_params} \\) -prune -o -print | xargs ls -ldls"
    )

    folder_struct = run_command(
        folder_path,
        {
            "tool": "run_command",
            "name": "get_folder_inventory",
            "params": [command],
            "order": 1,
        },
    )

    log.info(f"Files and Folders included from {folder_path}")
    log.debug(folder_struct)

    return folder_struct


def delete_subfolder(folder_path, folder_name):
    try:
        target_path = os.path.join(folder_path, folder_name)
        if os.path.exists(target_path) and os.path.isdir(target_path):
            shutil.rmtree(target_path)
            log.info(f"Subfolder '{folder_name}' deleted successfully.")
        else:
            log.info(f"Subfolder '{folder_name}' does not exist.")
    except Exception as e:
        error = f"delete_subfolder: {str(e)}"
        log.error(error)


def empty_directory(folder_path):
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        log.info(f"Directory '{folder_path}' emptied successfully.")
    except Exception as e:
        error = f"empty_directory: {str(e)}"
        log.error(error)
