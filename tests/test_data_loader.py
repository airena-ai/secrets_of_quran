import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from src.data_loader import QuranDataLoader

class TestQuranDataLoader(unittest.TestCase):
    """
    Unit tests for the QuranDataLoader class.
    """
    
    def setUp(self):
        self.maxDiff = None
        # Create a temporary file with test data
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.temp_file.write("1|1|بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n")
        self.temp_file.write("1|2|الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\n")
        self.temp_file.close()
    
    def tearDown(self):
        # Clean up the temporary file
        os.unlink(self.temp_file.name)
    
    def test_load_data_file_not_found(self):
        """
        Test that load_data raises FileNotFoundError when the file doesn't exist.
        """
        loader = QuranDataLoader(file_path="nonexistent_file.txt")
        with self.assertRaises(FileNotFoundError):
            loader.load_data()
    
    def test_load_data_success(self):
        """
        Test that load_data correctly parses the file and returns the expected data.
        """
        loader = QuranDataLoader(file_path=self.temp_file.name)
        data = loader.load_data()
        
        # Verify that the data is loaded correctly
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["surah"], 1)
        self.assertEqual(data[0]["ayah"], 1)
        self.assertEqual(data[0]["verse_text"], "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
        self.assertEqual(data[1]["surah"], 1)
        self.assertEqual(data[1]["ayah"], 2)
        self.assertEqual(data[1]["verse_text"], "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ")

if __name__ == "__main__":
    unittest.main()