import os
import shutil
from app.tools.run_command import run_command


def get_folder_inventory(folder_path):
    folder_struct = run_command(
        [
            "find . -type d \( -name excludeFolder -o -name venv -o -name .git -o -name node_modules \) -prune -o -print | xargs ls -ldls"
        ],
        folder_path,
    )

    print(f"\nFiles and Folders to assess:\n{folder_struct}")

    return folder_struct


def delete_subfolder(folder_path, folder_name):
    target_path = os.path.join(folder_path, folder_name)
    if os.path.exists(target_path) and os.path.isdir(target_path):
        shutil.rmtree(target_path)
        print(f"Subfolder '{folder_name}' deleted successfully.")
    else:
        print(f"Subfolder '{folder_name}' does not exist.")
