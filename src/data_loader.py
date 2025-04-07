import os
import logging

class QuranDataLoader:
    '''
    A class to load Quran data from a text file.
    '''
    def __init__(self, file_path=None):
        '''
        Initialize the QuranDataLoader.
        
        :param file_path: Path to the data file. If None, returns empty data.
        '''
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    def load_data(self):
        '''
        Load data from the specified file. Each line is expected to be in the format:
        surah|ayah|verse_text
        
        :return: A list of dictionaries with keys "surah", "ayah", and "verse_text".
        :raises: FileNotFoundError if the file_path is not provided or the file does not exist.
        '''
        if not self.file_path or not os.path.exists(self.file_path):
            self.logger.error("Data file not provided or does not exist.")
            raise FileNotFoundError("Data file not found")
            
        data = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    data.append({
                        "surah": int(parts[0]),
                        "ayah": int(parts[1]),
                        "verse_text": parts[2]
                    })
        self.logger.info("Completed data loading.")
        return data