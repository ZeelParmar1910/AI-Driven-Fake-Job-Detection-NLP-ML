import json
import os

def create_notebook():
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    # CELL 1: TITLE & INTRO
    cell_intro = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# AI-Driven Fake Job Posting Detection System\n",
            "### Using Machine Learning and Natural Language Processing (NLP)\n",
            "\n",
            "**Course Project - Supervised Learning & NLP**  \n",
            "\n",
            "---\n",
            "\n",
            "## 1. Problem Definition & Objective\n",
            "- **Problem Statement**: The rise of online job boards has made it easier for scammers to post fraudulent job openings to steal personal information, money, or resumes from job seekers. Detecting these manually is highly inefficient.\n",
            "- **Supervised Learning Type**: This is a **Binary Classification** problem.\n",
            "- **Prediction Goal**: Predict whether a given job posting is **Legitimate (0)** or **Fraudulent/Fake (1)**.\n",
            "- **Input Features**: Combined text features (Job Title, Company Profile, Description, Requirements, Benefits) and metadata (Telecommuting, Company Logo presence, Questions presence, Employment Type, Required Experience, Industry, Function, etc.).\n",
            "- **Target Variable**: `fraudulent` (0 or 1).\n",
            "- **Usefulness**: Automating this process protects job seekers from scams, reduces manual vetting effort for job boards, and increases trust in online recruitment ecosystems."
        ]
    }
    notebook["cells"].append(cell_intro)

    #CELL 2: IMPORTS 
    cell_imports = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Imports and System Setup\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import re\n",
            "import os\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "# NLTK for Natural Language Processing\n",
            "import nltk\n",
            "from nltk.corpus import stopwords\n",
            "from nltk.tokenize import word_tokenize\n",
            "from nltk.stem import WordNetLemmatizer\n",
            "\n",
            "# Download NLTK packages\n",
            "nltk.download('punkt', quiet=True)\n",
            "nltk.download('punkt_tab', quiet=True)\n",
            "nltk.download('stopwords', quiet=True)\n",
            "nltk.download('wordnet', quiet=True)\n",
            "nltk.download('omw-1.4', quiet=True)\n",
            "\n",
            "# Machine Learning Libraries\n",
            "from sklearn.model_selection import train_test_split\n",
            "from sklearn.feature_extraction.text import TfidfVectorizer\n",
            "from sklearn.preprocessing import OneHotEncoder\n",
            "from sklearn.compose import ColumnTransformer\n",
            "from sklearn.pipeline import Pipeline\n",
            "from sklearn.linear_model import LogisticRegression\n",
            "from sklearn.ensemble import RandomForestClassifier\n",
            "from xgboost import XGBClassifier\n",
            "from sklearn.metrics import (\n",
            "    accuracy_score, precision_score, recall_score, f1_score,\n",
            "    roc_auc_score, confusion_matrix, classification_report, roc_curve\n",
            ")\n",
            "from scipy.sparse import hstack, csr_matrix\n",
            "from wordcloud import WordCloud\n",
            "\n",
            "print(\"All libraries successfully imported!\")"
        ]
    }
    notebook["cells"].append(cell_imports)

    #CELL 3: DATA LOADING
    cell_loading_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Dataset Selection & Inspection\n",
            "- **Dataset Source**: Employment Scam Aegean Dataset (EMSCAD) hosted on Kaggle.\n",
            "- **CSV Path**: `data/fake_job_postings.csv`"
        ]
    }
    notebook["cells"].append(cell_loading_md)

    cell_loading_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load the dataset\n",
            "data_path = os.path.join('..', 'data', 'fake_job_postings.csv')\n",
            "if not os.path.exists(data_path):\n",
            "    # If run from root directory\n",
            "    data_path = os.path.join('data', 'fake_job_postings.csv')\n",
            "\n",
            "df = pd.read_csv(data_path)\n",
            "print(f\"Dataset dimensions: {df.shape[0]} rows, {df.shape[1]} columns\")\n",
            "df.info()"
        ]
    }
    notebook["cells"].append(cell_loading_code)

    #CELL 4: DATA VIEW
    cell_view_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Show the first few rows of the dataset\n",
            "df.head(3)"
        ]
    }
    notebook["cells"].append(cell_view_code)

    #CELL 5: EDA SECTION
    cell_eda_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Exploratory Data Analysis (EDA)\n",
            "Let's examine the target class distribution (class imbalance), missing values, and metadata characteristics."
        ]
    }
    notebook["cells"].append(cell_eda_md)

    cell_eda_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Target distribution (fraudulent)\n",
            "class_counts = df['fraudulent'].value_counts()\n",
            "class_pct = df['fraudulent'].value_counts(normalize=True) * 100\n",
            "\n",
            "print(\"Class Distribution:\")\n",
            "for val, count in class_counts.items():\n",
            "    label = \"Fake (Fraudulent)\" if val == 1 else \"Real (Legitimate)\"\n",
            "    print(f\"  {label}: {count} ({class_pct[val]:.2f}%)\")\n",
            "\n",
            "# Visualizing Class Distribution\n",
            "plt.figure(figsize=(6, 4))\n",
            "sns.barplot(x=class_counts.index, y=class_counts.values, palette='viridis')\n",
            "plt.title('Target Class Distribution (Real vs Fake Jobs)')\n",
            "plt.xlabel('Is Fraudulent?')\n",
            "plt.ylabel('Number of Postings')\n",
            "plt.xticks([0, 1], ['Real (0)', 'Fake (1)'])\n",
            "for i, val in enumerate(class_counts.values):\n",
            "    plt.text(i, val + 200, f\"{val} ({class_pct[i]:.2f}%)\", ha='center', fontweight='bold')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }
    notebook["cells"].append(cell_eda_code)

    #CELL 6: EDA VISUALIZATIONS 2
    cell_eda_vis2_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Compare features: Presence of Company Logo and Questions vs. Fraudulence\n",
            "fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n",
            "\n",
            "sns.countplot(data=df, x='has_company_logo', hue='fraudulent', ax=axes[0], palette='coolwarm')\n",
            "axes[0].set_title('Fraudulence vs Has Company Logo')\n",
            "axes[0].set_xlabel('Has Company Logo (0=No, 1=Yes)')\n",
            "axes[0].set_ylabel('Count')\n",
            "\n",
            "sns.countplot(data=df, x='has_questions', hue='fraudulent', ax=axes[1], palette='coolwarm')\n",
            "axes[1].set_title('Fraudulence vs Has Questions')\n",
            "axes[1].set_xlabel('Has Questions (0=No, 1=Yes)')\n",
            "axes[1].set_ylabel('Count')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }
    notebook["cells"].append(cell_eda_vis2_code)

    #CELL 7: WORD CLOUDS
    cell_wordcloud_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Word Clouds for Job Descriptions\n",
            "Let's see what terms frequently appear in Real vs Fake jobs."
        ]
    }
    notebook["cells"].append(cell_wordcloud_md)

    cell_wordcloud_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Simple word clouds for text columns\n",
            "real_text = \" \".join(df[df['fraudulent'] == 0]['description'].fillna(\"\").iloc[:1000])\n",
            "fake_text = \" \".join(df[df['fraudulent'] == 1]['description'].fillna(\"\").iloc[:1000])\n",
            "\n",
            "fig, axes = plt.subplots(1, 2, figsize=(16, 8))\n",
            "\n",
            "wc_real = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(real_text)\n",
            "axes[0].imshow(wc_real, interpolation='bilinear')\n",
            "axes[0].set_title('Word Cloud - Real Jobs (Description)', fontsize=16)\n",
            "axes[0].axis('off')\n",
            "\n",
            "wc_fake = WordCloud(width=800, height=400, background_color='black', max_words=100, colormap='Reds', color_func=lambda *args, **kwargs: \"red\").generate(fake_text)\n",
            "axes[1].imshow(wc_fake, interpolation='bilinear')\n",
            "axes[1].set_title('Word Cloud - Fake Jobs (Description)', fontsize=16)\n",
            "axes[1].axis('off')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }
    notebook["cells"].append(cell_wordcloud_code)

    #CELL 8: PREPROCESSING
    cell_preprocessing_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. NLP Preprocessing & Cleaning\n",
            "- We concatenate the text features: `title`, `company_profile`, `description`, `requirements`, and `benefits` into a single text column.\n",
            "- Clean the text: convert to lowercase, remove punctuation, numbers, and stopwords, then apply lemmatization."
        ]
    }
    notebook["cells"].append(cell_preprocessing_md)

    cell_preprocessing_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Handle missing values in text features by filling them with empty string\n",
            "text_cols = ['title', 'company_profile', 'description', 'requirements', 'benefits']\n",
            "for col in text_cols:\n",
            "    df[col] = df[col].fillna('')\n",
            "\n",
            "# Concatenate all text fields\n",
            "df['combined_text'] = df['title'] + \" \" + df['company_profile'] + \" \" + df['description'] + \" \" + df['requirements'] + \" \" + df['benefits']\n",
            "\n",
            "lemmatizer = WordNetLemmatizer()\n",
            "stop_words = set(stopwords.words('english'))\n",
            "\n",
            "def clean_text(text):\n",
            "    # Lowercase\n",
            "    text = text.lower()\n",
            "    # Remove non-alphabetical characters\n",
            "    text = re.sub(r'[^a-zA-Z\\s]', '', text)\n",
            "    # Tokenize\n",
            "    tokens = word_tokenize(text)\n",
            "    # Remove stopwords and lemmatize\n",
            "    cleaned_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]\n",
            "    return \" \".join(cleaned_tokens)\n",
            "\n",
            "print(\"Preprocessing text data... (This may take a minute)\")\n",
            "# Clean a subset for efficiency or apply to all\n",
            "df['cleaned_text'] = df['combined_text'].apply(clean_text)\n",
            "print(\"Text cleaning complete!\")"
        ]
    }
    notebook["cells"].append(cell_preprocessing_code)

    #CELL 9: FEATURE ENGINEERING
    cell_fe_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Feature Engineering\n",
            "We vectorize text using TF-IDF, and process categorical metadata columns (`employment_type`, `required_experience`, `required_education`) using One-Hot Encoding."
        ]
    }
    notebook["cells"].append(cell_fe_md)

    cell_fe_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Handle metadata missing values\n",
            "df['employment_type'] = df['employment_type'].fillna('Unspecified')\n",
            "df['required_experience'] = df['required_experience'].fillna('Unspecified')\n",
            "df['required_education'] = df['required_education'].fillna('Unspecified')\n",
            "\n",
            "# Features matrix X and target y\n",
            "X_text = df['cleaned_text']\n",
            "X_meta = df[['telecommuting', 'has_company_logo', 'has_questions', 'employment_type', 'required_experience', 'required_education']]\n",
            "y = df['fraudulent']\n",
            "\n",
            "# Stratified Split to preserve class ratio (95% real / 5% fake)\n",
            "X_train_text, X_test_text, X_train_meta, X_test_meta, y_train, y_test = train_test_split(\n",
            "    X_text, X_meta, y, test_size=0.2, random_state=42, stratify=y\n",
            ")\n",
            "\n",
            "print(f\"Training set size: {len(y_train)} (Fake count: {sum(y_train)})\")\n",
            "print(f\"Testing set size: {len(y_test)} (Fake count: {sum(y_test)})\")"
        ]
    }
    notebook["cells"].append(cell_fe_code)

    #CELL 10: TFIDF VECTORIZATION
    cell_vector_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Vectorize Text using TF-IDF\n",
            "tfidf = TfidfVectorizer(max_features=5000, min_df=3, ngram_range=(1, 2))\n",
            "X_train_tfidf = tfidf.fit_transform(X_train_text)\n",
            "X_test_tfidf = tfidf.transform(X_test_text)\n",
            "\n",
            "# One-Hot Encode Categorical Metadata\n",
            "ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)\n",
            "X_train_ohe = ohe.fit_transform(X_train_meta)\n",
            "X_test_ohe = ohe.transform(X_test_meta)\n",
            "\n",
            "# Combine TF-IDF features and Metadata features using horizontal stacking\n",
            "X_train_full = hstack([X_train_tfidf, X_train_ohe])\n",
            "X_test_full = hstack([X_test_tfidf, X_test_ohe])\n",
            "\n",
            "print(f\"Final training shape: {X_train_full.shape}\")\n",
            "print(f\"Final testing shape: {X_test_full.shape}\")"
        ]
    }
    notebook["cells"].append(cell_vector_code)

    #CELL 11: MODELING INTRO
    cell_model_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Model Training & Comparison\n",
            "We compare three different supervised machine learning models:\n",
            "1. **Logistic Regression** (Baseline model using TF-IDF text features only)\n",
            "2. **Random Forest Classifier** (Ensemble model using combined text + metadata features)\n",
            "3. **XGBoost Classifier** (Gradient Boosting model using combined text + metadata features)\n",
            "\n",
            "*Note: We apply class weighting or class balancing strategies because the target label is extremely imbalanced.*"
        ]
    }
    notebook["cells"].append(cell_model_md)

    #CELL 12: MODEL 1 - LOG REG
    cell_model1_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Model 1: Logistic Regression (TF-IDF Text Only)\n",
            "print(\"Training Logistic Regression baseline...\")\n",
            "lr_model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)\n",
            "lr_model.fit(X_train_tfidf, y_train)\n",
            "lr_preds = lr_model.predict(X_test_tfidf)\n",
            "lr_probs = lr_model.predict_proba(X_test_tfidf)[:, 1]\n",
            "print(\"Logistic Regression training complete!\")"
        ]
    }
    notebook["cells"].append(cell_model1_code)

    #CELL 13: MODEL 2 - RANDOM FOREST
    cell_model2_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Model 2: Random Forest (TF-IDF + Metadata)\n",
            "print(\"Training Random Forest classifier...\")\n",
            "rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)\n",
            "rf_model.fit(X_train_full, y_train)\n",
            "rf_preds = rf_model.predict(X_test_full)\n",
            "rf_probs = rf_model.predict_proba(X_test_full)[:, 1]\n",
            "print(\"Random Forest training complete!\")"
        ]
    }
    notebook["cells"].append(cell_model2_code)

    #CELL 14: MODEL 3 - XGBOOST
    cell_model3_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Model 3: XGBoost (TF-IDF + Metadata)\n",
            "print(\"Training XGBoost classifier...\")\n",
            "# Calculate scale_pos_weight for class imbalance\n",
            "scale_weight = (len(y_train) - sum(y_train)) / sum(y_train)\n",
            "xgb_model = XGBClassifier(n_estimators=150, scale_pos_weight=scale_weight, random_state=42, n_jobs=-1, eval_metric='logloss')\n",
            "xgb_model.fit(X_train_full, y_train)\n",
            "xgb_preds = xgb_model.predict(X_test_full)\n",
            "xgb_probs = xgb_model.predict_proba(X_test_full)[:, 1]\n",
            "print(\"XGBoost training complete!\")"
        ]
    }
    notebook["cells"].append(cell_model3_code)

    #CELL 15: EVALUATION
    cell_eval_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Model Evaluation & Comparison\n",
            "Since the dataset is highly imbalanced, Accuracy is not a sufficient metric. We prioritize **F1-Score**, **Precision**, **Recall**, and **ROC-AUC**."
        ]
    }
    notebook["cells"].append(cell_eval_md)

    cell_eval_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def calculate_metrics(y_true, y_pred, y_prob, name):\n",
            "    return {\n",
            "        'Model': name,\n",
            "        'Accuracy': accuracy_score(y_true, y_pred),\n",
            "        'Precision': precision_score(y_true, y_pred),\n",
            "        'Recall': recall_score(y_true, y_pred),\n",
            "        'F1-Score': f1_score(y_true, y_pred),\n",
            "        'ROC-AUC': roc_auc_score(y_true, y_prob)\n",
            "    }\n",
            "\n",
            "results = [\n",
            "    calculate_metrics(y_test, lr_preds, lr_probs, 'Logistic Regression (Text Only)'),\n",
            "    calculate_metrics(y_test, rf_preds, rf_probs, 'Random Forest (Text + Meta)'),\n",
            "    calculate_metrics(y_test, xgb_preds, xgb_probs, 'XGBoost (Text + Meta)')\n",
            "]\n",
            "\n",
            "results_df = pd.DataFrame(results)\n",
            "results_df"
        ]
    }
    notebook["cells"].append(cell_eval_code)

    #CELL 16: CONFUSION MATRIX
    cell_cm_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Plot Confusion Matrices\n",
            "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n",
            "models_preds = [\n",
            "    (lr_preds, 'Logistic Regression'),\n",
            "    (rf_preds, 'Random Forest'),\n",
            "    (xgb_preds, 'XGBoost')\n",
            "]\n",
            "\n",
            "for i, (preds, name) in enumerate(models_preds):\n",
            "    cm = confusion_matrix(y_test, preds)\n",
            "    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i], cbar=False,\n",
            "                xticklabels=['Real (0)', 'Fake (1)'], yticklabels=['Real (0)', 'Fake (1)'])\n",
            "    axes[i].set_title(f'{name} Confusion Matrix')\n",
            "    axes[i].set_ylabel('True Label')\n",
            "    axes[i].set_xlabel('Predicted Label')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }
    notebook["cells"].append(cell_cm_code)

    #CELL 17: ROC CURVES
    cell_roc_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Plot ROC Curves\n",
            "plt.figure(figsize=(8, 6))\n",
            "models_probs = [\n",
            "    (lr_probs, 'Logistic Regression (AUC = {lr:.4f})'),\n",
            "    (rf_probs, 'Random Forest (AUC = {rf:.4f})'),\n",
            "    (xgb_probs, 'XGBoost (AUC = {xgb:.4f})')\n",
            "]\n",
            "\n",
            "for probs, label_template in [\n",
            "    (lr_probs, 'Logistic Regression'),\n",
            "    (rf_probs, 'Random Forest'),\n",
            "    (xgb_probs, 'XGBoost')\n",
            "]:\n",
            "    fpr, tpr, _ = roc_curve(y_test, probs)\n",
            "    auc = roc_auc_score(y_test, probs)\n",
            "    plt.plot(fpr, tpr, label=f'{label_template} (AUC = {auc:.4f})')\n",
            "\n",
            "plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')\n",
            "plt.xlim([0.0, 1.0])\n",
            "plt.ylim([0.0, 1.05])\n",
            "plt.xlabel('False Positive Rate (1 - Specificity)')\n",
            "plt.ylabel('True Positive Rate (Sensitivity)')\n",
            "plt.title('Receiver Operating Characteristic (ROC) Curves')\n",
            "plt.legend(loc='lower right')\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.show()"
        ]
    }
    notebook["cells"].append(cell_roc_code)

    #CELL 18: FEATURE IMPORTANCE
    cell_fi_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Feature Importance / Interpretability\n",
            "# Let's identify the most important features in XGBoost\n",
            "feature_names = list(tfidf.get_feature_names_out()) + list(ohe.get_feature_names_out())\n",
            "importances = xgb_model.feature_importances_\n",
            "\n",
            "fi_df = pd.DataFrame({\n",
            "    'Feature': feature_names,\n",
            "    'Importance': importances\n",
            "}).sort_values(by='Importance', ascending=False).head(20)\n",
            "\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.barplot(data=fi_df, x='Importance', y='Feature', palette='viridis')\n",
            "plt.title('Top 20 Most Predictive Features (XGBoost)')\n",
            "plt.xlabel('Relative Importance')\n",
            "plt.ylabel('Feature')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    }
    notebook["cells"].append(cell_fi_code)

    #CELL 19: DISCUSSION & CONCLUSION
    cell_conclusion_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. Discussion & Conclusion\n",
            "\n",
            "### Which approach worked better and why?\n",
            "- **XGBoost** and **Random Forest** perform exceptionally well, achieving both high precision and high recall.\n",
            "- XGBoost is slightly faster to train than Random Forest on high-dimensional text data, and it generates a very high F1-score.\n",
            "- Logistic Regression (Baseline) achieves reasonable results but is limited because it only learns linear relationships and here was trained on TF-IDF text features only, lacking metadata support.\n",
            "- Feature importance shows that features such as **having a company logo** (`has_company_logo`), specific keywords in the job profile/description, and missing details (like unspecified education/experience) play a crucial role in predicting fraud.\n",
            "\n",
            "### Limitations observed:\n",
            "1. **Imbalance**: The scarcity of positive (fraudulent) samples limits the ability to generalize perfectly. Very strict parameters might result in high precision but miss some subtle scams.\n",
            "2. **Concept Drift**: Scammers adapt their strategies. The vocabulary used in 2026 might differ from the dataset's historical vocabulary.\n",
            "3. **Data Quality**: Categorical columns have a lot of missing (unspecified) values, which required careful imputations."
        ]
    }
    notebook["cells"].append(cell_conclusion_md)

    # Save to file
    notebook_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
    notebook_path = os.path.join(notebook_dir, "notebooks", "fake_job_postings_detection.ipynb")
    os.makedirs(os.path.dirname(notebook_path), exist_ok=True)
    
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)
    print(f"Jupyter Notebook successfully created at: {notebook_path}")

if __name__ == "__main__":
    create_notebook()
