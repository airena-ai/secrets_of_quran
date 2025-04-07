''' 
Module for Arabic lemmatization.
'''

try:
    from camel_tools.lemmatizer import Lemmatizer
    _lemmatizer_instance = Lemmatizer(model='calima-msa')
except Exception as e:
    _lemmatizer_instance = None

def lemmatize_token(token):
    '''
    Lemmatize the given Arabic token using CAMeL Tools.
    
    :param token: The Arabic word token.
    :return: The lemmatized form of the token.
    '''
    if _lemmatizer_instance is not None:
        try:
            lemma = _lemmatizer_instance.lemmatize(token)
            return lemma
        except Exception:
            return token
    return token