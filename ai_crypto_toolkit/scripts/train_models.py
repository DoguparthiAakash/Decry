import pandas as pd
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.classifier import CryptoClassifier

def train():
    data_path = '../data/crypto_dataset.csv'
    if not os.path.exists(data_path):
        print("Dataset not found. Please run generate_data.py first.")
        return
        
    print("Loading dataset...")
    df = pd.read_csv(data_path)
    
    print("Training Classifier...")
    clf = CryptoClassifier()
    clf.train(df['text'].astype(str), df['label'])
    
    model_path = '../models/crypto_classifier.pkl'
    clf.save(model_path)
    print(f"Classifier trained and saved to {model_path}")

if __name__ == "__main__":
    train()
