import string

class ClassicalCipherSolver:
    def __init__(self):
        # Basic English letter frequencies for scoring
        self.english_freq = {
            'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253,
            'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094,
            'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
            'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929,
            'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
            'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
            'Y': 0.01974, 'Z': 0.00074
        }
        
    def _score_text(self, text):
        score = 0
        text = text.upper()
        for char in text:
            if char in self.english_freq:
                score += self.english_freq[char]
        return score
        
    def solve_caesar(self, ciphertext):
        best_score = 0
        best_plaintext = ""
        best_shift = 0
        
        for shift in range(26):
            plaintext = ""
            for char in ciphertext:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                    plaintext += decrypted_char
                else:
                    plaintext += char
                    
            score = self._score_text(plaintext)
            if score > best_score:
                best_score = score
                best_plaintext = plaintext
                best_shift = shift
                
        return best_plaintext, f"Caesar Shift: {best_shift}"
