'''Module for logging analysis outputs of the Quran Secrets application.'''

import datetime

LOG_FILE = "results.log"

def log_secret_found(message):
    '''Log a secret finding to the results.log file with a special tag and a timestamp.

    The log message is prefixed with "POTENTIAL SECRET FOUND:" along with the current timestamp.

    Args:
        message (str): The secret message to log.
    '''
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{timestamp} - POTENTIAL SECRET FOUND: {message}\n")
    except Exception as e:
        print(f"Logging failed: {e}")

def log_result(message):
    '''Log a result message to the results.log file with a timestamp.

    Args:
        message (str): The result message to log.
    '''
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{timestamp} - RESULT: {message}\n")
    except Exception as e:
        print(f"Logging failed: {e}")

def log_bigram_frequencies(bigram_frequencies, top_n=20):
    '''Log the top N most frequent bigrams to the results log file.

    The function logs a header indicating the start of bigram analysis,
    followed by the top N bigrams and their frequency counts.

    Args:
        bigram_frequencies (dict): A dictionary mapping bigram tuples to frequency counts.
        top_n (int): The number of top bigrams to log.
    '''
    lines = []
    lines.append("--- Bigram Frequency Analysis ---")
    lines.append("Top {} Bigrams:".format(top_n))
    sorted_bigrams = sorted(bigram_frequencies.items(), key=lambda item: item[1], reverse=True)
    for idx, (bigram, count) in enumerate(sorted_bigrams[:top_n], start=1):
        lines.append("{}. {}: {}".format(idx, bigram, count))
    for line in lines:
        log_result(line)