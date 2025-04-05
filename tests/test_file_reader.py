'''Unit tests for the file_reader module.'''

import os
import unittest
from src.file_reader import read_quran_text

class TestFileReader(unittest.TestCase):
    def test_read_existing_file(self):
        '''Test reading an existing file returns correct content.'''
        test_file = "tests/test_quran.txt"
        sample_text = "Test Quran content."
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        try:
            result = read_quran_text(test_file)
            self.assertEqual(result, sample_text)
        finally:
            os.remove(test_file)

    def test_read_non_existing_file(self):
        '''Test reading a non-existing file raises an IOError.'''
        with self.assertRaises(IOError):
            read_quran_text("non_existing_file.txt")

if __name__ == '__main__':
    unittest.main()