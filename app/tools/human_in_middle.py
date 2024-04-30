import logging

log = logging.getLogger("app")


def human_in_middle(instructions):
    try:
        user_answers = []
        for instruction in instructions:
            print(f"\n{instruction}")
            answer = input(
                "\nDid you complete the instruction? (Yes / No / Paste Output):"
            )
            user_answers.append(
                f"Instruction: {instruction}\nThe user responded: {answer}"
            )
        log.debug(
            f"Human in the middle instructions: {instructions}\nAnswers: {user_answers}"
        )
        return user_answers
    except Exception as e:
        log.error(f"human_in_middle: {str(e)}")
        return f"Instruction: {instruction} errored: {str(e)}"
