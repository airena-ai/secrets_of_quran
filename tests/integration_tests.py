import os
import unittest
import re
from collections import Counter
from src.comparative_analyzer import (
    compare_makki_madani_text_complexity,
    compare_makki_madani_word_frequency_distribution,
    compare_makki_madani_gematria_distribution
)
from src.data_loader import QuranDataLoader

class TestComparativeAnalyzer(unittest.TestCase):
    """
    Integration tests for the comparative analysis functions.
    Each test sets up a temporary Quran data file with sample verses and validates
    that the comparative analysis functions compute and log the expected outputs.
    """
    def test_compare_text_complexity(self):
        self.maxDiff = None
        # Create sample data with two verses:
        # Verse from surah 1 (Makki) and surah 2 (Madani)
        sample_data = "1|1|كلمة واحدة\n2|1|كلمة اثنتان\n"
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        test_file = os.path.join(data_dir, "quran_test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(sample_data)
        
        os.environ["DATA_FILE"] = test_file
        
        # Define Makki and Madani surah lists for the test
        makki_surahs = [1]
        madani_surahs = [2]
        
        # Run comparative text complexity analysis
        result = compare_makki_madani_text_complexity(makki_surahs, madani_surahs)
        # Check that result is a dict with keys Makki and Madani and that metric values are floats.
        self.assertIn("Makki", result)
        self.assertIn("Madani", result)
        for group in result:
            for metric, value in result[group].items():
                self.assertIsInstance(value, float)
        
        os.remove(test_file)
    
    def test_compare_word_frequency_distribution(self):
        self.maxDiff = None
        # Create sample data with distinct words for Makki and Madani verses.
        sample_data = "1|1|سلام سلام\n2|1|حياة نجاح\n"
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        test_file = os.path.join(data_dir, "quran_test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(sample_data)
        
        os.environ["DATA_FILE"] = test_file
        
        makki_surahs = [1]
        madani_surahs = [2]
        
        result = compare_makki_madani_word_frequency_distribution(makki_surahs, madani_surahs, top_n=2)
        self.assertIn("Makki", result)
        self.assertIn("Madani", result)
        # Check that the top frequency lists are non-empty lists.
        self.assertIsInstance(result["Makki"], list)
        self.assertIsInstance(result["Madani"], list)
        self.assertGreater(len(result["Makki"]), 0)
        self.assertGreater(len(result["Madani"]), 0)
        
        os.remove(test_file)
    
    def test_compare_gematria_distribution(self):
        self.maxDiff = None
        # Create sample data where words have predictable gematria values.
        # Using the default gematria mapping from gematria_analyzer, values for each character.
        sample_data = "1|1|اب\n2|1|تث\n"
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        test_file = os.path.join(data_dir, "quran_test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(sample_data)
        
        os.environ["DATA_FILE"] = test_file
        
        makki_surahs = [1]
        madani_surahs = [2]
        
        result = compare_makki_madani_gematria_distribution(makki_surahs, madani_surahs, top_n=2)
        self.assertIn("Makki", result)
        self.assertIn("Madani", result)
        self.assertIsInstance(result["Makki"], list)
        self.assertIsInstance(result["Madani"], list)
        # The gematria distribution should be a list of tuples (value, frequency)
        for tup in result["Makki"]:
            self.assertEqual(len(tup), 2)
        for tup in result["Madani"]:
            self.assertEqual(len(tup), 2)
        
        os.remove(test_file)

if __name__ == "__main__":
    unittest.main()