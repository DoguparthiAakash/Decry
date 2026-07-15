import math
import collections
import pickle
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def calculate_entropy(text):
    if not text:
        return 0
    freq = collections.Counter(text)
    length = len(text)
    entropy = -sum((count / length) * math.log2(count / length) for count in freq.values())
    return entropy

def extract_features(text):
    features = {
        'length': len(text),
        'entropy': calculate_entropy(text),
        'alpha_ratio': sum(c.isalpha() for c in text) / max(len(text), 1),
        'digit_ratio': sum(c.isdigit() for c in text) / max(len(text), 1),
        'space_ratio': text.count(' ') / max(len(text), 1),
        'special_char_ratio': sum(not c.isalnum() and not c.isspace() for c in text) / max(len(text), 1)
    }
    return features

class CryptoClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def train(self, X, y):
        # Convert text to features
        X_features = pd.DataFrame([extract_features(text) for text in X])
        self.model.fit(X_features, y)
        
    def predict(self, text):
        features = pd.DataFrame([extract_features(text)])
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = max(probabilities)
        return prediction, confidence
        
    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
            
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
