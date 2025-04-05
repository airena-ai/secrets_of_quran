"""
Module for searching words in the loaded Quran data.
"""

def search_word_in_quran(quran_data, search_word):
    """
    Search for a word in the Quran verses.

    This function iterates over the provided Quran data and checks if the search word is present
    in the verse text. The search is case-sensitive.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        search_word (str): The word to search for in the verse text.

    Returns:
        list: A list of dictionaries for verses containing the search word.
    """
    results = []
    for verse in quran_data:
        if search_word in verse.get('verse_text', ''):
            results.append(verse)
    return results