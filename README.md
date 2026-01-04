# Automated Text Extraction and NLP Analysis


## Project Overview

This project implements an **end-to-end automated text analysis pipeline** that extracts online articles from URLs and performs **in-depth linguistic and sentiment analysis** using NLP techniques.

The solution is designed to replicate **real-world data analyst and NLP assignments** commonly used by companies to evaluate skills in **web scraping, text preprocessing, sentiment scoring, and readability analysis**.

It demonstrates the ability to transform **raw, unstructured web content** into a **structured, analytics-ready dataset**.

---

## Business / Real-World Problem

Organizations regularly analyze large volumes of textual content such as:

* News articles
* Blogs and opinion pieces
* Research and policy documents

Manual analysis is slow and error-prone. Businesses need:

* Automated extraction of text from URLs
* Quantitative sentiment and readability metrics
* Structured outputs for downstream analytics

### This project answers:

> **How can we automatically extract online articles and generate standardized text analytics metrics at scale?**

---

## Key Highlights (Recruiter Focused)

* End-to-end **web scraping + NLP pipeline**
* Robust **retry & timeout handling** for network requests
* Custom **sentiment scoring using master dictionaries**
* Readability analysis using **Fog Index & complexity metrics**
* Modular, production-style Python code
* Outputs clean, structured **Excel-ready analytics tables**

---

## Project Workflow

```
Input URLs (Excel)
        ↓
Web Article Extraction (Requests + BeautifulSoup)
        ↓
Text Cleaning & Tokenization
        ↓
Stopword Removal
        ↓
Sentiment Analysis (Positive / Negative)
        ↓
Readability & Linguistic Metrics
        ↓
Structured Output (Excel)
```

---

## Key Functional Components

### 1️. Web Article Extraction

* Fetches article content using `requests` with retry logic
* Parses HTML using **BeautifulSoup**
* Extracts titles and body text
* Saves each article as a local `.txt` file

---

### 2️. Text Preprocessing

* Sentence and word tokenization (NLTK)
* Stopword removal using custom stopword lists
* Alphabetic filtering and normalization

---

### 3️. Sentiment Analysis

* Dictionary-based sentiment scoring
* Computes:

  * Positive Score
  * Negative Score
  * Polarity Score
  * Subjectivity Score

This approach ensures **transparent and explainable sentiment metrics**.

---

### 4️. Readability & Linguistic Metrics

* Average sentence length
* Percentage of complex words
* Fog Index (readability measure)
* Syllables per word
* Average word length
* Personal pronoun count

These metrics are widely used in **content analysis, risk assessment, and editorial analytics**.

---

## Key Outputs

For each article, the pipeline generates:

* Sentiment scores
* Readability metrics
* Word and sentence-level statistics

All results are exported to a **structured Excel file**, ready for reporting or further analysis.

---

## Tech Stack

* **Python**
* Pandas
* Requests
* BeautifulSoup
* NLTK
* Regular Expressions (re)
* Excel I/O

---

## Repository Structure

```
├── Input.xlsx
├── extracted_articles/
├── Output Data Structure.xlsx
├── text_analysis_pipeline.py
├── README.md
```

---

## Why This Project Stands Out (For Recruiters)

* Mirrors **real hiring assignments** used for Data Analyst roles
* Demonstrates **end-to-end ownership** of a data pipeline
* Shows strong skills in:

  * Web scraping
  * NLP preprocessing
  * Text analytics
  * Structured data output
* Emphasizes **code reliability and scalability**

This project is highly relevant for roles such as:

* Data Analyst
* NLP Engineer
* Data Scientist
* Data Operations / Research Analyst

---

## Author

**Rohit Wagh**
Data Analytics | NLP | Machine Learning

🔗 GitHub: [https://github.com/Rohitwagh1406](https://github.com/Rohitwagh1406)

---

## Future Enhancements

* ML-based sentiment classification
* Named Entity Recognition (NER)
* Topic modeling (LDA)
* Dashboard integration (Power BI / Tableau)
* Cloud-based execution

---

*If you find this project valuable, consider starring the repository!*
