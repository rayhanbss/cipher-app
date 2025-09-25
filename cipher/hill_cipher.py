# cipher/hill_cipher.py

import numpy as np
import math

class InvalidKeyError(Exception):
    pass

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def mod_inverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1: return x
    return None

# Teks (Modulo 26)
def create_text_matrix(key):
    key_clean = ''.join(filter(str.isalpha, key.upper()))
    n = int(math.sqrt(len(key_clean)))
    if n * n != len(key_clean):
        raise InvalidKeyError("Panjang kunci Hill (hanya huruf) harus bilangan kuadrat.")
    
    matrix = np.array([ord(c) - ord('A') for c in key_clean]).reshape(n, n)
    det = int(np.round(np.linalg.det(matrix)))
    if gcd(det, 26) != 1:
        raise InvalidKeyError(f"Determinan matriks ({det}) tidak valid untuk dekripsi teks.")
    return matrix

def encrypt_hill_text(text, key):
    try:
        key_matrix = create_text_matrix(key)
        n = key_matrix.shape[0]
        text_clean = ''.join(filter(str.isalpha, text.upper()))
        
        pad_len = (n - len(text_clean) % n) % n
        text_clean += 'X' * pad_len
        
        result = ""
        for i in range(0, len(text_clean), n):
            block = np.array([ord(c) - ord('A') for c in text_clean[i:i+n]])
            enc_block = np.dot(key_matrix, block) % 26
            result += "".join([chr(c + ord('A')) for c in enc_block])
        return result
    except Exception as e:
        return str(e)

def decrypt_hill_text(text, key):
    try:
        key_matrix = create_text_matrix(key)
        n = key_matrix.shape[0]
        text_clean = ''.join(filter(str.isalpha, text.upper()))
        
        if len(text_clean) % n != 0:
            return "Error: Panjang ciphertext tidak valid."

        det = int(np.round(np.linalg.det(key_matrix)))
        det_inv = mod_inverse(det, 26)
        
        adj_matrix = np.linalg.inv(key_matrix) * det
        inv_matrix = np.round(det_inv * adj_matrix).astype(int) % 26
        
        result = ""
        for i in range(0, len(text_clean), n):
            block = np.array([ord(c) - ord('A') for c in text_clean[i:i+n]])
            dec_block = np.dot(inv_matrix, block) % 26
            result += "".join([chr(c + ord('A')) for c in dec_block])
        return result
    except Exception as e:
        return str(e)

# Bytes (Modulo 256)
def create_bytes_matrix(key):
    key_bytes = key.encode('utf-8')
    n = int(math.sqrt(len(key_bytes)))
    if n * n != len(key_bytes):
        raise InvalidKeyError("Panjang kunci Hill harus bilangan kuadrat.")
        
    matrix = np.array(list(key_bytes)).reshape(n, n)
    det = int(np.round(np.linalg.det(matrix)))
    if det % 2 == 0:
        raise InvalidKeyError("Determinan matriks kunci tidak boleh genap untuk enkripsi file.")
    return matrix

def encrypt_hill_bytes(data_bytes, key):
    try:
        key_matrix = create_bytes_matrix(key)
        n = key_matrix.shape[0]
        pad_len = (n - len(data_bytes) % n) % n
        data_bytes += b'\x00' * pad_len
        
        result = bytearray()
        for i in range(0, len(data_bytes), n):
            block = np.array(list(data_bytes[i:i+n]))
            enc_block = np.dot(key_matrix, block) % 256
            result.extend(enc_block.astype(int))
        return bytes(result)
    except Exception as e:
        return str(e).encode('utf-8')

def decrypt_hill_bytes(data_bytes, key):
    try:
        key_matrix = create_bytes_matrix(key)
        n = key_matrix.shape[0]

        det = int(np.round(np.linalg.det(key_matrix)))

        t, newt = 0, 1
        r, newr = 256, det
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        if r > 1: raise InvalidKeyError("Determinan tidak memiliki invers modular 256.")
        det_inv = t % 256

        adj_matrix = np.linalg.inv(key_matrix) * det
        inv_matrix = np.round(det_inv * adj_matrix).astype(int) % 256
        
        result = bytearray()
        for i in range(0, len(data_bytes), n):
            block = np.array(list(data_bytes[i:i+n]))
            dec_block = np.dot(inv_matrix, block) % 256
            result.extend(dec_block.astype(int))
        return bytes(result).rstrip(b'\x00')
    except Exception as e:
        return str(e).encode('utf-8')