'''Module for loading data files for the Quran Secrets application.'''

import os
import json

def load_muqattaat_interpretations():
    '''Load and return the scholarly interpretations of Muqatta'at from the JSON file.

    Returns:
        dict: A dictionary containing interpretations with keys as interpretation IDs.
    '''
    file_path = os.path.join("data", "muqattaat_interpretations.json")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)