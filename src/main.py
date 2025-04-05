"""
Main entry point for the Quran search application.
"""

from src.quran_data_loader import load_quran_text
from src.quran_search import search_word_in_quran

def main():
    """
    Main function to load Quran data and search for a specific word.

    Loads the Quran text from the file and performs a search for the word 'اللَّهِ'.
    The search results are then printed to the console.
    """
    quran_file_path = 'data/quran-uthmani-min.txt'
    quran_data = load_quran_text(quran_file_path)
    search_word = 'اللَّهِ'
    results = search_word_in_quran(quran_data, search_word)
    
    print("Search results for word '{}':".format(search_word))
    for verse in results:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))

if __name__ == '__main__':
    main()