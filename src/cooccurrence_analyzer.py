import logging
from src.tokenizer import tokenize_text

def analyze_word_cooccurrence(quran_data):
    '''
    Analyze word co-occurrence within each ayah of the Quran data.
    
    Each ayah's processed text is tokenized into words, and all unique word pairs 
    that co-occur within the same ayah are counted. Word pairs are stored in alphabetical 
    order to ensure consistency.
    
    :param quran_data: List of dictionaries. Each dictionary should contain 'surah', 'ayah',
                       and either 'processed_text' (preferred) or 'verse_text'.
    :return: Dictionary with keys as tuples (word1, word2) and values as co-occurrence counts.
    '''
    logger = logging.getLogger(__name__)
    pair_counts = {}
    
    for item in quran_data:
        # Use 'processed_text' if available; otherwise fall back to 'verse_text'
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split() if text else []
        if len(tokens) < 2:
            continue
        for i in range(len(tokens) - 1):
            for j in range(i + 1, len(tokens)):
                pair = tuple(sorted((tokens[i], tokens[j])))
                if pair in pair_counts:
                    pair_counts[pair] += 1
                else:
                    pair_counts[pair] = 1
                    
    sorted_pairs = sorted(pair_counts.items(), key=lambda item: item[1], reverse=True)
    top_20 = sorted_pairs[:20]
    logger.info("Word Co-occurrence Analysis Results")
    for pair, count in top_20:
        logger.info("Pair: %s, Count: %d", str(pair), count)
    logger.info("Total unique word pairs: %d", len(pair_counts))
    return pair_counts