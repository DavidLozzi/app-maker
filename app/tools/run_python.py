def run_python(code):
    try:
        exec(code)
        return "Code executed successfully."
    except Exception as e:
        return f"Error occurred: {str(e)}"
