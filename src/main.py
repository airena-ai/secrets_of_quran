"""
Main entry point for the Quran search application.
"""

from src.quran_data_loader import load_quran_text
from src.quran_search import search_word_in_quran, search_word_group_in_surah, count_word_group_occurrences

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
    
    # Demonstration of new count_word_group_occurrences function
    total_count = count_word_group_occurrences(quran_data, word_group)
    print("\nTotal occurrences of phrase '{}': {}".format(word_group, total_count))
    
    # Demonstration of new search_word_in_verse_range function
    from src.quran_search import search_word_in_verse_range
    verse_range_start = (1, 1)
    verse_range_end = (1, 5)
    results_range = search_word_in_verse_range(quran_data, "اللَّهِ", verse_range_start, verse_range_end)
    
    print("\nSearch results for word 'اللَّهِ' in verse range {} to {}:".format(verse_range_start, verse_range_end))
    for verse in results_range:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
        
    # Demonstration of new search_word_group_in_verse_range function
    from src.quran_search import search_word_group_in_verse_range
    verse_range_group_start = (1, 1)
    verse_range_group_end = (1, 5)
    group_phrase = "بسم الله"
    results_group_range = search_word_group_in_verse_range(quran_data, group_phrase, verse_range_group_start, verse_range_group_end)
    
    print("\nSearch results for word group '{}' in verse range {} to {}:".format(group_phrase, verse_range_group_start, verse_range_group_end))
    for verse in results_group_range:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))

if __name__ == '__main__':
    main()