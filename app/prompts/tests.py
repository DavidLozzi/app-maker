from app.prompts.components import act_step_complete, init_prompt, init_user_prompt

reqs = """- Read the README and run unit tests
- Confirm coverage numbers are over 90%
- Confirm the tests are passing
- Fix any tests which are failing
"""

initial_prompt = init_prompt(reqs=reqs)
initial_user_prompt = init_user_prompt
action_step_complete = act_step_complete(reqs=reqs)


def get_prompts():
    return initial_prompt, initial_user_prompt, action_step_complete
