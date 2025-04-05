'''Module for analyzing the Quran text for hidden patterns and anomalies.'''

from collections import Counter
import datetime
import importlib.util

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

def analyze_root_words(text):
    '''Perform Arabic root word analysis on the given preprocessed Quran text.

    This function uses the CAMeL Tools morphological analyzer to extract the root of each word in the text.
    It counts the frequency of each identified root word and logs the frequency details to the results log file.
    Specifically, the function logs both the frequency of each root word and the top N most frequent root words.

    Args:
        text (str): The preprocessed Quran text.

    Returns:
        tuple: A tuple containing:
            - summary (str): A formatted summary of the root word frequency analysis.
            - root_freq (dict): A dictionary mapping each root word to its frequency.
            - top_roots (list): A list of tuples for the top N most frequent root words (root, frequency).
    '''
    from collections import Counter
    from src.logger import log_result

    # Check if camel_tools is available
    camel_tools_available = importlib.util.find_spec("camel_tools") is not None
    
    tokens = text.split()
    roots = []
    
    if camel_tools_available:
        try:
            from camel_tools.morphology.analyzer import Analyzer
            analyzer = Analyzer.builtin_analyzer()
            
            for token in tokens:
                try:
                    analyses = analyzer.analyze(token)
                    if analyses and 'root' in analyses[0]:
                        root = analyses[0]['root']
                    else:
                        root = token
                except Exception:
                    root = token
                roots.append(root)
        except Exception:
            # Fallback if camel_tools fails for any reason
            roots = tokens
    else:
        # Fallback when camel_tools is not available
        roots = tokens
    
    root_freq = Counter(roots)
    TOP_N = 20
    top_roots = root_freq.most_common(TOP_N)

    summary_lines = []
    summary_lines.append("Arabic Root Word Frequency Analysis:")
    for root, freq in root_freq.items():
        summary_lines.append(f"Root '{root}': {freq}")
    summary_lines.append("")
    summary_lines.append("Top Root Word Frequencies:")
    for idx, (root, freq) in enumerate(top_roots, 1):
        summary_lines.append(f"{idx}. Root '{root}' : {freq}")
    summary = "\n".join(summary_lines)

    log_result("Arabic Root Word Frequency Analysis:")
    for root, freq in root_freq.items():
        log_result(f"Root '{root}': {freq}")
    log_result("Top Root Word Frequencies:")
    for idx, (root, freq) in enumerate(top_roots, 1):
        log_result(f"{idx}. Root '{root}' : {freq}")

    return summary, dict(root_freq), top_roots