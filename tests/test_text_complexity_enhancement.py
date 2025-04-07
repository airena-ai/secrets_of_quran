import os
import unittest
from src.text_complexity_analyzer import (
    calculate_flesch_reading_ease,
    calculate_flesch_kincaid_grade_level,
    analyze_quran_flesch_reading_ease,
    analyze_quran_flesch_kincaid_grade_level,
    analyze_surah_flesch_reading_ease,
    analyze_surah_flesch_kincaid_grade_level,
    analyze_ayah_flesch_reading_ease,
    analyze_ayah_flesch_kincaid_grade_level
)

class TestFleschMetrics(unittest.TestCase):
    '''Unit tests for Flesch Reading Ease and Flesch-Kincaid Grade Level calculations.'''
    def test_calculate_flesch_reading_ease_empty(self):
        self.maxDiff = None
        # Test with empty text should return 0.0
        score = calculate_flesch_reading_ease("")
        self.assertEqual(score, 0.0)
        
    def test_calculate_flesch_kincaid_grade_level_empty(self):
        self.maxDiff = None
        grade = calculate_flesch_kincaid_grade_level("")
        self.assertEqual(grade, 0.0)
        
    def test_calculate_flesch_reading_ease_known(self):
        self.maxDiff = None
        # Using a simple sentence with known word and vowel counts.
        # Example: "I am." -> words: ["I", "am."]
        # Vowel counts: "I" has 1, "am." has 1 => total 2 syllables; total words =2; sentences =1
        # Score = 206.835 - 1.015*(2) - 84.6*(2/2)= 206.835 - 2.03 - 84.6 = 120.205
        text = "I am."
        score = calculate_flesch_reading_ease(text)
        self.assertAlmostEqual(score, 120.205, places=2)
        
    def test_calculate_flesch_kincaid_grade_level_known(self):
        self.maxDiff = None
        # Using the same text "I am.":
        # Grade = 0.39*(2) + 11.8*(2/2) - 15.59 = 0.78 + 11.8 - 15.59 = -2.01
        text = "I am."
        grade = calculate_flesch_kincaid_grade_level(text)
        self.assertAlmostEqual(grade, -2.01, places=2)

class TestFleschIntegrationAnalysis(unittest.TestCase):
    '''Integration tests for Quran, Surah, and Ayah level Flesch analyses.'''
    def test_integration_quran_level(self):
        self.maxDiff = None
        # Create a temporary test data file with sample verses.
        test_data = "1|1|I am happy.\n1|2|You are joyful."
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        test_file = os.path.join(data_dir, "quran-uthmani-min-test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_data)
        os.environ["DATA_FILE"] = test_file
        
        # Call the Quran level analysis functions.
        quran_reading_ease = analyze_quran_flesch_reading_ease()
        quran_grade = analyze_quran_flesch_kincaid_grade_level()
        
        # Assert that the results are numeric.
        self.assertIsInstance(quran_reading_ease, float)
        self.assertIsInstance(quran_grade, float)
        
        # Cleanup test file.
        os.remove(test_file)
        
    def test_integration_surah_and_ayah_level(self):
        self.maxDiff = None
        # Create a temporary test file with two Surahs and multiple Ayahs.
        test_data = (
            "1|1|I am happy.\n"
            "1|2|You are joyful.\n"
            "2|1|We are excited.\n"
            "2|2|They are content."
        )
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        test_file = os.path.join(data_dir, "quran-uthmani-min-test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_data)
        os.environ["DATA_FILE"] = test_file
        
        surah_reading = analyze_surah_flesch_reading_ease()
        surah_grade = analyze_surah_flesch_kincaid_grade_level()
        ayah_reading = analyze_ayah_flesch_reading_ease()
        ayah_grade = analyze_ayah_flesch_kincaid_grade_level()
        
        # Assert that results are dictionaries and contain expected keys.
        self.assertIsInstance(surah_reading, dict)
        self.assertIsInstance(surah_grade, dict)
        self.assertIsInstance(ayah_reading, dict)
        self.assertIsInstance(ayah_grade, dict)
        self.assertIn("1", surah_reading)
        self.assertIn("2", surah_reading)
        self.assertIn("1|1", ayah_reading)
        self.assertIn("2|2", ayah_grade)
        
        # Cleanup test file.
        os.remove(test_file)

if __name__ == "__main__":
    unittest.main()