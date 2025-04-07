import unittest
from unittest.mock import MagicMock, patch
from src.root_extractor import extract_root

class TestRootExtractor(unittest.TestCase):
    '''
    Unit tests for the Arabic root extraction.
    '''

    @patch('src.root_extractor._analyzer_instance')
    def test_extract_root(self, mock_analyzer_instance):
        self.maxDiff = None
        mock_analyzer_instance.analyze = MagicMock(return_value=[{'root': 'كتب'}])
        token = "كتابة"
        expected = "كتب"
        result = extract_root(token)
        self.assertEqual(result, expected)

    @patch('src.root_extractor._analyzer_instance')
    def test_extract_root_no_analysis(self, mock_analyzer_instance):
        self.maxDiff = None
        mock_analyzer_instance.analyze = MagicMock(return_value=[])
        token = "غير_معروف"
        expected = "غير_معروف"
        result = extract_root(token)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()