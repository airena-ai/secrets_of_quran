'''Module for reading the Quran text from a file.'''

def read_quran_text(file_path):
    '''Read and return the text from the specified Quran file.

    Args:
        file_path (str): The path to the Quran text file.

    Returns:
        str: The content of the Quran text file.

    Raises:
        IOError: If the file cannot be read.
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Unable to read file {file_path}: {e}")