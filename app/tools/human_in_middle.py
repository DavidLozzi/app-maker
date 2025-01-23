import logging

log = logging.getLogger("app")


def human_in_middle(tool):
    try:
        user_answers = []
        instructions = tool["params"]
        for instruction in instructions:
            print(f"\n{instruction}")
            answer = input(
                "\nDid you complete the instruction? (Respond with any message or paste an output):"
            )
            user_answers.append(
                f"Instruction: {instruction}\nThe user responded: {answer}"
            )
        log.debug(
            f"Human in the middle instructions: {instructions}\nAnswers: {user_answers}"
        )
        return {"action": tool, "output": user_answers}
    except Exception as e:
        log.error(f"human_in_middle: {str(e)}")
        return {
            "action": tool,
            "output": f"Error with Instruction: {instruction}: {str(e)}",
        }
