'''Unit tests for the analyzer module.'''

import unittest
from unittest.mock import patch, MagicMock
from src.analyzer import analyze_text, analyze_word_frequency, analyze_root_words, analyze_bigrams
import importlib.util

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        
    def test_analyze_non_empty(self):
        '''Test that a non-empty text returns a simulated anomaly.'''
        text = "Some sample Quran text"
        anomalies = analyze_text(text)
        self.assertIsInstance(anomalies, list)
        self.assertGreater(len(anomalies), 0)
        self.assertIn("Calculated numerical pattern: 42", anomalies)

    def test_analyze_empty(self):
        '''Test that an empty text returns no anomalies.'''
        text = "   "
        anomalies = analyze_text(text)
        self.assertEqual(anomalies, [])
        
    def test_analyze_word_frequency_summary(self):
        '''Test that the word frequency analysis returns a proper summary and flagged list.'''
        text = "apple apple banana banana banana cherry"
        summary, flagged = analyze_word_frequency(text)
        self.assertIn("Word Frequency Analysis (Top 20):", summary)
        self.assertIn("1.", summary)
        self.assertIsInstance(flagged, list)
        
    def test_analyze_word_frequency_with_flags(self):
        '''Test that the word frequency analysis flags unusual word frequencies.'''
        text = ("wow " * 10) + ("meh " * 2)
        summary, flagged = analyze_word_frequency(text)
        self.assertIn("wow", summary)
        self.assertTrue(any("meh" in flag for flag in flagged))
        for flag in flagged:
            self.assertIn("frequency is", flag)
            
    def test_analyze_root_words_empty(self):
        '''Test Arabic root word analysis on empty text.'''
        # Mock importlib.util.find_spec to return None for camel_tools
        with patch('importlib.util.find_spec', return_value=None):
            summary, root_freq, top_roots = analyze_root_words("")
            self.assertIn("Arabic Root Word Frequency Analysis:", summary)
            self.assertEqual(root_freq, {})
            self.assertEqual(top_roots, [])
        
    def test_analyze_root_words_sample(self):
        '''Test Arabic root word analysis on sample text with mocked CAMeL Tools analyzer.'''
        # Create a mock for importlib.util.find_spec to return a non-None value
        mock_spec = MagicMock()
        
        # Mock the camel_tools module and its components
        mock_analyzer = MagicMock()
        mock_analyzer.analyze.side_effect = lambda token: [{'root': 'كتب'}] if token == "كتاب" else [{'root': 'درس'}] if token == "مدرسة" else [{'root': token}]
        
        mock_analyzer_class = MagicMock()
        mock_analyzer_class.builtin_analyzer.return_value = mock_analyzer
        
        # Apply the mocks
        with patch('importlib.util.find_spec', return_value=mock_spec), \
             patch.dict('sys.modules', {'camel_tools': MagicMock(), 
                                       'camel_tools.morphology': MagicMock(),
                                       'camel_tools.morphology.analyzer': MagicMock()}), \
             patch('camel_tools.morphology.analyzer.Analyzer', mock_analyzer_class):
            
            sample_text = "كتاب مدرسة كتاب"
            summary, root_freq, top_roots = analyze_root_words(sample_text)
            
            self.assertEqual(root_freq.get('كتب'), 2)
            self.assertEqual(root_freq.get('درس'), 1)
            self.assertIn("Root 'كتب': 2", summary)
            self.assertIn("Root 'درس': 1", summary)
            self.assertEqual(top_roots[0], ('كتب', 2))
            
    def test_analyze_bigrams_empty(self):
        '''Test that analyze_bigrams returns an empty dictionary when provided an empty tokenized text or insufficient tokens.'''
        self.assertEqual(analyze_bigrams([]), {})
        self.assertEqual(analyze_bigrams(["word"]), {})
        
    def test_analyze_bigrams_sample(self):
        '''Test analyze_bigrams with a sample tokenized text for correct bigram generation and frequency counting.'''
        tokens = ['a', 'b', 'a', 'b']
        # Expected bigrams: ('a', 'b'), ('b', 'a'), ('a', 'b')
        result = analyze_bigrams(tokens)
        expected = {('a', 'b'): 2, ('b', 'a'): 1}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()