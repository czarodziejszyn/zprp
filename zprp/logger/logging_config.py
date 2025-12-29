import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s | %(name)s | %(message)s",
)

# quiet some logs of httpx library 
logging.getLogger("httpx").setLevel(logging.WARNING)