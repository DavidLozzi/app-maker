from app.prompts.components import act_step_complete, init_prompt, init_user_prompt


class TestPrompts:
    def __init__(self):
        reqs = """- Read the README and run unit tests
        - Confirm coverage numbers are over 90%
        - Confirm the tests are passing
        - Fix any tests which are failing
        """
        self.initial_prompt = init_prompt(reqs=reqs)
        self.initial_user_prompt = init_user_prompt
        self.action_step_complete = act_step_complete(reqs=reqs)

    def get_prompts(self):
        return self.initial_prompt, self.initial_user_prompt, self.action_step_complete
