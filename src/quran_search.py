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

def search_word_in_surah(word, surah_number, quran_data):
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

def search_word_group_in_surah(quran_data, word_group, surah_number, case_sensitive=False):
    """
    Search for a specific word group (phrase) within a given Surah of the Quran data.

    This function iterates over the provided Quran data, filtering verses to those that belong
    to the specified Surah (identified by surah_number). It then checks if the given word group,
    treated as an exact phrase, is present in the verse text using either case-sensitive or
    case-insensitive comparison based on the case_sensitive flag.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (exact phrase) to search for in the verse text.
        surah_number (int): The Surah number to filter verses.
        case_sensitive (bool): If True, performs case-sensitive search; otherwise, performs case-insensitive search.
                               Defaults to False.

    Returns:
        list: A list of dictionaries for verses that contain the specified word group within the given Surah.
    """
    results = []
    for verse in quran_data:
        try:
            verse_surah_number = int(verse.get('surah_number'))
        except (ValueError, TypeError):
            continue
        if verse_surah_number == surah_number:
            verse_text = verse.get('verse_text', '')
            if case_sensitive:
                if word_group in verse_text:
                    results.append(verse)
            else:
                if word_group.lower() in verse_text.lower():
                    results.append(verse)
    return results

def count_word_occurrences(quran_data, word):
    """
    Count the total number of occurrences of a word in the entire Quran text data.

    The search is performed in a case-insensitive manner by default, counting all occurrences
    of the specified word as a substring within each verse.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word (str): The word whose occurrences need to be counted.

    Returns:
        int: The total number of occurrences of the word in the Quran data.
    """
    if not word:
        return 0
    word_lower = word.lower()
    total_count = 0
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        total_count += verse_text.lower().count(word_lower)
    return total_count

def count_word_group_occurrences(quran_data, word_group):
    """
    Count the total number of occurrences of a word group (phrase) in the entire Quran text data.

    This function iterates over each verse in the provided Quran data and counts all non-overlapping
    occurrences of the specified word group, performing a case-insensitive search by default.
    If the word_group is an empty string, the function returns 0.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (phrase) to count occurrences of.

    Returns:
        int: The total number of occurrences of the word group in the Quran data.
    """
    if not word_group:
        return 0
    word_group_lower = word_group.lower()
    total_count = 0
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        total_count += verse_text.lower().count(word_group_lower)
    return total_count