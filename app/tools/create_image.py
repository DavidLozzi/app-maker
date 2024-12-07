import os
import logging
from app.gpt import call_gpt_4o
from app.messages import user_message

log = logging.getLogger("app")


# TODO finish off image creation
async def create_image(file_path, tool):
    relative_path = tool["params"][0]
    image_desc = tool["params"][1]
    try:
        response = await call_gpt_4o(
            [
                user_message(
                    f"Create an image using the following description:\n{image_desc}"
                )
            ]
        )
        print(response)
        file_full_path = os.path.join(file_path, relative_path.replace("./", ""))
        os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        # with open(file_full_path, "w") as file:
        #     file.write(file_contents)
        # return {"action": tool, "output": f"File '{file_name}' created successfully."}
    except Exception as e:
        error = f"Error creating file '{relative_path}': {str(e)}"
        log.error(f"create_file: {error}")
        return {"action": tool, "error": error}
