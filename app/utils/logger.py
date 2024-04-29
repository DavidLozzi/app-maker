import logging
from datetime import datetime
import os


def setup_logger():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    log_file = f"./logs/log_{timestamp}.txt"
    error_log_file = f"./logs/error_log_{timestamp}.txt"

    logger = logging.getLogger("app")

    # Check if the logger already has handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    error_file_handler = logging.FileHandler(error_log_file)
    error_file_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(message)s")

    file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(console_handler)

    return logger
