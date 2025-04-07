import logging
import numpy as np
from src.gematria_analyzer import calculate_gematria_value

def analyze_sentence_length_gematria_correlation(quran_data):
    '''
    Analyze the correlation between sentence length (number of words per ayah) and the average Gematria value of words.
    
    For each ayah in the provided Quran data (list of dictionaries), the function:
      - Retrieves the processed text (using "processed_text" if available, otherwise "verse_text").
      - Tokenizes the text into words.
      - Computes the sentence length.
      - Calculates the Gematria value for each word using calculate_gematria_value.
      - Computes the average Gematria value for that ayah.
    
    The function then groups the results by sentence length and computes the average of average Gematria values per sentence length.
    Additionally, it computes the Pearson correlation coefficient between sentence lengths and the average Gematria values
    across all ayahs.
    
    Logs a structured table of results and summary statistics including:
      - Each sentence length, the count of ayahs, and the average of average Gematria values.
      - The computed correlation coefficient.
    
    :param quran_data: List of dictionaries representing preprocessed Quran data.
    :return: Dictionary with keys:
             "group_averages": mapping sentence length to a dictionary {"average_gematria": value, "count": count},
             "correlation_coefficient": computed Pearson correlation coefficient.
    '''
    logger = logging.getLogger("quran_analysis")
    sentence_results = []
    lengths = []
    avg_gematria_values = []
    
    for item in quran_data:
        text = item.get("processed_text") or item.get("verse_text", "")
        tokens = text.split()
        if not tokens:
            continue
        sentence_length = len(tokens)
        gematria_vals = [calculate_gematria_value(token) for token in tokens]
        average_gematria = sum(gematria_vals) / sentence_length if sentence_length > 0 else 0
        lengths.append(sentence_length)
        avg_gematria_values.append(average_gematria)
        sentence_results.append((sentence_length, average_gematria))
    
    group_dict = {}
    for length, avg_val in sentence_results:
        if length not in group_dict:
            group_dict[length] = {"total": 0, "count": 0}
        group_dict[length]["total"] += avg_val
        group_dict[length]["count"] += 1
    
    group_averages = {}
    for length, data in group_dict.items():
        avg_of_avg = data["total"] / data["count"] if data["count"] > 0 else 0
        group_averages[length] = {"average_gematria": avg_of_avg, "count": data["count"]}
    
    correlation_coefficient = None
    if len(lengths) > 1:
        correlation_matrix = np.corrcoef(lengths, avg_gematria_values)
        correlation_coefficient = correlation_matrix[0, 1]
    
    logger.info("Sentence Length vs Gematria Correlation Analysis:")
    logger.info("Sentence Length | Count | Average Gematria")
    for length in sorted(group_averages.keys()):
        avg_val = group_averages[length]["average_gematria"]
        count = group_averages[length]["count"]
        logger.info("      %d       |  %d   |  %.2f", length, count, avg_val)
    if correlation_coefficient is not None:
        logger.info("Pearson Correlation Coefficient between sentence length and average Gematria: %.4f", correlation_coefficient)
    else:
        logger.info("Insufficient data to compute correlation coefficient.")
    
    return {"group_averages": group_averages, "correlation_coefficient": correlation_coefficient}