"""
Main entry point for the Quran search application.
"""

from src.quran_data_loader import load_quran_text
from src.quran_search import search_word_in_quran, search_word_group_in_surah

def main():
    """
    Main function to load Quran data and perform search operations.
    
    Loads the Quran text from the file and performs a search for a specific word and a word group.
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
    
    # Demonstration of new search_word_group_in_surah function
    word_group = "الرحمن الرحيم"
    results_group = search_word_group_in_surah(quran_data, word_group, surah_number=1)
    
    print("\nSearch results for word group '{}':".format(word_group))
    for verse in results_group:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))

if __name__ == '__main__':
    main()