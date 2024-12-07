from app.prompts.components import act_step_complete, init_prompt, init_user_prompt

reqs = """- Follow best practices for software development.
- Request contents of files, starting with the entry file, and review each one.
  - Ignore unit tests.
- Identify performance risks, memory leaks, and other detrimental coding practices.
- Identify messy code, code that is hard to read, and code that is hard to maintain.
  - Feel free to create new files to keep files small.
- Make changes to the code to improve the identified problems.
  - Provide the entire modified file in your response
  - Add a comment above your change to explain why this change improves the code.
- Review as many files as you want at once, but only modify one file at a time."""

initial_prompt = init_prompt(reqs=reqs)
initial_user_prompt = init_user_prompt
action_step_complete = act_step_complete(reqs=reqs)


def get_prompts():
    return initial_prompt, initial_user_prompt, action_step_complete