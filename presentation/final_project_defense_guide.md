# Project Defense Guide: Fake Job Posting Detection
### Final Presentation & Q&A Study Guide

---

## 1. Project Pitch & Motivation
*   **The Problem**: The rise of online recruitment platforms has led to a major increase in job scams. Cybercriminals post fake job advertisements to harvest candidate resumes, extract personal identity information (e.g., social security numbers, passport photos), or demand advance fees for "training" or "visa processing."
*   **Why we chose this**: It represents a critical, real-world security challenge that sits at the intersection of Natural Language Processing (NLP) and Machine Learning (ML). It is an impactful task that directly protects job seekers.
*   **The Aim**: To design and compare multiple supervised classifiers that utilize both textual features (NLP) and listing metadata to flag fraudulent job posts automatically.

---

## 2. Technologies Used & Why
*   **Python**: Chosen for its rich ecosystem of data science and machine learning libraries.
*   **Pandas & NumPy**: For efficient tabular data manipulation, parsing the CSV, and handling missing metadata values.
*   **NLTK (Natural Language Toolkit)**: 
    *   `word_tokenize` to split texts into individual words.
    *   `stopwords` list to filter out diagnostic noise.
    *   `WordNetLemmatizer` to reduce words to their base form (e.g., "requirements" to "requirement"), ensuring consistent word representations.
*   **Scikit-Learn**:
    *   `TfidfVectorizer` to convert text descriptions into a matrix of TF-IDF features (top 5,000 unigrams and bigrams).
    *   `OneHotEncoder` to encode categorical metadata columns.
    *   `LogisticRegression` and `RandomForestClassifier` for modeling.
*   **XGBoost (Extreme Gradient Boosting)**: Used for training our top-performing boosting tree classifier.
*   **Matplotlib & Seaborn**: For generating confusion matrices, ROC-AUC curves, and feature importance charts.

---

## 3. Data Preprocessing & Pipeline Steps
Be prepared to explain the sequential flow of data:
1.  **Imputation**: Replaced null categorical values in metadata columns (like required education) with "Unspecified" so that the model learns the absence of details as a feature.
2.  **Aggregation**: Combined all textual columns (`title`, `company_profile`, `description`, `requirements`, and `benefits`) into a single text block.
3.  **NLP Cleaning**: Converted the text to lowercase, removed numbers and punctuation, tokenized it, stripped out stopwords, and lemmatized the tokens.
4.  **Vectorization**: Fused the TF-IDF representation of the text and the one-hot encoded metadata arrays horizontally using `scipy.sparse.hstack`.
5.  **Stratified Split**: Split the data into 80% training and 20% testing, using stratification to preserve the 95:5 class ratio in both splits.

---

## 4. Addressing Class Imbalance (Crucial grading point!)
*   **The Challenge**: Only 4.84% (866 out of 17,880) of the job posts are fake. If the model simply guesses "Real" every time, it gets 95.16% accuracy but catches zero scams.
*   **Our Solutions**:
    1.  **F1-Score over Accuracy**: We used F1-score as the primary model selection metric since it represents the harmonic mean of Precision and Recall.
    2.  **Class Penalization**: 
        *   Used `class_weight='balanced'` in Logistic Regression and Random Forest.
        *   Configured `scale_pos_weight` in XGBoost. This multiplies the loss of positive (fake class) errors by ~19.6x, forcing the tree builder to prioritize correctly identifying the rare class.

---

## 5. Detailed Model Comparison
*   **Logistic Regression (Baseline)**:
    *   *Features*: Text TF-IDF only.
    *   *Results*: F1: 69.44%, Recall: 86.71%, Precision: 57.92%.
    *   *Analysis*: Reasonable baseline, but has lower precision (too many false alarms) because it lacks metadata context.
*   **Random Forest**:
    *   *Features*: Text + Metadata.
    *   *Results*: F1: 78.81%, Recall: 68.79%, Precision: 92.25%.
    *   *Analysis*: Extremely precise (92.25% of jobs flagged as fake are actually fake), but misses a lot of scams (Recall is only 68.79%).
*   **XGBoost Classifier**:
    *   *Features*: Text + Metadata.
    *   *Results*: F1: 85.20%, Recall: 81.50%, Precision: 89.24%.
    *   *Analysis*: **The Winner**. Balanced Precision and Recall. Gradient boosting iteratively builds trees to correct residual classification errors, which allows it to adapt perfectly to the fused NLP-metadata representation.

---

## 6. Interpretability & Insights
*   **Feature Importance**: The XGBoost model shows that the single most predictive feature is `has_company_logo`. Postings **without** a company logo are statistically much more likely to be fake.
*   **Screening Questions**: Legitimate employers set up custom application questions (`has_questions = 1`). Scam posts rarely include these.
*   **Text Cues**: Keywords related to high returns, urgency, and work-from-home structures with "unspecified" experience/education requirements are highly correlated with fraudulent listings.

---

## 7. Possible Q&A Questions & Answers

#### Q1: "Why did you use lemmatization instead of stemming?"
*   *Answer*: Stemming is rule-based and chops off word endings, often resulting in non-words (e.g., "studying" becomes "studi"). Lemmatization uses vocabulary and morphological analysis to return valid dictionary root words (e.g., "studi" becomes "study"), preserving the semantic relationships in our TF-IDF vectorizer.

#### Q2: "What is the real-world impact of your False Positive Rate?"
*   *Answer*: False positives occur when a real job is flagged as fake. Since our best model (XGBoost) has **89.24% Precision**, only ~10.7% of flagged jobs are false positives. This is an acceptable margin for moderation pipelines, ensuring users aren't flooded with false alarms.

#### Q3: "What are the limitations of this model?"
*   *Answer*: 
    1.  **Concept Drift**: Scammers adapt and write more convincing text over time, meaning the model's vocabulary needs regular updates.
    2.  **Meta-Feature Forgeability**: A sophisticated scammer can easily upload a fake logo or add screening questions to bypass metadata rules, leaving the model heavily reliant on raw text semantics.
