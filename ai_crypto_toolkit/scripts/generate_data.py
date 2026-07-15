import os
import random
import string
import base64
import hashlib
import binascii
import json
from cryptography.fernet import Fernet
import pandas as pd

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=length))

def generate_base64(text):
    return base64.b64encode(text.encode()).decode()

def generate_hex(text):
    return binascii.hexlify(text.encode()).decode()

def generate_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

def generate_aes(text):
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def generate_dataset(num_samples=1000):
    data = []
    
    # 1. Plaintext
    for _ in range(num_samples):
        text = generate_random_string(random.randint(10, 100))
        data.append({'text': text, 'label': 'plaintext'})
        
    # 2. Base64
    for _ in range(num_samples):
        text = generate_random_string(random.randint(10, 100))
        data.append({'text': generate_base64(text), 'label': 'base64'})
        
    # 3. Hex
    for _ in range(num_samples):
        text = generate_random_string(random.randint(10, 100))
        data.append({'text': generate_hex(text), 'label': 'hex'})
        
    # 4. MD5
    for _ in range(num_samples):
        text = generate_random_string(random.randint(5, 50))
        data.append({'text': generate_md5(text), 'label': 'md5'})
        
    # 5. AES (High Entropy)
    for _ in range(num_samples):
        text = generate_random_string(random.randint(10, 100))
        data.append({'text': generate_aes(text), 'label': 'aes_high_entropy'})
        
    df = pd.DataFrame(data)
    # Shuffle dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Create data dir if not exists
    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/crypto_dataset.csv', index=False)
    print("Dataset generated successfully at ../data/crypto_dataset.csv")

if __name__ == "__main__":
    generate_dataset()
