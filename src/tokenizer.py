import re

def tokenize_text(text):
    # Split on punctuation (Arabic and English) or whitespace:
    #  - [.,،!\s] covers periods, commas, Arabic comma, exclamation marks, and whitespace.
    #  - The + quantifier makes sure we group consecutive punctuation/whitespace as one split.
    tokens = re.split(r'[.,،!\s]+', text)
    
    # Filter out any empty tokens (which may appear if text starts/ends with punctuation)
    tokens = [token for token in tokens if token]
    return tokens