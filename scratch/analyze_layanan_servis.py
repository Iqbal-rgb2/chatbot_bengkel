import sys
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from web.nlp.preprocessor import normalize_user_input
from web.nlp.classifier import prioritize_intent

def main():
    # Load dataset
    dataset_path = BASE_DIR / 'data' / 'processed' / 'dataset_augmented.csv'
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {dataset_path}")
        return
    
    combined = pd.read_csv(dataset_path).fillna('')
    
    # Encode intent labels
    le_eval = LabelEncoder()
    combined['label'] = le_eval.fit_transform(combined['intent'])
    
    # Split dataset with stratification (exactly as in augment_and_retrain.py)
    train_df, test_df = train_test_split(
        combined,
        test_size=0.2,
        random_state=3,
        stratify=combined['label']
    )
    
    # Fit Vectorizer and Classifier
    vec_eval = TfidfVectorizer()
    X_train = vec_eval.fit_transform(train_df['processed_question'])
    y_train = train_df['label']
    
    clf_eval = MultinomialNB()
    clf_eval.fit(X_train, y_train)
    
    # Predict on test split
    X_test = vec_eval.transform(test_df['processed_question'])
    y_pred_raw_idx = clf_eval.predict(X_test)
    
    print("=== ANALYSIS OF FALSE POSITIVES FOR 'layanan_servis' ===")
    print(f"Total test samples: {len(test_df)}")
    
    false_positives = []
    
    for i, row in test_df.reset_index(drop=True).iterrows():
        actual_intent = row['intent']
        question = row['pertanyaan']
        processed = row['processed_question']
        
        # Raw Prediction from Naive Bayes
        raw_pred_intent = le_eval.classes_[y_pred_raw_idx[i]]
        
        # Apply production pipeline rules
        normalized = normalize_user_input(question)
        final_intent = prioritize_intent(normalized, raw_pred_intent)
        
        # We are looking for cases where:
        # Actual is NOT 'layanan_servis', but Final is 'layanan_servis'
        if actual_intent != 'layanan_servis' and final_intent == 'layanan_servis':
            false_positives.append({
                'pertanyaan': question,
                'processed': processed,
                'actual_intent': actual_intent,
                'nb_raw_intent': raw_pred_intent,
                'final_intent': final_intent
            })
            
    print(f"Found {len(false_positives)} False Positives for 'layanan_servis':\n")
    for idx, fp in enumerate(false_positives, 1):
        print(f"{idx}. Pertanyaan: \"{fp['pertanyaan']}\"")
        print(f"   Processed: \"{fp['processed']}\"")
        print(f"   Actual Intent: {fp['actual_intent']}")
        print(f"   NB Raw Pred:  {fp['nb_raw_intent']}")
        print(f"   Final Pred:   {fp['final_intent']}")
        print("-" * 50)

if __name__ == '__main__':
    main()
