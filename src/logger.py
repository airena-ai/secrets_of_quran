'''Module for logging analysis outputs of the Quran Secrets application.'''

LOG_FILE = "results.log"

def log_secret_found(message):
    '''Log a secret finding to the results.log file with a special tag.

    The log message is prefixed with "POTENTIAL SECRET FOUND:".

    Args:
        message (str): The secret message to log.
    '''
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"POTENTIAL SECRET FOUND: {message}\n")
    except Exception as e:
        print(f"Logging failed: {e}")