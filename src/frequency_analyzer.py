from collections import Counter

def count_word_frequencies(tokenized_text):
    """
    Calculate the frequency of each unique word across the tokenized Quran text.
    
    The input is a list of lists of words, where each inner list represents a verse.
    The output is a dictionary with unique words as keys and their frequency counts as values.
    
    :param tokenized_text: List of lists of word tokens.
    :return: Dictionary of word frequencies.
    """
    counter = Counter()
    for verse_tokens in tokenized_text:
        counter.update(verse_tokens)
    return dict(counter)