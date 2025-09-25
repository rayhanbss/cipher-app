import numpy as np
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inverse_256(n):
    g, x, _ = extended_gcd(n, 256)
    if g != 1: return None # Invers tidak ada
    return x % 256

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

def create_key_matrix_file(key):
    key_bytes = key.encode('utf-8')
    n = int(math.sqrt(len(key_bytes)))
    
    if n * n != len(key_bytes):
        raise ValueError("Error: Panjang kunci untuk file harus bilangan kuadrat.")
        
    matrix = np.array(list(key_bytes)).reshape(n, n)
    det = int(np.round(np.linalg.det(matrix)))
    
    if det % 2 == 0:
        raise ValueError("Error: Kunci tidak valid untuk file (determinan genap).")
        
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

def hill_encrypt_file(data_bytes, key):
    try:
        key_matrix = create_key_matrix_file(key)
    except ValueError as e:
        return str(e).encode('utf-8') 

    n = key_matrix.shape[0]
    
    # Padding
    pad_len = (n - len(data_bytes) % n) % n
    padded_data = data_bytes + b'\x00' * pad_len
    
    result_bytes = bytearray()
    for i in range(0, len(padded_data), n):
        block = np.array(list(padded_data[i:i+n]))
        encrypted_block = np.dot(key_matrix, block) % 256
        result_bytes.extend(encrypted_block.astype(int))
        
    return bytes(result_bytes)