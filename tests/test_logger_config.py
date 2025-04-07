import os
import logging
import unittest
from src.logger_config import configure_logger

class TestLoggerConfig(unittest.TestCase):
    """
    Unit tests for the logger configuration.
    """

    def test_configure_logger_creates_log_file(self):
        self.maxDiff = None
        # Backup current handlers and clear them for testing
        root_logger = logging.getLogger("quran_analysis")
        original_handlers = root_logger.handlers[:]
        root_logger.handlers = []
        logger = configure_logger()
        file_handler = None
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                file_handler = handler
                break
        self.assertIsNotNone(file_handler, "FileHandler not found in logger handlers.")
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        expected_log_file = os.path.join(project_root, "quran_analysis.log")
        self.assertEqual(os.path.abspath(file_handler.baseFilename), os.path.abspath(expected_log_file))
        # Restore original handlers
        root_logger.handlers = original_handlers

if __name__ == "__main__":
    unittest.main()