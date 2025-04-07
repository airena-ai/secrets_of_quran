import logging
import os

def configure_logger():
    '''
    Configure and return a logger that logs messages to both console and a log file.

    The log file is named 'quran_analysis.log' and is located in the project root.

    :return: Configured logger instance.
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "quran_analysis.log")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger