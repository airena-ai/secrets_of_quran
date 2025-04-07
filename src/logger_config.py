import logging
import os

def configure_logger():
    '''
    Configure and return a logger for the Quran analysis application.
    
    The logger writes logs to a file named 'quran_analysis.log' in the current working directory.
    Log messages are formatted in a structured JSON-like format for machine-parseability and human readability.
    
    :return: Configured logger instance.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_file = os.path.join(os.getcwd(), "quran_analysis.log")
        file_handler = logging.FileHandler(log_file, mode='w', encoding="utf-8")
        formatter = logging.Formatter('{"timestamp": "%(asctime)s.%(msecs)03d", "level": "%(levelname)s", "message": "%(message)s"}', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger