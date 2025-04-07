import logging
import statistics
from collections import Counter

from src.text_complexity_analyzer import analyze_text_complexity

def analyze_semantic_complexity_distribution_ayah(quran_data):
    '''
    Analyze text complexity distribution by semantic group frequency at the Ayah level.

    For each Ayah in quran_data:
      - Calculate semantic group frequency by counting the occurrences of each root word (treated as a semantic group).
      - Derive a semantic density metric as the maximum frequency among the semantic groups in that Ayah.
      - Compute text complexity metrics (average word length and average sentence length) based on the ayah's text using the
        analyze_text_complexity function.
    Then, group Ayahs into three categories (low, medium, high) based on the semantic density metric.
    If quantile calculation fails due to insufficient data variability (or not enough distinct semantic density values),
    a fallback strategy is used where all ayahs are assigned to the 'medium' category.
    For each group, descriptive statistics (mean, median, standard deviation, min, max) for both average word length
    and average sentence length are calculated. The quantile boundaries (if available) and the descriptive statistics for each group are logged.

    :param quran_data: List of dictionaries representing Quran data. Each dictionary should include:
                       - 'verse_text': Original verse text.
                       - 'processed_text': (Optional) Preprocessed verse text.
                       - 'roots': List of root words for the verse.
                       - 'surah': Surah identifier.
                       - 'ayah': Ayah identifier.
    :return: Dictionary containing the quantile boundaries (or fallback None) and the descriptive statistics for each group.
    '''
    logger = logging.getLogger("quran_analysis")
    logger.info("Starting Semantic Complexity Distribution Analysis at Ayah Level.")

    # List to hold tuples: (ayah_id, semantic_density, text_complexity_metrics)
    ayah_analysis = []
    for item in quran_data:
        surah = item.get("surah", "Unknown")
        ayah_num = item.get("ayah", "Unknown")
        ayah_id = f"{surah}|{ayah_num}"
        # Use processed_text if available; otherwise use verse_text
        text = item.get("processed_text") or item.get("verse_text", "")
        complexity = analyze_text_complexity(text)
        # Calculate semantic group frequency from roots
        roots = item.get("roots", [])
        if roots:
            root_counts = {}
            for root in roots:
                root_counts[root] = root_counts.get(root, 0) + 1
            semantic_density = max(root_counts.values())
        else:
            semantic_density = 0
        ayah_analysis.append((ayah_id, semantic_density, complexity))

    # Compute quantile thresholds for semantic density across all ayahs
    densities = [entry[1] for entry in ayah_analysis]
    fallback = False
    if densities:
        try:
            boundaries = statistics.quantiles(densities, n=3)
            low_medium_threshold = boundaries[0]
            medium_high_threshold = boundaries[1]
            if low_medium_threshold == medium_high_threshold:
                raise ValueError("Quantile thresholds are equal. Insufficient variability in semantic densities.")
            logger.info("Semantic Density Quantile Boundaries: Low-Medium Threshold: %s, Medium-High Threshold: %s",
                        low_medium_threshold, medium_high_threshold)
        except Exception as e:
            logger.warning("Quantile calculation failed or insufficient variability. Applying fallback strategy: all ayahs assigned to 'medium'. Error: %s", str(e))
            fallback = True
    else:
        fallback = True

    if fallback:
        low_medium_threshold = None
        medium_high_threshold = None
        groups = {"low": [], "medium": [], "high": []}
        for _, _, complexity in ayah_analysis:
            groups["medium"].append(complexity)
    else:
        groups = {"low": [], "medium": [], "high": []}
        for ayah_id, density, complexity in ayah_analysis:
            if density <= low_medium_threshold:
                group = "low"
            elif density <= medium_high_threshold:
                group = "medium"
            else:
                group = "high"
            groups[group].append(complexity)

    # Compute descriptive statistics for each group
    results = {}
    for group_name, complexities in groups.items():
        if complexities:
            avg_word_lengths = [comp["average_word_length"] for comp in complexities if "average_word_length" in comp]
            avg_sentence_lengths = [comp["average_sentence_length"] for comp in complexities if "average_sentence_length" in comp]

            def compute_stats(values):
                if values:
                    mean_val = statistics.mean(values)
                    median_val = statistics.median(values)
                    stdev_val = statistics.stdev(values) if len(values) > 1 else 0
                    min_val = min(values)
                    max_val = max(values)
                    return {"mean": mean_val, "median": median_val, "stdev": stdev_val,
                            "min": min_val, "max": max_val}
                else:
                    return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}

            word_length_stats = compute_stats(avg_word_lengths)
            sentence_length_stats = compute_stats(avg_sentence_lengths)
            results[group_name] = {
                "average_word_length_stats": word_length_stats,
                "average_sentence_length_stats": sentence_length_stats,
                "num_ayahs": len(complexities)
            }
            logger.info("Group '%s' - Number of Ayahs: %d, Average Word Length Stats: %s, Average Sentence Length Stats: %s",
                        group_name, len(complexities), word_length_stats, sentence_length_stats)
        else:
            results[group_name] = {
                "average_word_length_stats": {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0},
                "average_sentence_length_stats": {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0},
                "num_ayahs": 0
            }
            logger.info("Group '%s' has no ayahs.", group_name)

    final_result = {
        "quantile_boundaries": {
            "low_medium_threshold": low_medium_threshold,
            "medium_high_threshold": medium_high_threshold
        },
        "group_statistics": results
    }
    logger.info("Semantic Complexity Distribution Analysis at Ayah Level completed.")
    return final_result