from src.tokenizer import tokenize_text
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

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
            db = MorphologyDB.builtin_db()
            analyzer = Analyzer(db)            
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

                tokens = tokenize_text(verse_text)
                roots = []
                lemmas = []
                try:            
                    for token in tokens:
                        try:
                            analyses = analyzer.analyze(token)
                            if analyses and 'root' in analyses[0]:
                                root = analyses[0]['root']
                            else:
                                root = token
                            if analyses and 'lex' in analyses[0]:
                                lemma = analyses[0]['lex']
                            else:
                                lemma = token                                
                        except Exception as e:
                            raise e
                        roots.append(root)
                        lemmas.append(lemma)
                except Exception as e:
                    raise e
            
                data.append({
                    "surah": surah,
                    "ayah": ayah,
                    "verse_text": verse_text,
                    "roots": roots,
                    "lemmas": lemmas
                })
        return data