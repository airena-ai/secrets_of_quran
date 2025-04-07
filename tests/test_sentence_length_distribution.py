import unittest
from src.frequency_analyzer import (
    analyze_sentence_length_distribution,
    analyze_surah_sentence_length_distribution,
    analyze_ayah_sentence_length_distribution
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
        # "Al-Fatiha|1": 5 words, "Al-Fatiha|2": 4 words,
        # "Al-Baqara|255": 10 words.
        expected = {
            "Al-Fatiha|1": 5,
            "Al-Fatiha|2": 4,
            "Al-Baqara|255": 10
        }
        result = analyze_ayah_sentence_length_distribution(data)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()