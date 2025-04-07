import os
import logging

def configure_logger():
    """
    Configure the root logger to write log messages to 'quran_analysis.log'
    in the project root directory.

    :return: Configured root logger.
    """
    logger = logging.getLogger()
    
    # Clear existing handlers to ensure we don't have multiple handlers
    # writing to the same or deleted log files
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    logger.setLevel(logging.INFO)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(project_root, "quran_analysis.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger