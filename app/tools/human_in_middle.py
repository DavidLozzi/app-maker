import logging

log = logging.getLogger("app")


def human_in_middle(instructions):
    try:
        user_answers = []
        for instruction in instructions:
            print(instruction)
            answer = input("Did you complete the instruction? (Y/N): ")
            user_answers.append(
                f"Instruction: {instruction}\nThe user responded: {answer}"
            )
        log.info(
            f"Human in the middle instructions: {instructions}\nAnswers: {user_answers}"
        )
        return user_answers
    except Exception as e:
        log.error(f"human_in_middle: {str(e)}")
        return f"Instruction: {instruction} errored: {str(e)}"
