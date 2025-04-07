import re

def tokenize_text(text):
    """
    Tokenize the Arabic text into individual words using whitespace and punctuation as delimiters.
    
    :param text: The input normalized Arabic text.
    :return: A list of word tokens.
    """
    # Split on whitespace and common punctuation (including Arabic punctuation)
    tokens = re.split(r"[ \t\n\r\.,;:!?،؟()\"'\-]+", text)
    # Filter out any empty tokens
    tokens = [token for token in tokens if token]
    return tokens