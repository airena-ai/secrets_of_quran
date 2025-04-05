'''Unit tests for the analyzer module.'''

import unittest
from src.analyzer import analyze_text

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

if __name__ == '__main__':
    unittest.main()