import logging
import os

def configure_logger():
    '''
    Configure and return a logger for the Quran analysis application.
    
    The logger writes logs to a file named 'quran_analysis.log' in the current working directory.
    
    :return: Configured logger instance.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_file = os.path.join(os.getcwd(), "quran_analysis.log")
        file_handler = logging.FileHandler(log_file, mode='w', encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger