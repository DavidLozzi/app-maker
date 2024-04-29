import logging

log = logging.getLogger("app")


def run_python(code):
    try:
        exec(code)
        return "Code executed successfully."
    except Exception as e:
        log.error(f"run_python: {str(e)}")
        return f"Error occurred: {str(e)}"
