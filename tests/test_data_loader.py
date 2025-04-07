import os
import tempfile
import unittest
from src.data_loader import QuranDataLoader

class TestQuranDataLoader(unittest.TestCase):
    """
    Unit tests for the QuranDataLoader class.
    """

    def test_load_data_success(self):
        self.maxDiff = None
        sample_data = "1|1|Test verse one\n1|2|Test verse two\n"
        # Create a temporary file with sample data
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as tmp_file:
            tmp_file.write(sample_data)
            temp_path = tmp_file.name
        try:
            loader = QuranDataLoader(file_path=temp_path)
            result = loader.load_data()
            expected = [
                {"surah": 1, "ayah": 1, "verse_text": "Test verse one"},
                {"surah": 1, "ayah": 2, "verse_text": "Test verse two"}
            ]
            self.assertEqual(result, expected)
        finally:
            os.remove(temp_path)

    def test_load_data_file_not_found(self):
        self.maxDiff = None
        loader = QuranDataLoader(file_path="non_existent_file.txt")
        with self.assertRaises(FileNotFoundError):
            loader.load_data()

if __name__ == "__main__":
    unittest.main()