from app.prompts.components import act_step_complete, init_prompt, init_user_prompt

reqs = """- Create documentation for a developer to get up to speed on this code repo.
- The documentation should be detailed and cover all aspects of the code
- You may include code snippets
  - If you identify complex code, provide explanations for the complex code
- If it's an API
  - Include all endpoints and request/response examples
  - Include a happy path scenario for the API, explaining each function and file a typical request would go through
    - I.e. the request would hit the router, then the controller, then the service, etc. naming each function and their params
- Keep the primary file in the root directory of the repo, named DEV_OVERVIEW.md
  - You may create multiple files if desired, ensure to link to them if you do
  - The documentation should be in markdown format
"""

initial_prompt = init_prompt(reqs=reqs)
initial_user_prompt = init_user_prompt
action_step_complete = act_step_complete(reqs=reqs)


def get_prompts():
    return initial_prompt, initial_user_prompt, action_step_complete
