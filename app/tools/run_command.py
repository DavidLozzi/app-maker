import subprocess
import logging

log = logging.getLogger("app")


def run_command(command, file_path):
    try:
        output = subprocess.check_output(
            " ".join(command), cwd=file_path, shell=True, stderr=subprocess.STDOUT
        )
        output = output.decode("utf-8").strip()

        result = {"command": command, "output": output}

        return result
    except subprocess.CalledProcessError as e:
        error = e.output.decode("utf-8").strip()
        result = {"command": command, "error": error}
        log.error(f"run_command CalledProcessError: {str(e)}")
        return result
    except Exception as e:
        log.error(f"run_command: {str(e)}")
        result = {"command": command, "error": str(e)}
