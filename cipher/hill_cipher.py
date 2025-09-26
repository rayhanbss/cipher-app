
import numpy as np
import math


class InvalidKeyError(Exception):
    pass

def extended_gcd_inverse(a, m):
    if math.gcd(a, m) != 1:
        return None  

    t, new_t = 0, 1
    r, new_r = m, a % m
    
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
        
    if r > 1:
        return None
    if t < 0:
        t = t + m
        
    return t

def modular_matrix_inverse(matrix, modulus):
   
    det = int(np.round(np.linalg.det(matrix)))
    
    det_inv = extended_gcd_inverse(det, modulus)
    if det_inv is None:
        raise InvalidKeyError(f"Determinan {det} tidak memiliki invers modular {modulus}, kunci tidak valid.")

    n = len(matrix)
    if n == 2:
        adj_matrix = np.array([[matrix[1, 1], -matrix[0, 1]], [-matrix[1, 0], matrix[0, 0]]])
    else: 
        adj_matrix = np.zeros_like(matrix, dtype=int)
        for i in range(n):
            for j in range(n):
                minor_matrix = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                cofactor = ((-1)**(i + j)) * int(np.round(np.linalg.det(minor_matrix)))
                adj_matrix[j, i] = cofactor 
    inv_matrix = (det_inv * adj_matrix) % modulus
    return inv_matrix


def create_text_matrix(key):
    key_clean = ''.join(filter(str.isalpha, key.upper()))
    n = int(math.sqrt(len(key_clean)))
    if n * n != len(key_clean):
        raise InvalidKeyError("Panjang kunci (hanya huruf) harus bilangan kuadrat (4, 9, 16, ...).")
    
    matrix = np.array([ord(c) - ord('A') for c in key_clean]).reshape(n, n)
    
    det = int(np.round(np.linalg.det(matrix)))
    if math.gcd(det, 26) != 1:
        raise InvalidKeyError(f"Determinan matriks ({det}) tidak koprima dengan 26. Kunci tidak valid untuk dekripsi.")
    return matrix

def encrypt_hill_text(plaintext, key):
    try:
        key_matrix = create_text_matrix(key)
        n = key_matrix.shape[0]
        text_clean = ''.join(filter(str.isalpha, plaintext.upper()))
        
        pad_len = (n - len(text_clean) % n) % n
        text_clean += 'X' * pad_len
        
        ciphertext = ""
        for i in range(0, len(text_clean), n):
            block = np.array([ord(c) - ord('A') for c in text_clean[i:i+n]])
            enc_block = np.dot(key_matrix, block) % 26
            ciphertext += "".join([chr(c + ord('A')) for c in enc_block])
        return ciphertext
    except InvalidKeyError as e:
        return f"Error: {e}"

def decrypt_hill_text(ciphertext, key):
    try:
        key_matrix = create_text_matrix(key)
        n = key_matrix.shape[0]
        text_clean = ''.join(filter(str.isalpha, ciphertext.upper()))
        
        if len(text_clean) % n != 0:
            return "Error: Panjang ciphertext tidak valid."

        inv_matrix = modular_matrix_inverse(key_matrix, 26)
        
        plaintext = ""
        for i in range(0, len(text_clean), n):
            block = np.array([ord(c) - ord('A') for c in text_clean[i:i+n]])
            dec_block = np.dot(inv_matrix, block) % 26
            plaintext += "".join([chr(c + ord('A')) for c in dec_block])
        return plaintext
    except InvalidKeyError as e:
        return f"Error: {e}"


def create_bytes_matrix(key):
    key_bytes = key.encode('utf-8')
    n = int(math.sqrt(len(key_bytes)))
    if n * n != len(key_bytes):
        raise InvalidKeyError("Panjang kunci (dalam byte) harus bilangan kuadrat (4, 9, 16, ...).")
        
    matrix = np.array(list(key_bytes)).reshape(n, n)
    
    det = int(np.round(np.linalg.det(matrix)))
    if math.gcd(det, 256) != 1: 
        raise InvalidKeyError(f"Determinan matriks ({det}) tidak koprima dengan 256. Kunci tidak valid.")
    return matrix

def encrypt_hill_bytes(data_bytes, key):
    try:
        key_matrix = create_bytes_matrix(key)
        n = key_matrix.shape[0]
        
        pad_len = (n - len(data_bytes) % n) % n
        padding_byte = bytes([pad_len])
        data_bytes += padding_byte * pad_len
        
        encrypted_bytes = bytearray()
        for i in range(0, len(data_bytes), n):
            block = np.array(list(data_bytes[i:i+n]))
            enc_block = np.dot(key_matrix, block) % 256
            encrypted_bytes.extend(enc_block.astype(np.uint8))
        return bytes(encrypted_bytes)
    except InvalidKeyError as e:
        return str(e).encode('utf-8')

def decrypt_hill_bytes(data_bytes, key):
    try:
        key_matrix = create_bytes_matrix(key)
        n = key_matrix.shape[0]

        if len(data_bytes) % n != 0:
            return b"Error: Panjang data terenkripsi tidak valid."

        inv_matrix = modular_matrix_inverse(key_matrix, 256)
        
        decrypted_bytes = bytearray()
        for i in range(0, len(data_bytes), n):
            block = np.array(list(data_bytes[i:i+n]))
            dec_block = np.dot(inv_matrix, block) % 256
            decrypted_bytes.extend(dec_block.astype(np.uint8))
            
        last_byte_val = decrypted_bytes[-1]
        pad_len = int(last_byte_val)
        
        if decrypted_bytes[-pad_len:] != bytes([last_byte_val]) * pad_len:
             return bytes(decrypted_bytes) 

        return bytes(decrypted_bytes[:-pad_len])

    except InvalidKeyError as e:
        return str(e).encode('utf-8')