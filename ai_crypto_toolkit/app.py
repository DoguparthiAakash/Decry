import streamlit as st
import sys
import os

# Ensure the parent directory is in path to load modules correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models.classifier import CryptoClassifier
from models.cipher_solver import ClassicalCipherSolver
from models.anomaly_detector import CryptoAnomalyDetector

st.set_page_config(page_title="AI Cryptography Toolkit", layout="wide")

st.title("AI Cryptography Toolkit")
st.markdown("A unified toolkit blending machine learning, NLP, and statistical analysis for cryptography.")

# Sidebar navigation
page = st.sidebar.selectbox("Choose a Tool", ["Cipher Analyzer", "Classical Cipher Solver", "Anomaly Detector"])

@st.cache_resource
def load_classifier():
    clf = CryptoClassifier()
    model_path = os.path.join(os.path.dirname(__file__), 'models/crypto_classifier.pkl')
    if os.path.exists(model_path):
        clf.load(model_path)
        return clf
    return None

if page == "Cipher Analyzer":
    st.header("Cipher Analyzer")
    st.write("Detect if text is Plaintext, Base64, Hex, MD5, or High-Entropy (AES).")
    
    clf = load_classifier()
    if clf is None:
        st.warning("Classifier model not found. Please run the training script first.")
    else:
        text_input = st.text_area("Enter text to analyze:")
        if st.button("Analyze"):
            if text_input:
                prediction, confidence = clf.predict(text_input)
                st.success(f"**Prediction:** {prediction.upper()}")
                st.info(f"**Confidence:** {confidence:.2%}")
            else:
                st.error("Please enter some text.")

elif page == "Classical Cipher Solver":
    st.header("Classical Cipher Solver")
    st.write("Break simple classical ciphers (like Caesar Shift) using NLP and frequency analysis.")
    
    solver = ClassicalCipherSolver()
    ciphertext = st.text_area("Enter ciphertext:")
    if st.button("Solve"):
        if ciphertext:
            plaintext, method = solver.solve_caesar(ciphertext)
            st.success(f"**Decrypted Text:**\n\n{plaintext}")
            st.info(f"**Method Detected:** {method}")
        else:
            st.error("Please enter ciphertext.")

elif page == "Anomaly Detector":
    st.header("Anomaly Detector")
    st.write("Detect statistical anomalies (like hidden encrypted payloads) in normal text.")
    
    st.info("The Anomaly Detector compares the input text against baseline 'normal' plaintext properties (entropy, character distribution). Highly random strings (like encrypted data) will be flagged as anomalies.")
    
    # Simple simulated logic for demo since we didn't train the anomaly model yet
    # In a real app we'd load the trained IsolationForest model
    text_input = st.text_area("Enter text or log entry to scan:")
    if st.button("Scan for Anomalies"):
        if text_input:
            from models.classifier import calculate_entropy
            entropy = calculate_entropy(text_input)
            
            st.write(f"**Calculated Entropy:** {entropy:.2f}")
            if entropy > 4.5:
                st.error("🚨 **ANOMALY DETECTED:** High entropy payload found. Possible encrypted data or obfuscation.")
            else:
                st.success("✅ **NORMAL:** Text fits normal distribution profiles.")
        else:
            st.error("Please enter some text.")
