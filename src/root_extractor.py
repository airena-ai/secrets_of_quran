''' 
Module for Arabic root word extraction.
'''

try:
    from camel_tools.morphology.analyzer import Analyzer
    _analyzer_instance = Analyzer.predefined('calima-msa')
except Exception as e:
    _analyzer_instance = None

def extract_root(token):
    '''
    Extract the root of the given Arabic token using CAMeL Tools morphological analysis.
    
    :param token: The Arabic word token.
    :return: The extracted root form of the token.
    '''
    if _analyzer_instance is not None:
        try:
            analyses = _analyzer_instance.analyze(token)
            if analyses and isinstance(analyses, list) and len(analyses) > 0:
                return analyses[0].get('root', token)
        except Exception:
            return token
    return token