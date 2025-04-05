'''Module for analyzing the Quran text for hidden patterns and anomalies.'''

from collections import Counter
import datetime

def analyze_text(text):
    '''Analyze the given text for hidden numerical patterns and anomalies.

    This function simulates pattern detection. If the text is non-empty,
    a simulated anomaly is detected and returned.

    Args:
        text (str): The preprocessed text of the Quran.

    Returns:
        list: A list of anomaly messages detected in the text.
    '''
    anomalies = []
    if text.strip():
        # Simulated detection of a hidden pattern
        anomalies.append("Calculated numerical pattern: 42")
    return anomalies

def analyze_word_frequency(text):
    '''Perform word frequency analysis on the given preprocessed Quran text.

    This function tokenizes the text using whitespace, counts the occurrences of each unique word,
    and determines the top N most frequent words. It prepares a summary of the word frequency analysis
    and identifies any words whose frequency is unusually high or low based on a simple heuristic.

    The heuristic flags a word if its frequency is more than twice the average frequency of the top words
    (and greater than 1), or if the frequency is less than half the average (provided the average is greater than 1).

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        tuple: A tuple containing:
            - summary (str): A formatted multiline string listing the top N words and their counts.
            - flagged (list): A list of flagged messages for words deemed unusual.
    '''
    # Tokenize the text by whitespace
    tokens = text.split()
    counter = Counter(tokens)
    TOP_N = 20
    top_words = counter.most_common(TOP_N)
    
    lines = ["Word Frequency Analysis (Top {}):".format(TOP_N)]
    for idx, (word, freq) in enumerate(top_words, start=1):
        lines.append("{}. '{}' : {}".format(idx, word, freq))
    summary = "\n".join(lines)
    
    flagged = []
    if top_words:
        avg_freq = sum(freq for _, freq in top_words) / len(top_words)
        for word, freq in top_words:
            if freq > 2 * avg_freq and freq > 1:
                flagged.append("Word '{}' frequency is {}".format(word, freq))
            elif avg_freq > 1 and freq < (avg_freq / 2):
                flagged.append("Word '{}' frequency is {}".format(word, freq))
    
    return summary, flagged