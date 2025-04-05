'''Unit tests for the logger module.'''

import unittest
import os
from unittest.mock import patch, mock_open
from src.logger import log_secret_found, log_result

class TestLogger(unittest.TestCase):
    '''Test cases for the logger module.'''
    
    def setUp(self):
        '''Set up test environment.'''
        self.maxDiff = None
    
    @patch('src.logger.open', new_callable=mock_open)
    @patch('src.logger.datetime')
    def test_log_secret_found(self, mock_datetime, mock_file):
        '''Test that log_secret_found writes the correct message to the log file.'''
        # Mock the datetime to return a fixed value
        mock_datetime.datetime.now.return_value.strftime.return_value = "2025-04-05 00:43:48"
        
        # Call the function
        log_secret_found("Test secret message")
        
        # Get the contents that were written to the mocked file
        log_contents = mock_file().write.call_args[0][0]
        
        # Assert that the log contains the expected message
        self.assertIn("POTENTIAL SECRET FOUND: Test secret message", log_contents)
    
    @patch('src.logger.open', new_callable=mock_open)
    @patch('src.logger.datetime')
    def test_log_result(self, mock_datetime, mock_file):
        '''Test that log_result writes the correct message to the log file.'''
        # Mock the datetime to return a fixed value
        mock_datetime.datetime.now.return_value.strftime.return_value = "2025-04-05 00:43:48"
        
        # Call the function
        log_result("Test result message")
        
        # Get the contents that were written to the mocked file
        log_contents = mock_file().write.call_args[0][0]
        
        # Assert that the log contains the expected message
        expected_log = "2025-04-05 00:43:48 - RESULT: Test result message\n"
        self.assertEqual(log_contents, expected_log)