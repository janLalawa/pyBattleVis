import logging
from modules.config.constants import Paths


def setup_logging():
    """
    Configures the global logging settings for the application.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        handlers=[
                            logging.FileHandler(Paths.LOG_PATH),
                            logging.StreamHandler()
                        ])
    logger = logging.getLogger(__name__)
    return logger
