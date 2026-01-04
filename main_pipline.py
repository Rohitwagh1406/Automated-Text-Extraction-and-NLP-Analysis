import os
import re
import requests
import pandas as pd
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("tokenizers/punkt_tab/english")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

# --------------------------------------------------
# PATH CONFIGURATION (LOCAL)
# --------------------------------------------------

INPUT_FILE = "src/Input.xlsx"
STOPWORDS_FOLDER = "src/StopWords"
MASTER_DICT_FOLDER = "srct/MasterDictionary"
ARTICLE_FOLDER = "src/extracted_articles"
OUTPUT_FILE = "Output Data Structure.xlsx"

# Network / retry configuration
REQUEST_TIMEOUT = 15
RETRY_TOTAL = 3
RETRY_BACKOFF = 1

os.makedirs(ARTICLE_FOLDER, exist_ok=True)

# --------------------------------------------------
# LOAD STOPWORDS
# --------------------------------------------------

def load_stopwords(folder_path):
    stop_words = set()
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="latin-1") as f:
                stop_words.update(word.strip().lower() for word in f)
    return stop_words

# --------------------------------------------------
# LOAD MASTER DICTIONARY
# --------------------------------------------------

def load_dictionary(file_path):
    with open(file_path, "r", encoding="latin-1") as f:
        return set(word.strip().lower() for word in f)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    prev_vowel = False

    for char in word:
        if char in vowels:
            if not prev_vowel:
                count += 1
            prev_vowel = True
        else:
            prev_vowel = False

    if word.endswith(("es", "ed")):
        count -= 1

    return max(count, 1)

def is_complex(word):
    return count_syllables(word) > 2

def count_personal_pronouns(text):
    pattern = r"\b(I|we|my|ours|us)\b"
    return len(re.findall(pattern, text, re.I))

# --------------------------------------------------
# STEP 1: ARTICLE EXTRACTION
# --------------------------------------------------

def extract_articles(df):
    print("Extracting articles...")
    # create a requests Session with retry/backoff
    session = requests.Session()
    retries = Retry(
        total=RETRY_TOTAL,
        connect=RETRY_TOTAL,
        read=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET"]),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    for _, row in df.iterrows():
        url_id = row["URL_ID"]
        url = row["URL"]

        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("h1")
            title_text = title_tag.get_text(strip=True) if title_tag else ""

            content_div = soup.find("div", class_="td-post-content")
            article_text = ""

            if content_div:
                paragraphs = content_div.find_all("p")
                article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

            file_path = os.path.join(ARTICLE_FOLDER, f"{url_id}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(title_text + "\n\n" + article_text)

            print(f"Saved: {url_id}.txt")

        except Exception as e:
            print(f"Failed for {url_id}: {e}")

# --------------------------------------------------
# STEP 2: TEXT ANALYSIS
# --------------------------------------------------

def analyze_text(text, stop_words, positive_words, negative_words):

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    cleaned_words = [
        w.lower() for w in words
        if w.isalpha() and w.lower() not in stop_words
    ]

    word_count = len(cleaned_words)
    sentence_count = len(sentences)

    positive_score = sum(1 for w in cleaned_words if w in positive_words)
    negative_score = sum(1 for w in cleaned_words if w in negative_words)

    polarity_score = (positive_score - negative_score) / (
        (positive_score + negative_score) + 0.000001
    )

    subjectivity_score = (positive_score + negative_score) / (
        word_count + 0.000001
    )

    avg_sentence_length = word_count / sentence_count if sentence_count else 0

    complex_words = [w for w in cleaned_words if is_complex(w)]
    complex_word_count = len(complex_words)

    percentage_complex_words = complex_word_count / word_count if word_count else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    syllables_per_word = (
        sum(count_syllables(w) for w in cleaned_words) / word_count
        if word_count else 0
    )

    personal_pronouns = count_personal_pronouns(text)
    avg_word_length = sum(len(w) for w in cleaned_words) / word_count if word_count else 0

    return [
        positive_score,
        negative_score,
        polarity_score,
        subjectivity_score,
        avg_sentence_length,
        percentage_complex_words,
        fog_index,
        avg_sentence_length,
        complex_word_count,
        word_count,
        syllables_per_word,
        personal_pronouns,
        avg_word_length
    ]

# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():
    print("Loading resources...")
    df = pd.read_excel(INPUT_FILE)

    stop_words = load_stopwords(STOPWORDS_FOLDER)
    positive_words = load_dictionary(os.path.join(MASTER_DICT_FOLDER, "positive-words.txt"))
    negative_words = load_dictionary(os.path.join(MASTER_DICT_FOLDER, "negative-words.txt"))

    # Step 1: Extract articles
    extract_articles(df)

    # Step 2: Analyze text
    print("Performing text analysis...")
    results = []

    for _, row in df.iterrows():
        url_id = row["URL_ID"]
        url = row["URL"]
        article_path = os.path.join(ARTICLE_FOLDER, f"{url_id}.txt")

        if not os.path.exists(article_path):
            continue

        with open(article_path, "r", encoding="utf-8") as f:
            text = f.read()

        metrics = analyze_text(text, stop_words, positive_words, negative_words)
        results.append([url_id, url] + metrics)

    columns = [
        "URL_ID", "URL",
        "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
        "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
        "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
        "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ]

    output_df = pd.DataFrame(results, columns=columns)
    output_df.to_excel(OUTPUT_FILE, index=False)

    print("Analysis completed successfully.")
    print("Output saved as:", OUTPUT_FILE)

# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()
