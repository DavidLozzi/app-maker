def get_file_contents(file_path, file_names):
    contents = ""
    for file_name in file_names:
        full_path = file_path + "/" + file_name
        try:
            with open(full_path, "r") as file:
                contents += f"File: {file_name}\nContents:\n{file.read()}\n\n"
        except FileNotFoundError:
            contents += f"File: {file_name}\File not found\n\n"
        except Exception as e:
            print(f"Error reading file: {file_name} {str(e)}")
    return contents
