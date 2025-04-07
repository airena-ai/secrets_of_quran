class QuranDataLoader:
    '''
    A class to load Quran data from a text file.
    
    The text file is expected to have each line in the format:
    surah|ayah|verse_text
    '''
    def __init__(self, file_path=None):
        '''
        Initialize the data loader.
        
        :param file_path: Path to the Quran data file. If None, defaults to a predefined path.
        '''
        self.file_path = file_path

    def load_data(self):
        '''
        Load and parse the Quran data file.
        
        :return: List of dictionaries representing each verse with keys 'surah', 'ayah', 'verse_text', and 'roots'.
        '''
        data = []
        if not self.file_path:
            raise ValueError("No data file specified.")
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) < 3:
                    continue
                surah = int(parts[0])
                ayah = int(parts[1])
                verse_text = parts[2]
                data.append({
                    "surah": surah,
                    "ayah": ayah,
                    "verse_text": verse_text,
                    "roots": []
                })
        return data