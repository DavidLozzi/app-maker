def system_message(content):
    return {"role": "system", "content": content}


def user_message(content):
    return {"role": "user", "content": content}


def assistant_message(content):
    return {"role": "assistant", "content": content}
