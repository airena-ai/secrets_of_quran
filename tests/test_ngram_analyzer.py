import unittest
from collections import Counter
from src.ngram_analyzer import analyze_character_ngrams, analyze_surah_character_ngrams, analyze_ayah_character_ngrams

class TestCharacterNGrams(unittest.TestCase):
    def test_analyze_character_ngrams_n2(self):
        self.maxDiff = None
        # Sample data: one ayah with processed_text "abab"
        sample_data = [
            {"surah": 1, "ayah": 1, "processed_text": "abab"}
        ]
        # "abab" with n=2: "ab", "ba", "ab" -> Counter({'ab': 2, 'ba': 1})
        result = analyze_character_ngrams(sample_data, n=2)
        expected = Counter({'ab': 2, 'ba': 1})
        self.assertEqual(dict(result), dict(expected))
        
    def test_analyze_character_ngrams_n3(self):
        self.maxDiff = None
        sample_data = [
            {"surah": 1, "ayah": 1, "processed_text": "abcabc"}
        ]
        # "abcabc" with n=3: "abc", "bca", "cab", "abc" -> Counter({'abc': 2, 'bca': 1, 'cab': 1})
        result = analyze_character_ngrams(sample_data, n=3)
        expected = Counter({'abc': 2, 'bca': 1, 'cab': 1})
        self.assertEqual(dict(result), dict(expected))

    def test_analyze_surah_character_ngrams(self):
        self.maxDiff = None
        sample_data = [
            {"surah": 1, "ayah": 1, "processed_text": "abcd"},
            {"surah": 1, "ayah": 2, "processed_text": "bcda"},
            {"surah": 2, "ayah": 1, "processed_text": "xyz"}
        ]
        # For surah 1, concatenated text = "abcd" + "bcda" = "abcdbcda"
        # n=2 bigrams on "abcdbcda": "ab", "bc", "cd", "db", "bc", "cd", "da"
        # Frequency: {'ab':1, 'bc':2, 'cd':2, 'db':1, 'da':1}
        # For surah 2, text = "xyz": bigrams: "xy", "yz"
        result = analyze_surah_character_ngrams(sample_data, n=2)
        expected = {
            1: Counter({'ab': 1, 'bc': 2, 'cd': 2, 'db': 1, 'da': 1}),
            2: Counter({'xy': 1, 'yz': 1})
        }
        self.assertEqual({k: dict(v) for k, v in result.items()}, {k: dict(v) for k, v in expected.items()})
    
    def test_analyze_ayah_character_ngrams(self):
        self.maxDiff = None
        sample_data = [
            {"surah": 1, "ayah": 1, "processed_text": "ababa"},
            {"surah": 1, "ayah": 2, "processed_text": "babab"}
        ]
        # For first ayah "ababa" with n=2: bigrams: "ab", "ba", "ab", "ba" -> Counter({'ab': 2, 'ba': 2})
        # For second ayah "babab" with n=2: bigrams: "ba", "ab", "ba", "ab" -> Counter({'ba': 2, 'ab': 2})
        result = analyze_ayah_character_ngrams(sample_data, n=2)
        expected = {
            "1|1": Counter({'ab': 2, 'ba': 2}),
            "1|2": Counter({'ba': 2, 'ab': 2})
        }
        self.assertEqual({k: dict(v) for k, v in result.items()}, {k: dict(v) for k, v in expected.items()})

if __name__ == '__main__':
    unittest.main()