import logging
import os
from src.logger_config import configure_logger
from src.data_loader import QuranDataLoader
from src.text_preprocessor import TextPreprocessor

def main():
    """
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
    12. Analyzes lemma word frequency across the Quran data.
    13. Analyzes lemma word co-occurrence across the Quran data.
    """
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
        
        # Surah-level word frequency analysis
        from src.frequency_analyzer import analyze_surah_word_frequency, analyze_ayah_word_frequency
        logger.info("Starting Surah-level word frequency analysis.")
        surah_frequencies = analyze_surah_word_frequency(data)
        logger.info("Surah-level word frequency analysis completed.")

        # Ayah-level word frequency analysis
        logger.info("Starting Ayah-level word frequency analysis.")
        ayah_frequencies = analyze_ayah_word_frequency(data)
        logger.info("Ayah-level word frequency analysis completed.")

        # Integrate surah-level root word frequency analysis
        from src.frequency_analyzer import analyze_surah_root_word_frequency
        logger.info("Starting surah-level root word frequency analysis.")
        surah_root_frequencies = analyze_surah_root_word_frequency(data)
        logger.info("Surah-level root word frequency analysis completed.")

        # Integrate ayah-level root word frequency analysis
        from src.frequency_analyzer import analyze_ayah_root_word_frequency
        logger.info("Starting Ayah-level Root Word Frequency Analysis.")
        ayah_root_frequencies = analyze_ayah_root_word_frequency(data)
        logger.info("Ayah-level Root Word Frequency Analysis completed.")

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
        
        logger.info("Application finished.")
    except Exception as e:
        logger.error(f"Error in application: {str(e)}")
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()