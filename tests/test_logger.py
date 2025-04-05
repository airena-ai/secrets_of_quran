'''Unit tests for the logger module.'''

import os
import unittest
from src import logger

class TestLogger(unittest.TestCase):
    def test_log_secret_found(self):
        '''Test that log_secret_found writes the correct log message.'''
        test_log_file = "tests/test_results.log"
        original_log_file = logger.LOG_FILE
        logger.LOG_FILE = test_log_file
        try:
            if os.path.exists(test_log_file):
                os.remove(test_log_file)
            test_message = "Test secret message"
            logger.log_secret_found(test_message)
            with open(test_log_file, 'r', encoding='utf-8') as f:
                log_contents = f.read()
            expected_log = f"POTENTIAL SECRET FOUND: {test_message}\n"
            self.assertEqual(log_contents, expected_log)
        finally:
            logger.LOG_FILE = original_log_file
            if os.path.exists(test_log_file):
                os.remove(test_log_file)

if __name__ == '__main__':
    unittest.main()