import unittest
from src.frequency_analyzer import (
    analyze_sentence_length_distribution,
    analyze_surah_sentence_length_distribution,
    analyze_ayah_sentence_length_distribution
)
from src.distribution_analyzer import (
    analyze_surah_sentence_length_distribution_by_index,
    analyze_ayah_sentence_length_distribution_by_index
)

class TestSentenceLengthDistribution(unittest.TestCase):
    '''Integration tests for sentence length distribution analysis functions.'''
    
    def test_analyze_sentence_length_distribution(self):
        self.maxDiff = None
        # Sample tokenized text: each inner list represents an ayah as a list of words.
        tokenized_text = [
            ["This", "is", "a", "test"],
            ["Another", "test"],
            ["One", "more", "test"],
            []
        ]
        # Expected distribution:
        # 4 words -> 1 ayah, 2 words -> 1 ayah, 3 words -> 1 ayah, 0 words -> 1 ayah.
        expected = {4: 1, 2: 1, 3: 1, 0: 1}
        result = analyze_sentence_length_distribution(tokenized_text)
        self.assertEqual(result, expected)
    
    def test_analyze_surah_sentence_length_distribution(self):
        self.maxDiff = None
        # Sample data for two surahs with processed_text.
        data = [
            {"surah": "Al-Fatiha", "processed_text": "In the name of God"},
            {"surah": "Al-Fatiha", "processed_text": "Praise be to God"},
            {"surah": "Al-Baqara", "processed_text": "This is a longer verse test"},
            {"surah": "Al-Baqara", "processed_text": ""}
        ]
        # For Al-Fatiha: first ayah has 5 words, second ayah has 4 words.
        # For Al-Baqara: first ayah has 6 words, second ayah has 0 words.
        expected = {
            "Al-Fatiha": {5: 1, 4: 1},
            "Al-Baqara": {6: 1, 0: 1}
        }
        result = analyze_surah_sentence_length_distribution(data)
        self.assertEqual(result, expected)
    
    def test_analyze_ayah_sentence_length_distribution(self):
        self.maxDiff = None
        # Sample data with surah and ayah identifiers.
        data = [
            {"surah": "Al-Fatiha", "ayah": "1", "processed_text": "In the name of God"},
            {"surah": "Al-Fatiha", "ayah": "2", "processed_text": "Praise be to God"},
            {"surah": "Al-Baqara", "ayah": "255", "processed_text": "Allah is the Light of the heavens and the earth"}
        ]
        # Expected:
        # "Al-Fatiha|1": {5: 1}, "Al-Fatiha|2": {4: 1},
        # "Al-Baqara|255": {10: 1}.
        expected = {
            "Al-Fatiha|1": {5: 1},
            "Al-Fatiha|2": {4: 1},
            "Al-Baqara|255": {10: 1}
        }
        result = analyze_ayah_sentence_length_distribution(data)
        self.assertEqual(result, expected)
    
    def test_analyze_surah_sentence_length_distribution_by_index(self):
        self.maxDiff = None
        # Sample data with surah_number and processed_text.
        data = [
            {"surah_number": "1", "processed_text": "First ayah of surah one"},
            {"surah_number": "1", "processed_text": "Second ayah"},
            {"surah_number": "2", "processed_text": "Single ayah of surah two"},
            {"surah_number": "2", "processed_text": ""}
        ]
        # For surah 1: "First ayah of surah one" -> 5 words, "Second ayah" -> 2 words.
        # For surah 2: "Single ayah of surah two" -> 5 words, "" -> 0 words.
        result = analyze_surah_sentence_length_distribution_by_index(data)
        expected = {
            1: {
                "frequency": {5: 1, 2: 1},
                "average": 3.5,
                "median": 3.5,
                "mode": [2, 5],
                "std_dev": 2.1213203435596424
            },
            2: {
                "frequency": {5: 1, 0: 1},
                "average": 2.5,
                "median": 2.5,
                "mode": [0, 5],
                "std_dev": 3.5355339059327378
            }
        }
        for surah in expected:
            self.assertEqual(result[surah]["frequency"], expected[surah]["frequency"])
            self.assertAlmostEqual(result[surah]["average"], expected[surah]["average"], places=2)
            self.assertAlmostEqual(result[surah]["median"], expected[surah]["median"], places=2)
            self.assertEqual(result[surah]["mode"], expected[surah]["mode"])
            self.assertAlmostEqual(result[surah]["std_dev"], expected[surah]["std_dev"], places=2)
    
    def test_analyze_ayah_sentence_length_distribution_by_index(self):
        self.maxDiff = None
        # Sample data with ayah and processed_text.
        data = [
            {"ayah": "1", "processed_text": "First ayah text here"},
            {"ayah": "1", "processed_text": "Another first ayah"},
            {"ayah": "2", "processed_text": "Second ayah longer text"},
            {"ayah": "2", "processed_text": ""}
        ]
        # For ayah index 1: "First ayah text here" -> 4 words, "Another first ayah" -> 3 words.
        # For ayah index 2: "Second ayah longer text" -> 4 words, "" -> 0 words.
        result = analyze_ayah_sentence_length_distribution_by_index(data)
        expected = {
            1: {
                "frequency": {4: 1, 3: 1},
                "average": 3.5,
                "median": 3.5,
                "mode": [3, 4],
                "std_dev": 0.7071067811865476
            },
            2: {
                "frequency": {4: 1, 0: 1},
                "average": 2.0,
                "median": 2.0,
                "mode": [0, 4],
                "std_dev": 2.8284271247461903
            }
        }
        for index in expected:
            self.assertEqual(result[index]["frequency"], expected[index]["frequency"])
            self.assertAlmostEqual(result[index]["average"], expected[index]["average"], places=2)
            self.assertAlmostEqual(result[index]["median"], expected[index]["median"], places=2)
            self.assertEqual(result[index]["mode"], expected[index]["mode"])
            self.assertAlmostEqual(result[index]["std_dev"], expected[index]["std_dev"], places=2)

if __name__ == "__main__":
    unittest.main()