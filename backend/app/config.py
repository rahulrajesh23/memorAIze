import os
import logging
from concurrent.futures import ThreadPoolExecutor

APP_ENV = os.getenv("APP_ENV", "DEV")

def setup_logger():
    logging.basicConfig(level=logging.INFO if APP_ENV == "DEV" else logging.WARNING)
    logger = logging.getLogger(__name__)
    return logger

# Initialize the logger
logger = setup_logger()


executor = ThreadPoolExecutor(max_workers=4)

