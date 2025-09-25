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

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def mod_inverse_256(n):
    g, x, _ = extended_gcd(n, 256)
    if g != 1: return None
    return x % 256

def create_key_matrix(key):
    key = ''.join(filter(str.isalpha, key.upper()))
    n = int(math.sqrt(len(key)))
    if n * n != len(key):
        raise ValueError("Error: Panjang kunci Hill Cipher harus bilangan kuadrat sempurna (4, 9, 16, ...).")
    matrix = np.array([ord(char) - ord('A') for char in key]).reshape(n, n)
    det = int(np.round(np.linalg.det(matrix)))
    if gcd(det, 26) != 1:
        raise ValueError(f"Error: Determinan ({det}) tidak koprima dengan 26. Kunci ini tidak valid.")
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

def get_inverse_matrix(matrix):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = mod_inverse(det, 26)
    
    adjugate_matrix = np.linalg.inv(matrix) * det
    inverse_matrix = (det_inv * adjugate_matrix) % 26
    return np.round(inverse_matrix).astype(int)

def get_inverse_matrix_file(matrix):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = mod_inverse_256(det)
    if det_inv is None:
        raise ValueError("Tidak dapat menemukan invers modular dari determinan.")
    
    adjugate_matrix = np.linalg.inv(matrix) * det
    inverse_matrix = (det_inv * adjugate_matrix) % 256
    return np.round(inverse_matrix).astype(int)

def hill_decrypt(text, key):
    try:
        key_matrix = create_key_matrix(key)
        inv_key_matrix = get_inverse_matrix(key_matrix)
    except ValueError as e:
        return str(e)

    n = key_matrix.shape[0]
    cipher_text = ''.join(filter(str.isalpha, text.upper()))
    
    if len(cipher_text) % n != 0:
        return "Error: Panjang ciphertext tidak sesuai dengan ukuran blok kunci."

    plain_text = ""
    for i in range(0, len(cipher_text), n):
        block = np.array([ord(char) - ord('A') for char in cipher_text[i:i+n]])
        decrypted_block = np.dot(inv_key_matrix, block) % 26
        plain_text += "".join([chr(code + ord('A')) for code in decrypted_block])
        
    return plain_text

def hill_decrypt_file(data_bytes, key):
    try:
        key_matrix = create_key_matrix_file(key)
        inv_key_matrix = get_inverse_matrix_file(key_matrix)
    except ValueError as e:
        return str(e).encode('utf-8')

    n = key_matrix.shape[0]
    
    if len(data_bytes) % n != 0:
        return b"Error: Panjang file terenkripsi tidak sesuai dengan blok kunci."
        
    result_bytes = bytearray()
    for i in range(0, len(data_bytes), n):
        block = np.array(list(data_bytes[i:i+n]))
        decrypted_block = np.dot(inv_key_matrix, block) % 256
        result_bytes.extend(decrypted_block.astype(int))
        
    return bytes(result_bytes).rstrip(b'\x00')