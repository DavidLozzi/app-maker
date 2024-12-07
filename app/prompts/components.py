import json
from app.models.output import OutputModel

tools = """The GPTs have access to various tools. These tools are run within Python, as noted. Use these tools appropriately based on the task requirements:
- `get_file_contents(file_path)`: Retrieves the file and returns the contents of the specified file.
- `create_file(file_path, contents)`: Creates the file at the specified path and writes the contents into it.
- `run_python(code)`: Executes Python code and returns the results using Python's `exec`.
- `run_command(command)`: Use this to execute automated CLI commands that do not require human decision-making during their execution. \
This command will always be run in the same directory, use approprite paths in the command. This command is run using Python's `subprocess`.
- `human_in_middle(instructions)`: Use this only for CLI commands that require human interaction or decision making during execution. The user \
will run the commands you provide in a separate terminal. The instructions should include what command to run and what you would like them to \
return to you upon completion of the command.
- `clear_previous()`: Use this to clear the memory of previous attempts, if needed.
- 'create_image(path, description)': Use this to create an image at the specified relative path, including filename. The description will be used by GPT to create the image.

## Tools Exceptions
- Do not provide any `git` commands or instructions, the user will commit and push when they decide to.
- Use human_in_middle() for any interactive commands: `amplify ...`, `aws ...`, `npm init...` etc.
- The user already has aws, amplify, git, npm, nodejs, and python installed and configured"""

output = f"""- Provide a list of actions to accomplish your goal.
- Your output will be a single JSON as defined: {json.dumps(OutputModel.model_json_schema())}"""


def init_prompt(reqs):
    return f"""# Your Tasks
- Review the FOLDERS structure
- Review the README file
- Review the Your Requirements
- Review Your Tools and provide any action or actions you wish to take
- Review Your Output

# Your Inputs
- FOLDERS: The folder path and structure of the code
- README: The README.md file for the code which should provide details about the code.
- NOTES: Any notes or comments from the user about the code

# Your Requirements
{reqs}

# Your Tools
{tools}

# Your Output
{output}"""


init_user_prompt = """FOLDERS:
*****
{folder_struct}
*****

README:
*****
{readme}
*****"""


def act_step_complete(reqs):
    return f"""
# Your Tasks
- Review the FOLDERS structure
- Review the README file
- Review Your Requirements
- Review Your Tools
- Review PREVIOUS for actions already taken and their outputs
- Determine if the PREVIOUS actions and their outputs are adequate to achieve \
Your Goal and meet the Requirements
  - If not, provide any additional actions to achieve Your Goal and meet the Requirements
  - Do not repeat actions unless you are retrying or want to see if a file has changed
  - If you are done, make sure to use an action, follow Your Output, to create your final outputs
- Review Your Output

# Your Inputs
- FOLDERS: The folder path and structure of the code
- README: The README.md file for the code which should provide details about the code.
- NOTES: Any notes or comments from the user about the code
- PREVIOUS: Any previous actions taken and their resulting output.

# Your Requirements
{reqs}

# Your Tools
{tools}

# Your Output
{output}"""
