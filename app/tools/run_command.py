import subprocess


def run_command(command, file_path):
    try:
        output = subprocess.check_output(
            " ".join(command), cwd=file_path, shell=True, stderr=subprocess.STDOUT
        )
        output = output.decode("utf-8").strip()

        result = {"command": command, "output": output}

        return result
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during command execution
        error = e.output.decode("utf-8").strip()
        result = {"command": command, "error": error}

        return result
