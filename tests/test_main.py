'''Integration test for the main module to execute end-to-end analysis.'''

import os
import unittest
from src import main

class TestMainIntegration(unittest.TestCase):
    def test_main_integration(self):
        '''Test the full execution of main() function end-to-end.'''
        data_dir = "data"
        file_path = os.path.join(data_dir, "quran-uthmani-min.txt")
        os.makedirs(data_dir, exist_ok=True)
        sample_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        log_file = "results.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        
        try:
            main.main()
            self.assertTrue(os.path.exists(log_file))
            with open(log_file, 'r', encoding='utf-8') as f:
                log_contents = f.read()
            self.assertIn("POTENTIAL SECRET FOUND:", log_contents)
            self.assertIn("Calculated numerical pattern: 42", log_contents)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(log_file):
                os.remove(log_file)
            try:
                os.rmdir(data_dir)
            except OSError:
                pass

if __name__ == '__main__':
    unittest.main()