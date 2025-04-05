Quran Secrets Analyzer
======================

This application performs a comprehensive analysis of the Quran text to search for potential secrets and uncover interesting patterns. The analysis includes:

- Keyword Searches (e.g., "Allah", "Ar-Rahman", "Ar-Rahim", "day", "night", "sun", "moon").
- Word Group Searches (e.g., "بسم الله الرحمن الرحيم", "الله أكبر").
- Gematrical Value Analysis (numerical analysis of Arabic words and phrases).
- Word Count Analysis (searching for verses with specific word counts).
- Positional Searches (finding words or phrases at specific positions in verses).
- Combinatorial Searches (combining multiple criteria to identify potential secrets).

These analyses are performed by integrating various search functions from the Quran search modules. All results are logged to the `analysis_results.log` file in the project root. Any potential secrets discovered in the analysis are explicitly tagged with "POTENTIAL SECRET FOUND:" in the log.

How to Run:
-----------
1. Ensure that Python is installed on your system.
2. Install dependencies (if any) by running:
   pip install -r requirements.txt
3. Place the Quran text file (e.g., `quran-uthmani-min.txt`) in the `data` directory.
4. Run the analysis by executing:
   python src/main.py

Viewing Results:
----------------
After running the analysis, check the `analysis_results.log` file in the project root for detailed results and findings.