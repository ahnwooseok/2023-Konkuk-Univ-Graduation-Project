import logging
import logging.handlers

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
timedfilehandler = logging.handlers.TimedRotatingFileHandler(
    filename="log", when="midnight", interval=1, encoding="utf-8"
)
timedfilehandler.setFormatter(formatter)
timedfilehandler.suffix = "%Y-%m-%d"

logger.addHandler(timedfilehandler)
