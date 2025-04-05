'''Unit tests for the analyzer module.'''

import unittest
from src.analyzer import analyze_text, analyze_word_frequency

class TestAnalyzer(unittest.TestCase):
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
        # Create a text where one word appears significantly less than another.
        text = ("wow " * 10) + ("meh " * 2)
        summary, flagged = analyze_word_frequency(text)
        self.assertIn("wow", summary)
        # Expect at least one flagged message (e.g., for 'meh')
        self.assertTrue(any("meh" in flag for flag in flagged))
        for flag in flagged:
            self.assertIn("frequency is", flag)

if __name__ == '__main__':
    unittest.main()