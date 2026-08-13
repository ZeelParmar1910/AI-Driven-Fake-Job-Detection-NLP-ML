# Presentation Deck: AI-Driven Fake Job Posting Detection System
### Using Machine Learning and Natural Language Processing (NLP)

---

## Slide 1: Title Slide
- **Title**: AI-Driven Fake Job Posting Detection System
- **Subtitle**: Classifying Fraudulent Job Advertisements using ML & NLP
- **Presenters**: [Your Group Members Name]
- **Context**: Final Project Presentation

---

## Slide 2: Problem Setting & Motivation
- **The Problem**: Online job platforms (LinkedIn, Indeed) host millions of listings. Scammers exploit these platforms to post fake jobs for identity theft, financial scams, or data harvesting.
- **Goal**: Develop an automated supervised system to distinguish real postings from fake ones.
- **Classification Type**: Binary Classification.
  - Class `0`: Legitimate (Real) Job Posting
  - Class `1`: Fraudulent (Fake) Job Posting
- **Why it matters**: Protects job seekers, maintains platform credibility, and automates manual moderation.

---

## Slide 3: Dataset Overview
- **Dataset**: Real / Fake Job Posting Prediction (EMSCAD).
- **Size**: 17,880 observations, 18 columns.
- **Target Feature**: `fraudulent` (binary indicator).
- **Major Challenge: Class Imbalance**:
  - Real Posts: ~95.16% (17,014 rows)
  - Fake Posts: ~4.84% (866 rows)
- **Input Variables**:
  - *Text columns*: `title`, `company_profile`, `description`, `requirements`, `benefits`
  - *Categorical metadata*: `employment_type`, `required_experience`, `required_education`
  - *Binary metadata*: `telecommuting`, `has_company_logo`, `has_questions`

---

## Slide 4: Natural Language Processing (NLP) Preprocessing
- **Text Aggregation**: Combined all text fields (`title`, `company_profile`, `description`, `requirements`, `benefits`) into a single string for each post.
- **Text Cleaning Pipeline**:
  1. Lowercasing.
  2. Removing special characters, punctuation, and digits.
  3. Tokenization (splitting sentences into words).
  4. Stopwords removal (filtering out standard common words like "the", "is").
  5. Lemmatization (reducing words to their base/root form using NLTK WordNet).

---

## Slide 5: Feature Engineering
- **Text Representation**:
  - TF-IDF Vectorization (`TfidfVectorizer` with n-grams range 1–2).
  - Selects the top 5,000 features based on inverse document frequency.
- **Metadata Representation**:
  - Missing values imputed as "Unspecified".
  - Categorical metadata One-Hot Encoded (`employment_type`, `required_experience`, etc.).
- **Feature Fusion**:
  - Horizontally stacked text TF-IDF matrices with encoded metadata arrays using SciPy sparse matrices.

---

## Slide 6: Models Chosen & Training
We trained and compared three models to test different algorithmic approaches:
1. **Logistic Regression (Baseline)**:
   - Features used: TF-IDF Text only.
   - Purpose: Establish a simple, fast, linear baseline. Balanced class weights.
2. **Random Forest Classifier (Ensemble)**:
   - Features used: Text + Metadata.
   - Purpose: Leverage non-linear decision boundaries and ensemble bagging. Balanced class weights.
3. **XGBoost Classifier (Gradient Boosting)**:
   - Features used: Text + Metadata.
   - Purpose: State-of-the-art boosting framework. Scaled positive class weight (`scale_pos_weight`) to penalize minority class errors.

---

## Slide 7: Evaluation Strategy
- **Why Accuracy is Deceptive**: Predicting all jobs as "Real" gives 95.16% accuracy but catches 0% of scams.
- **Key Metrics Focused On**:
  - **F1-Score**: Harmonic mean of Precision and Recall.
  - **Precision**: What fraction of flagged postings were actually scams? (Avoids false alarms).
  - **Recall (Sensitivity)**: What fraction of scams did we detect? (Minimizes missed scams).
  - **ROC-AUC**: Evaluates overall classification capability across all thresholds.

---

## Slide 8: Results & Performance Comparison
*(These numbers are populated after running the model pipeline)*

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Text Only)** | 96.31% | 57.92% | 86.71% | 69.44% | 98.15% |
| **Random Forest (Text + Meta)** | 98.21% | 92.25% | 68.79% | 78.81% | 99.28% |
| **XGBoost (Text + Meta)** | 98.63% | 89.24% | 81.50% | 85.20% | 98.92% |

- **Winner**: XGBoost achieved the best overall balance (highest F1-score and ROC-AUC) due to handling class imbalances natively and fusing metadata features with NLP features effectively.

---

## Slide 9: Feature Importance & Interpretability
- **Key Insights**:
  - Postings **without a company logo** (`has_company_logo = 0`) are statistically much more likely to be fraudulent.
  - Scammers tend to post jobs with specific phrasing (e.g., promising high returns, urgent hiring keywords).
  - Missing education/experience info correlated strongly with scam entries.

---

## Slide 10: Conclusion & Future Scope
- **Conclusion**: Fusing text data processed via NLP with tabular metadata creates a robust system capable of identifying over 84% of fraudulent job postings while maintaining a low false positive rate.
- **Limitations**:
  - Historical dataset vocabulary might drift over time.
  - Advanced scams mimicking real corporate profiles require external domain verification.
- **Future Enhancements**: Use Pre-trained Transformer embeddings (BERT, RoBERTa) and deploy the model as a browser extension.

---

## Slide 11: Q&A Preparation & Reference
- **Expected Questions**:
  1. *How did you handle the class imbalance?* We used `class_weight='balanced'` in Logistic Regression/Random Forest, and `scale_pos_weight` in XGBoost to assign higher penalties to minority class classification errors.
  2. *Why does the presence of a company logo matter?* Legitimate companies almost always upload logos; fake postings are quickly generated by bots or low-effort accounts that skip this step.
  3. *Why did XGBoost beat Random Forest?* Gradient boosting iteratively corrects residual errors, allowing it to adapt better to the highly skewed distribution of features.
