"""
Module for searching words in the loaded Quran data.
"""

ABJAD_VALUES = {
    'ا': 1,
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5,
    'و': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    'ي': 10,
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000
}

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

def search_word_in_verse_range(quran_data, word: str, start_verse: tuple[int, int], end_verse: tuple[int, int], case_sensitive: bool = False) -> list[dict]:
    """
    Searches for a word within a specified verse range in the Quran.

    This function searches the provided quran_data list for verses within the given range
    (inclusive) that contain the specified word. The search is performed in a case-sensitive or
    case-insensitive manner based on the case_sensitive flag.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word (str): The word to search for.
        start_verse (tuple[int, int]): The starting verse of the range as (surah_number, ayah_number).
        end_verse (tuple[int, int]): The ending verse of the range as (surah_number, ayah_number).
        case_sensitive (bool, optional): Whether the search is case-sensitive. Defaults to False.

    Returns:
        list[dict]: A list of dictionaries, each containing verse details where the word is found within the specified range.
    """
    results = []
    for verse in quran_data:
        try:
            surah_num = int(verse.get('surah_number'))
            ayah_num = int(verse.get('ayah_number'))
        except (ValueError, TypeError):
            continue
        current_verse = (surah_num, ayah_num)
        if current_verse < start_verse or current_verse > end_verse:
            continue
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word in verse_text:
                results.append(verse)
        else:
            if word.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_word_group_in_verse_range(quran_data, word_group: str, start_verse: tuple[int, int], end_verse: tuple[int, int], case_sensitive: bool = False) -> list[dict]:
    """
    Searches for a word group within a specified verse range in the Quran.

    This function searches the provided quran_data for verses within the given range
    (inclusive) that contain the specified word group. The search is performed in a case-sensitive or
    case-insensitive manner based on the case_sensitive flag.

    Args:
        quran_data (list): List of dictionaries representing Quran data.
        word_group (str): The word group (phrase) to search for.
        start_verse (tuple[int, int]): The starting verse of the range as (surah_number, ayah_number).
        end_verse (tuple[int, int]): The ending verse of the range as (surah_number, ayah_number).
        case_sensitive (bool, optional): Whether the search is case-sensitive. Defaults to False.

    Returns:
        list[dict]: A list of dictionaries, each containing verse details where the word group is found within the specified range.
    """
    results = []
    for verse in quran_data:
        try:
            surah_num = int(verse.get('surah_number'))
            ayah_num = int(verse.get('ayah_number'))
        except (ValueError, TypeError):
            continue
        current_verse = (surah_num, ayah_num)
        if current_verse < start_verse or current_verse > end_verse:
            continue
        verse_text = verse.get('verse_text', '')
        if case_sensitive:
            if word_group in verse_text:
                results.append(verse)
        else:
            if word_group.lower() in verse_text.lower():
                results.append(verse)
    return results

def search_verses_by_word_count(quran_data, word_count):
    """
    Search Quran verses that contain exactly the specified number of words.

    Iterates over the provided quran_data, splitting each verse's verse_text into words, and collects
    verses where the number of words is exactly equal to word_count.

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        word_count (int): The desired number of words in a verse.

    Returns:
        list: A list of dictionaries, each containing a verse with exactly word_count words.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        if len(words) == word_count:
            results.append(verse)
    return results

def search_verses_by_word_count_multiple(quran_data, multiple_of):
    """
    Search for Quran verses where the number of words is a multiple of a specified number.

    Iterates over the provided quran_data, splitting each verse's verse_text into words, 
    and collects verses where the number of words is an exact multiple of multiple_of.

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        multiple_of (int): The integer multiple to check against. Must be a non-zero integer.

    Returns:
        list: A list of dictionaries, each containing a verse where the word count is a multiple of multiple_of.

    Raises:
        ValueError: If multiple_of is zero.
    """
    if multiple_of == 0:
        raise ValueError("multiple_of must be non-zero")
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        if len(words) % multiple_of == 0:
            results.append(verse)
    return results

def calculate_gematrical_value(text: str) -> int:
    """
    Calculate the gematrical (Abjad) value of a given Arabic word or phrase.

    This function computes the sum of the numerical values of the Arabic letters in the input
    text based on the standard Abjad numeral mapping. Characters not present in the mapping are ignored.

    Args:
        text (str): An Arabic word or phrase.

    Returns:
        int: The gematrical value calculated by summing the Abjad numeral values of characters in the text.
    """
    total = 0
    for char in text:
        total += ABJAD_VALUES.get(char, 0)
    return total

def search_words_by_gematrical_value(quran_data, target_value: int) -> list:
    """
    Search for words in the Quran that have the specified gematrical value.

    This function iterates over each verse in the provided Quran data. It splits the verse text into individual words,
    calculates the gematrical value of each word using the calculate_gematrical_value function,
    and returns a list of dictionaries for words that match the specified target gematrical value.
    Each dictionary contains the matching word and its location (surah and ayah numbers).

    Args:
        quran_data (list): List of dictionaries representing Quran verses.
        target_value (int): The target gematrical value to match.

    Returns:
        list: A list of dictionaries. Each dictionary has the keys 'word', 'surah_number', and 'ayah_number' for each matching word.
    """
    results = []
    for verse in quran_data:
        verse_text = verse.get('verse_text', '')
        words = verse_text.split()
        for word in words:
            if calculate_gematrical_value(word) == target_value:
                results.append({
                    'word': word,
                    'surah_number': verse.get('surah_number'),
                    'ayah_number': verse.get('ayah_number')
                })
    return results