"""
Main entry point for the Quran search application.
"""

from src.quran_data_loader import load_quran_text, load_quran_data
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
    
    # Demonstration of search_word_group_in_surah function
    word_group = "الرحمن الرحيم"
    results_group = search_word_group_in_surah(quran_data, word_group, surah_number=1)
    
    print("\nSearch results for word group '{}':".format(word_group))
    for verse in results_group:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
    
    # Demonstration of count_word_group_occurrences function
    total_count = count_word_group_occurrences(quran_data, word_group)
    print("\nTotal occurrences of phrase '{}': {}".format(word_group, total_count))
    
    # Demonstration of search_word_in_verse_range function
    from src.quran_search import search_word_in_verse_range
    verse_range_start = (1, 1)
    verse_range_end = (1, 5)
    results_range = search_word_in_verse_range(quran_data, "اللَّهِ", verse_range_start, verse_range_end)
    
    print("\nSearch results for word 'اللَّهِ' in verse range {} to {}:".format(verse_range_start, verse_range_end))
    for verse in results_range:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
        
    # Demonstration of search_word_group_in_verse_range function
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
        
    # Demonstration of search_verses_by_word_count function
    from src.quran_search import search_verses_by_word_count
    specific_count = 19
    results_word_count = search_verses_by_word_count(quran_data, specific_count)
    print("\nSearch results for verses with exactly {} words:".format(specific_count))
    for verse in results_word_count:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
    
    # Demonstration of calculate_gematrical_value function
    from src.quran_search import calculate_gematrical_value
    gem_value = calculate_gematrical_value("بسم الله الرحمن الرحيم")
    print("\nGematrical value for 'بسم الله الرحمن الرحيم':", gem_value)
    
    # Demonstration of search_words_by_gematrical_value function
    from src.quran_search import search_words_by_gematrical_value
    target_gem_value = 66  # Gematrical value for 'الله'
    results_gem = search_words_by_gematrical_value(quran_data, target_gem_value)
    print("\nSearch results for words with gematrical value {}:".format(target_gem_value))
    for entry in results_gem:
        print("Surah: {} Ayah: {} - Word: {}".format(
            entry.get('surah_number'), entry.get('ayah_number'), entry.get('word')
        ))
        
    # Demonstration of search_word_groups_by_gematrical_value function (New Feature)
    from src.quran_search import search_word_groups_by_gematrical_value
    phrase = "الرحمن الرحيم"
    target_phrase_gem_value = 618  # Gematrical value for 'الرحمن الرحيم'
    results_phrase_gem = search_word_groups_by_gematrical_value(quran_data, phrase, target_phrase_gem_value)
    print("\nSearch results for word group '{}' with gematrical value {}:".format(phrase, target_phrase_gem_value))
    for verse in results_phrase_gem:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
    
    # Demonstration of search_verses_by_word_gematrical_value_equals_word_count function (New Feature)
    from src.quran_search import search_verses_by_word_gematrical_value_equals_word_count
    target_word_group = "بسم الله"
    results_gem_word_count = search_verses_by_word_gematrical_value_equals_word_count(quran_data, target_word_group)
    print("\nSearch results for verses where word count equals gematrical value of word group '{}':".format(target_word_group))
    for verse in results_gem_word_count:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
    
    # Demonstration of search_verses_by_word_group_gematrical_value_equals_verse_number function (New Feature)
    from src.quran_search import search_verses_by_word_group_gematrical_value_equals_verse_number
    word_group_target = "ب"
    results_group_verse = search_verses_by_word_group_gematrical_value_equals_verse_number(quran_data, word_group_target)
    print("\nSearch results for verses where the gematrical value of word group '{}' equals the verse number:".format(word_group_target))
    for verse in results_group_verse:
        print("Surah: {} Ayah: {} - {}".format(
            verse.get('surah_number'), verse.get('ayah_number'), verse.get('verse_text')
        ))
        
if __name__ == '__main__':
    main()