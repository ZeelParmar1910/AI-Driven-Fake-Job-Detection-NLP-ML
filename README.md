# 🛡️ AI-Driven Fake Job Posting Detection System

> **Using Machine Learning and Natural Language Processing (NLP) to protect job seekers from online recruitment scams.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.x-orange?style=flat&logo=scikit-learn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-✓-green?style=flat)](https://xgboost.readthedocs.io/)
[![NLTK](https://img.shields.io/badge/NLTK-NLP-yellow?style=flat)](https://www.nltk.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat)](LICENSE)

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Dataset](#-dataset)
- [Project Pipeline](#-project-pipeline)
- [Models & Results](#-models--results)
- [Key Insights](#-key-insights)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Tech Stack](#-tech-stack)
- [Future Work](#-future-work)

---

## 🚨 Problem Statement

Online job boards like LinkedIn and Indeed host millions of listings — but not all of them are real. Scammers post **fake job advertisements** to:

- 🪪 Steal personal identity information (passports, IDs, SSNs)
- 💰 Demand advance fees for "training" or "visa processing"
- 📄 Harvest resumes and personal data at scale

**This project builds an automated, AI-powered binary classifier** that distinguishes legitimate job postings from fraudulent ones, combining text-based NLP features with structured listing metadata.

| Class | Label | Description |
|---|---|---|
| `0` | **Real** | Legitimate job posting |
| `1` | **Fake** | Fraudulent job posting |

---

## 📊 Dataset

- **Name**: Real / Fake Job Posting Prediction (EMSCAD Dataset)
- **Size**: 17,880 observations, 18 columns
- **Target**: `fraudulent` (binary: 0 or 1)
- **Class Distribution**:
  - ✅ Real Posts: **95.16%** (17,014 rows)
  - 🚨 Fake Posts: **4.84%** (866 rows) — severe class imbalance

> ⚠️ The dataset CSV is **not included** in this repository due to file size (~50 MB).
> Run `python download_dataset.py` to automatically download it, or get it from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction).

---

## ⚙️ Project Pipeline

```
Raw CSV Data
     │
     ▼
┌─────────────────────────────────┐
│   1. Data Loading & EDA         │  → pandas, seaborn, matplotlib
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│   2. NLP Text Preprocessing     │  → NLTK: lowercase, tokenize,
│                                 │    stopword removal, lemmatization
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│   3. Feature Engineering        │  → TF-IDF (top 5,000 n-grams)
│                                 │    + One-Hot Encoded Metadata
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│   4. Feature Fusion             │  → scipy.sparse.hstack
│                                 │    (Text + Metadata)
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│   5. Model Training             │  → Logistic Regression
│      (Stratified 80/20 Split)   │    Random Forest
│                                 │    XGBoost
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│   6. Evaluation & Comparison    │  → F1-Score, Precision, Recall,
│                                 │    ROC-AUC, Confusion Matrix
└─────────────────────────────────┘
```

### NLP Preprocessing Steps
1. **Text Aggregation** — Concatenated `title`, `company_profile`, `description`, `requirements`, `benefits`
2. **Lowercasing** — Standardize text case
3. **Noise Removal** — Removed special characters, punctuation, digits
4. **Tokenization** — Split text into individual tokens
5. **Stopword Removal** — Filtered common English words ("the", "is", "a", ...)
6. **Lemmatization** — Reduced words to their dictionary root form (NLTK WordNet)

---

## 🏆 Models & Results

Three models were trained and compared to evaluate different algorithmic strategies:

| Model | Features | Accuracy | Precision | Recall | **F1-Score** | ROC-AUC |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| Logistic Regression | Text (TF-IDF) only | 96.31% | 57.92% | 86.71% | 69.44% | 98.15% |
| Random Forest | Text + Metadata | 98.21% | 92.25% | 68.79% | 78.81% | 99.28% |
| **XGBoost** ✅ | **Text + Metadata** | **98.63%** | **89.24%** | **81.50%** | **85.20%** | **98.92%** |

### 🥇 Winner: XGBoost

XGBoost achieved the **best overall balance** between Precision and Recall (highest F1-Score) because:
- Gradient boosting iteratively corrects residual errors from previous trees
- `scale_pos_weight` natively penalizes missed fraudulent posts (~19.6× weight on the minority class)
- Effectively leverages the fused NLP + metadata feature space

### Why Not Use Accuracy as the Metric?
A naive classifier that always predicts "Real" would achieve **95.16% accuracy** while catching **zero scams**. We focused on **F1-Score** and **ROC-AUC** as our primary evaluation metrics.

---

## 🔍 Key Insights

| Feature | Insight |
|---|---|
| `has_company_logo = 0` | **Strongest single predictor of fraud** — legitimate companies almost always have a logo |
| `has_questions = 0` | Fake posts rarely include custom application screening questions |
| `required_education = Unspecified` | Missing experience/education strongly correlates with scam entries |
| Text keywords | Phrases around "high returns", "urgent hiring", and vague "work-from-home" language are red flags |

---

## 📁 Project Structure

```
├── data/
│   └── fake_job_postings.csv       # Dataset (download via script)
│
├── notebooks/
│   └── fake_job_postings_detection.ipynb   # Full analysis notebook
│
├── download_dataset.py             # Script to auto-download the dataset
├── generate_notebook.py            # Script that generates the Jupyter notebook
├── requirements.txt                # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-fake-job-detection.git
cd ai-fake-job-detection
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the dataset
```bash
python download_dataset.py
```

### 4. Launch the Jupyter Notebook
```bash
jupyter notebook notebooks/fake_job_postings_detection.ipynb
```

> 💡 Run all cells from top to bottom. The notebook will handle all preprocessing, training, and evaluation automatically.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **Language** | Python 3.8+ |
| **Data Manipulation** | Pandas, NumPy |
| **NLP** | NLTK (Tokenizer, Stopwords, WordNetLemmatizer) |
| **Feature Engineering** | Scikit-Learn TfidfVectorizer, OneHotEncoder |
| **Machine Learning** | Scikit-Learn, XGBoost |
| **Visualization** | Matplotlib, Seaborn |
| **Notebook** | Jupyter Notebook |

---

## 🔮 Future Work

- [ ] 🤖 Replace TF-IDF with **BERT / RoBERTa** transformer embeddings for richer text representations
- [ ] 🌐 Deploy as a **REST API** (FastAPI or Flask) for real-time detection
- [ ] 🔌 Build a **browser extension** that warns users on LinkedIn/Indeed when a suspicious posting is detected
- [ ] 📈 Explore **SMOTE** (Synthetic Minority Oversampling) to further address class imbalance
- [ ] 🔄 Implement a **model retraining pipeline** to combat concept drift as scammer tactics evolve

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Acknowledgements

- Dataset: [Kaggle — Real or Fake Job Posting Prediction](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction) (EMSCAD)
- Libraries: scikit-learn, XGBoost, NLTK, Pandas, Matplotlib

---

*Built as a final project for a Supervised Machine Learning & NLP course.*
