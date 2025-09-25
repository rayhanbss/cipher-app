import numpy as np
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def create_key_matrix(key):
    key = ''.join(filter(str.isalpha, key.upper()))
    n = int(math.sqrt(len(key)))

    if n * n != len(key):
        raise ValueError("Error: Panjang kunci Hill Cipher harus bilangan kuadrat sempurna (4, 9, 16, ...).")

    matrix = np.array([ord(char) - ord('A') for char in key]).reshape(n, n)

    det = int(np.round(np.linalg.det(matrix)))
    if det == 0:
        raise ValueError("Error: Determinan matriks kunci adalah nol, tidak bisa diinvers.")
    if gcd(det, 26) != 1:
        raise ValueError(f"Error: Determinan ({det}) tidak koprima dengan 26. Kunci ini tidak bisa untuk dekripsi.")
        
    return matrix

def hill_encrypt(text, key):
    try:
        key_matrix = create_key_matrix(key)
    except ValueError as e:
        return str(e)

    n = key_matrix.shape[0]
    plain_text = ''.join(filter(str.isalpha, text.upper()))
    
    # Padding
    if len(plain_text) % n != 0:
        plain_text += 'X' * (n - len(plain_text) % n)
        
    cipher_text = ""
    for i in range(0, len(plain_text), n):
        block = np.array([ord(char) - ord('A') for char in plain_text[i:i+n]])
        encrypted_block = np.dot(key_matrix, block) % 26
        cipher_text += "".join([chr(code + ord('A')) for code in encrypted_block])
        
    return cipher_text