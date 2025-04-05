"""
Module for loading Quran data from a text file.
"""

def load_quran_text(file_path):
    """
    Load Quran text from a file.

    Reads the specified file and parses each line which should be in the format:
    surah_number|ayah_number|verse_text

    Args:
        file_path (str): Path to the Quran text file.

    Returns:
        list: A list of dictionaries. Each dictionary contains the keys 'surah_number', 'ayah_number',
              and 'verse_text' for a Quran verse.
    """
    quran_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|', 2)
                if len(parts) < 3:
                    continue
                surah_number, ayah_number, verse_text = parts
                verse = {
                    'surah_number': surah_number,
                    'ayah_number': ayah_number,
                    'verse_text': verse_text
                }
                quran_data.append(verse)
    except FileNotFoundError:
        print("Error: file not found -", file_path)
    return quran_data

def load_quran_data(file_path):
    """
    Load Quran data from a file by aliasing load_quran_text.

    This function is an alias to load_quran_text for backward compatibility and ease of use.
    
    Args:
        file_path (str): Path to the Quran text file.
    
    Returns:
        list: A list of dictionaries containing Quran verses.
    """
    return load_quran_text(file_path)