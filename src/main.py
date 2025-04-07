import logging
import os
from src.logger_config import configure_logger
from src.data_loader import QuranDataLoader
from src.text_preprocessor import TextPreprocessor

def main():
    """
    Main function to orchestrate data loading and text preprocessing.
    """
    logger = configure_logger()
    logger.info("Application started.")
    
    # Read file path from environment variable; if not set, defaults to None
    file_path = os.getenv("DATA_FILE")
    loader = QuranDataLoader(file_path=file_path)
    data = loader.load_data()
    
    # Preprocess each verse text
    processor = TextPreprocessor()
    for item in data:
        original_text = item.get("verse_text", "")
        processed_text = processor.preprocess_text(original_text)
        item["processed_text"] = processed_text

    logger.info("Application finished.")

    # Ensure FileHandler is closed
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        if isinstance(handler, logging.FileHandler):
            handler.close()
            root_logger.removeHandler(handler)


if __name__ == "__main__":
    main()