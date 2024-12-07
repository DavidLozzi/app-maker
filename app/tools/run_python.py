import logging
import os

log = logging.getLogger("app")


def run_python(source_path, tool):
    try:
        codes = tool["params"]
        outputs = ""
        for code in codes:
            outputs += f"Output for code: {code}\n"

            original_cwd = os.getcwd()
            os.chdir(source_path)
            outputs += exec(code)
            os.chdir(original_cwd)
        return {"action": tool, "output": outputs}
    except Exception as e:
        log.error(f"run_python: {str(e)}")
        return {"action": tool, "output": f"Error occurred: {str(e)}"}
