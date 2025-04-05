"""
Module for searching words in the loaded Quran data.
"""

def search_word_in_quran(quran_data, search_word, case_sensitive=False):
    """
    Search for a word in the Quran verses.

    This function iterates over the provided Quran data and checks if the search word is present
    in the verse text. The search can be performed in a case-sensitive or case-insensitive manner.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        search_word (str): The word to search for in the verse text.
        case_sensitive (bool): If True, performs case-sensitive search; otherwise, performs case-insensitive search.
                               Defaults to False.

    Returns:
        list: A list of dictionaries for verses containing the search word.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if search_word in verse_text:
                results.append(verse)
        else:
            if search_word.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_group(quran_data, word_group, case_sensitive=False):
    """
    Search for a specific word group (phrase) in the Quran verses.

    This function iterates over the provided Quran data and checks if the given word group, treated
    as an exact phrase, is present in the verse text. The search can be performed in a case-sensitive
    or case-insensitive manner while maintaining the word order.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (exact phrase) to search for in the verse text.
        case_sensitive (bool): If True, performs case-sensitive search; otherwise, performs case-insensitive search.
                               Defaults to False.

    Returns:
        list: A list of dictionaries representing verses that contain the specified word group.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word_group in verse_text:
                results.append(verse)
        else:
            if word_group.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_in_surah(word: str, surah_number: int, quran_data: list) -> list:
    """
    Searches for a word within a specific Surah in the Quran data.

    Args:
        word (str): The word to search for (case-insensitive).
        surah_number (int): The Surah number to search within.
        quran_data (list[dict]): The loaded Quran data.

    Returns:
        list[dict]: A list of verses (dictionaries) where the word is found in the specified Surah.
    """
    results = []
    for verse in quran_data:
        try:
            verse_surah_number = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if verse_surah_number == surah_number:
            verse_text = verse.get('verse_text', '')
            if word.lower() in verse_text.lower():
                results.append(verse)
    return results