import pandas as pd
import pickle
import os
from sklearn.ensemble import IsolationForest
import sys

# Add parent directory to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.classifier import extract_features

class CryptoAnomalyDetector:
    def __init__(self):
        # Isolation Forest for anomaly detection
        self.model = IsolationForest(contamination=0.1, random_state=42)
        
    def train(self, normal_texts):
        X_features = pd.DataFrame([extract_features(text) for text in normal_texts])
        self.model.fit(X_features)
        
    def detect(self, text):
        features = pd.DataFrame([extract_features(text)])
        # Returns -1 for anomalies/outliers and 1 for inliers
        prediction = self.model.predict(features)[0]
        score = self.model.score_samples(features)[0]
        
        is_anomaly = prediction == -1
        return is_anomaly, score

    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
            
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
