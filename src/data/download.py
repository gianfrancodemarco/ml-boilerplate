import logging
import logging.config
import os

from src import utils
from src.data.misc import fetch_or_resume

logging.config.fileConfig(os.path.join(utils.SRC_PATH, "logging.conf"))

DESTINATION_PATH = os.path.join(utils.DATA_PATH, "raw", "card_database.sqlite")
DATA_URL = os.getenv("CARD_DATABASE_URL", "https://mtgjson.com/api/v5/AllPrintings.sqlite")

fetch_or_resume(DATA_URL, DESTINATION_PATH)