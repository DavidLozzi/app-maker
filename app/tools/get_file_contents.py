import logging

log = logging.getLogger("app")


def get_file_contents(file_path, file_names):
    contents = ""
    for file_name in file_names:
        full_path = file_path + "/" + file_name
        try:
            with open(full_path, "r") as file:
                contents += f"File: {file_name}\nContents:\n{file.read()}\n\n"
        except FileNotFoundError as e:
            contents += f"Error with File: {file_name}\File not found\n\n"
            log.error(f"get_file_contents: {contents} {str(e)}")
        except Exception as e:
            contents += f"Error with File: {file_name}\n{str(e)}\n\n"
            log.error(f"get_file_contents: {file_name} {str(e)}")
    return contents
