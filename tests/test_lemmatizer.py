import unittest
from unittest.mock import MagicMock, patch
from src.lemmatizer import lemmatize_token

class TestLemmatizer(unittest.TestCase):
    '''
    Unit tests for the Arabic lemmatizer.
    '''

    @patch('src.lemmatizer._lemmatizer_instance')
    def test_lemmatize_token(self, mock_lemmatizer_instance):
        self.maxDiff = None
        mock_lemmatizer_instance.lemmatize = MagicMock(side_effect=lambda token: token + "_lem")
        token = "كلمة"
        expected = "كلمة_lem"
        result = lemmatize_token(token)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()