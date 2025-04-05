'''Module for preprocessing and normalizing Arabic text.'''

import re

def remove_diacritics(text):
    '''Remove Arabic diacritics from the given text.

    Args:
        text (str): The original Arabic text.

    Returns:
        str: The text with diacritics removed.
    '''
    arabic_diacritics = re.compile(r'[\u064B-\u0652]')
    return re.sub(arabic_diacritics, '', text)

def normalize_arabic_letters(text):
    '''Normalize specific Arabic letters in the given text.

    This function normalizes:
        - The Arabic letter 'ى' (U+0649) to 'ي' (U+064A) only when it appears as a standalone word
        - The Arabic letter 'ة' (U+0629) to 'ه' (U+0647) at the end of words

    Args:
        text (str): The text to normalize.

    Returns:
        str: The normalized text.
    '''
    # Replace standalone ى (U+0649) with ي (U+064A)
    text = re.sub(r'\b\u0649\b', '\u064A', text)
    
    # Replace ة (U+0629) at the end of words with ه (U+0647)
    text = re.sub(r'(\u0629)+\b', '\u0647', text)
    
    return text