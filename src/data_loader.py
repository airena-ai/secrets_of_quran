import os
import re
import logging

class QuranDataLoader:
    """
    A class to load and parse the Quran text data from a file.
    """

    def __init__(self, file_path=None):
        """
        Initialize the QuranDataLoader.

        :param file_path: Optional; path to the Quran text file.
                          If None, the default path is used.
        """
        if file_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.file_path = os.path.join(project_root, "data", "quran-uthmani-min.txt")
        else:
            self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    def load_data(self):
        """
        Load the Quran data from the text file.
        
        Parses each non-empty line of the file into surah, ayah,
        and verse_text based on the expected format "surah|ayah|verse_text".

        :return: A list of dictionaries with keys 'surah', 'ayah', and 'verse_text'.
        :raises FileNotFoundError: If the specified file does not exist.
        """
        self.logger.info("Starting data loading from %s", self.file_path)
        data = []
        # Expected format: surah|ayah|verse_text
        pattern = re.compile(r"^\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.+)$")
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    match = pattern.match(line)
                    if match:
                        surah, ayah, verse_text = match.groups()
                        data.append({
                            "surah": int(surah),
                            "ayah": int(ayah),
                            "verse_text": verse_text
                        })
                    else:
                        self.logger.warning("Line %d is not in expected format: %s", line_number, line)
        except FileNotFoundError as e:
            self.logger.error("File not found: %s", self.file_path)
            raise e
        self.logger.info("Completed data loading. Loaded %d verses.", len(data))
        return data