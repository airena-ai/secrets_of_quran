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
    """
    logger = configure_logger()
    logger.info("Application started.")

    try:
        # Read file path from environment variable; if not set, defaults to None
        file_path = os.getenv("DATA_FILE")
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
        
        # Integrate word frequency analysis
        from src.frequency_analyzer import count_word_frequencies
        logger.info("Starting word frequency analysis.")
        word_frequencies = count_word_frequencies(tokenized_text)
        unique_words_count = len(word_frequencies)
        logger.info("Total unique words: %d", unique_words_count)
        top_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:50]
        logger.info("Top 50 most frequent words:")
        for word, count in top_words:
            logger.info("Word: %s, Count: %d", word, count)
        logger.info("Word frequency analysis completed.")

        # Integrate word co-occurrence analysis
        from src.cooccurrence_analyzer import analyze_word_cooccurrence
        logger.info("Starting word co-occurrence analysis.")
        cooccurrence_freq = analyze_word_cooccurrence(data)
        logger.info("Co-occurrence analysis returned %d unique word pairs.", len(cooccurrence_freq))
        logger.info("Word co-occurrence analysis output: %s", cooccurrence_freq)

        logger.info("Application finished.")
    except Exception as e:
        logger.error(f"Error in application: {str(e)}")
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()