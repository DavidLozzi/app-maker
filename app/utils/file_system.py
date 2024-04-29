import os
import shutil
from app.tools.run_command import run_command
import logging

log = logging.getLogger("app")


def get_folder_inventory(folder_path):
    folder_struct = run_command(
        [
            "find . -type d \( -name excludeFolder -o -name venv -o -name .git -o -name node_modules \) -prune -o -print | xargs ls -ldls"
        ],
        folder_path,
    )

    log.info(f"\nFiles and Folders to assess:\n{folder_struct}")

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
