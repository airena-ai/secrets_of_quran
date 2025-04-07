import logging
import os
from src.logger_config import configure_logger
from src.data_loader import QuranDataLoader
from src.text_preprocessor import TextPreprocessor

def main():
    '''
    Main function to orchestrate data loading, text preprocessing, and word frequency analysis.
    
    This function performs the following steps:
    1. Loads Quran data.
    2. Preprocesses each verse (normalization, tokenization, lemmatization, root extraction).
    3. Collects the tokenized text (each verse as a list of words).
    4. Computes word frequency analysis on the tokenized text.
    5. Logs the total unique word count and the top 50 most frequent words.
    6. Computes word co-occurrence analysis, logs the top 20 most frequent co-occurring word pairs 
       and the total number of unique word pairs.
    7. Analyzes word frequencies at Surah and Ayah levels, logging top frequent words per analysis.
    8. Analyzes word length distribution within the tokenized text and logs summary statistics.
    9. Analyzes root word frequency across the Quran data and logs the top 20 root words and unique count.
    10. Analyzes root word co-occurrence within each Ayah of the Quran data, logging the top 20 most frequent pairs.
    11. Analyzes ayah-level root word frequency, logging top 5 root words and unique count per ayah.
    12. Analyzes surah-level root word frequency, logging top 10 root words and unique count per surah.
    13. Analyzes lemma word frequency across the Quran data.
    14. Analyzes lemma word co-occurrence across the Quran data.
    15. Analyzes word n-gram frequency at Quran, Surah, and Ayah levels.
    16. Analyzes character n-gram frequency at Quran, Surah, and Ayah levels.
    17. Analyzes word collocation, logging the top 20 collocation pairs and total unique collocation pairs.
    '''
    logger = configure_logger()
    logger.info("Application started.")

    try:
        # Read file path from environment variable; if not set, defaults to "quran-uthmani-min.txt"
        file_path = os.getenv("DATA_FILE")
        if file_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")            

        loader = QuranDataLoader(file_path=file_path)
        data = loader.load_data()

        # Preprocess each verse text and collect tokenized output for frequency analysis
        processor = TextPreprocessor()
        tokenized_text = []
        for item in data:
            original_text = item.get("verse_text", "")
            processed_text = processor.preprocess_text(original_text)
            item["processed_text"] = processed_text
            # Create token list from the processed text (tokens are separated by space)
            tokens = processed_text.split()
            tokenized_text.append(tokens)
        
        # Integrate Surah-level and Ayah-level Character Frequency Analysis
        from src.frequency_analyzer import analyze_surah_character_frequency, analyze_ayah_character_frequency
        logger.info("Starting Surah-level Character Frequency Analysis.")
        surah_char_freq = analyze_surah_character_frequency(data)
        logger.info("Surah-level Character Frequency Analysis completed.")
        
        logger.info("Starting Ayah-level Character Frequency Analysis.")
        ayah_char_freq = analyze_ayah_character_frequency(data)
        logger.info("Ayah-level Character Frequency Analysis completed.")

        # Integrate character frequency analysis
        from src.frequency_analyzer import analyze_character_frequency, analyze_word_length_distribution
        analyze_character_frequency(tokenized_text)

        # Integrate word length distribution analysis
        logger.info("Starting word length distribution analysis.")
        word_length_distribution = analyze_word_length_distribution(tokenized_text)
        logger.info("Word length distribution analysis completed.")

        # Integrate word frequency analysis
        from src.frequency_analyzer import count_word_frequencies
        logger.info("Starting word frequency analysis.")
        word_frequencies = count_word_frequencies(tokenized_text)
        unique_words_count = len(word_frequencies)
        logger.info("Total unique words: %d", unique_words_count)
        top_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:2000]
        logger.info("Top 2000 most frequent words:")
        for word, count in top_words:
            logger.info("Word: %s, Count: %d", word, count)
        logger.info("Word frequency analysis completed.")

        # Integrate word co-occurrence analysis
        from src.cooccurrence_analyzer import analyze_word_cooccurrence
        logger.info("Starting word co-occurrence analysis.")
        cooccurrence_freq = analyze_word_cooccurrence(data)
        logger.info("Co-occurrence analysis returned %d unique word pairs.", len(cooccurrence_freq))
        
        # Integrate word collocation analysis
        from src.collocation_analyzer import analyze_word_collocation
        logger.info("Starting Word Collocation Analysis.")
        collocation_freq = analyze_word_collocation(data, window_size=3)
        logger.info("Word Collocation Analysis completed. Total unique collocation pairs: %d", len(collocation_freq))

        # Surah-level word frequency analysis
        from src.frequency_analyzer import analyze_surah_word_frequency, analyze_ayah_word_frequency
        logger.info("Starting Surah-level word frequency analysis.")
        surah_frequencies = analyze_surah_word_frequency(data)
        logger.info("Surah-level word frequency analysis completed.")

        # Ayah-level word frequency analysis
        logger.info("Starting Ayah-level word frequency analysis.")
        ayah_frequencies = analyze_ayah_word_frequency(data)
        logger.info("Ayah-level word frequency analysis completed.")

        # Integrate ayah-level root word frequency analysis
        from src.frequency_analyzer import analyze_ayah_root_word_frequency
        logger.info("Starting Ayah-level Root Word Frequency Analysis.")
        ayah_root_frequencies = analyze_ayah_root_word_frequency(data)
        logger.info("Ayah-level Root Word Frequency Analysis completed.")
        
        # Integrate surah-level root word frequency analysis
        from src.frequency_analyzer import analyze_surah_root_word_frequency
        logger.info("Starting surah-level root word frequency analysis.")
        surah_root_frequencies = analyze_surah_root_word_frequency(data)
        logger.info("Surah-level Root Word Frequency Analysis completed.")
        
        # New: Integrate first and last root word frequency analysis at Ayah level
        from src.frequency_analyzer import analyze_ayah_first_root_word_frequency, analyze_ayah_last_root_word_frequency
        logger.info("Starting Ayah First Root Word Frequency Analysis.")
        first_root_freq = analyze_ayah_first_root_word_frequency(data)
        logger.info("Ayah First Root Word Frequency Analysis completed.")
        logger.info("Starting Ayah Last Root Word Frequency Analysis.")
        last_root_freq = analyze_ayah_last_root_word_frequency(data)
        logger.info("Ayah Last Root Word Frequency Analysis completed.")
        
        # Integrate semantic group frequency analysis using root words
        from src.frequency_analyzer import analyze_semantic_group_frequency
        logger.info("Starting Semantic Group Frequency Analysis.")
        semantic_group_freq = analyze_semantic_group_frequency(data)
        logger.info("Semantic Group Frequency Analysis completed.")
        
        # Integrate root word frequency analysis
        from src.frequency_analyzer import analyze_root_word_frequency
        logger.info("Starting root word frequency analysis.")
        root_frequencies = analyze_root_word_frequency(data)
        logger.info("Root word frequency analysis completed.")

        # Integrate root word co-occurrence analysis
        from src.cooccurrence_analyzer import analyze_root_word_cooccurrence
        logger.info("Starting Root Word Co-occurrence Analysis...")
        analyze_root_word_cooccurrence(data)
        logger.info("Root Word Co-occurrence Analysis Completed.\n")

        # Integrate lemma word frequency analysis
        from src.frequency_analyzer import analyze_lemma_word_frequency
        logger.info("Starting lemma word frequency analysis.")
        root_frequencies = analyze_lemma_word_frequency(data)
        logger.info("Lemma word frequency analysis completed.")

        # Integrate lemma word co-occurrence analysis
        from src.cooccurrence_analyzer import analyze_lemma_word_cooccurrence
        logger.info("Starting Lemma Word Co-occurrence Analysis...")
        analyze_lemma_word_cooccurrence(data)
        logger.info("Lemma Word Co-occurrence Analysis Completed.\n")
        
        # Integrate word n-gram analysis (bigram analysis at Quran level)
        from src.ngram_analyzer import analyze_word_ngrams, analyze_surah_word_ngrams, analyze_ayah_word_ngrams
        logger.info("Starting word n-gram analysis.")
        ngram_freq = analyze_word_ngrams(tokenized_text, n=2)
        logger.info("Word n-gram analysis completed.")
        
        # Integrate Surah-level word n-gram analysis
        logger.info("Starting Surah-level word n-gram analysis.")
        surah_ngram_freq = analyze_surah_word_ngrams(data, n=2)
        logger.info("Surah-level word n-gram analysis completed.")
        
        # Integrate Ayah-level word n-gram analysis
        logger.info("Starting Ayah-level word n-gram analysis.")
        ayah_ngram_freq = analyze_ayah_word_ngrams(data, n=2)
        logger.info("Ayah-level word n-gram analysis completed.")

        # Integrate Character N-gram Analysis
        from src.ngram_analyzer import analyze_character_ngrams, analyze_surah_character_ngrams, analyze_ayah_character_ngrams
        logger.info("Starting Character N-gram Analysis at Quran level.")
        char_ngram_freq = analyze_character_ngrams(data, n=2)
        logger.info("Character N-gram Analysis at Quran level completed.")
        
        logger.info("Starting Character N-gram Analysis at Surah level.")
        surah_char_ngram_freq = analyze_surah_character_ngrams(data, n=2)
        logger.info("Character N-gram Analysis at Surah level completed.")
        
        logger.info("Starting Character N-gram Analysis at Ayah level.")
        ayah_char_ngram_freq = analyze_ayah_character_ngrams(data, n=2)
        logger.info("Character N-gram Analysis at Ayah level completed.")

        logger.info("Application finished.")
    except Exception as e:
        logger.error(f"Error in application: {str(e)}")
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()