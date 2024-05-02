import subprocess
import logging

log = logging.getLogger("app")


def run_command(command, file_path):
    try:
        process = subprocess.Popen(
            " ".join(command),
            cwd=file_path,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
        )

        output = ""
        for line in iter(process.stdout.readline, b""):
            line = line.decode("utf-8").strip()
            print(line)  # print the line to the console
            output += line + "\n"

        process.communicate()  # wait for the process to finish

        result = {"command": command, "output": output.strip()}

        return result
    except subprocess.CalledProcessError as e:
        error = e.output.decode("utf-8").strip()
        result = {"command": command, "error": error}
        log.error(f"run_command CalledProcessError: {str(e)}")
        return result
    except Exception as e:
        log.error(f"run_command: {str(e)}")
        result = {"command": command, "error": str(e)}
        return result
