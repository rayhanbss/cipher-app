class InvalidKeyError(Exception):
    pass

def validate_key(key, data_length):
    """
    Fungsi ini memeriksa apakah kunci (key) yang dimasukkan pengguna valid atau tidak.
    """
    n = len(key)
    if n > data_length:
        raise InvalidKeyError("Key lebih panjang daripada teks!")
    if len(key) != len(set(key)):
        raise InvalidKeyError("Key mengandung angka ganda!")
    if min(key) != 1:
        raise InvalidKeyError("Key harus dimulai dari 1!")
    if set(key) != set(range(1, n + 1)):
        raise InvalidKeyError(f"Key harus berisi angka dari 1 sampai {n} tanpa skip!")
    return True



def encrypt_text(plain_text, key):

    validate_key(key, len(plain_text))
    
    n = len(key)
    
    if len(plain_text) % n != 0:
        padding_needed = n - (len(plain_text) % n)
        plain_text += "x" * padding_needed
    
    rows = len(plain_text) // n
    
    cipher_list = []
    
    for col_number in key:
        col_index = col_number - 1
        for r in range(rows):
            char_index = r * n + col_index
            cipher_list.append(plain_text[char_index])
            
    return "".join(cipher_list)

def decrypt_text(cipher_text, key):

    validate_key(key, len(cipher_text))
    
    n = len(key)
    rows = len(cipher_text) // n
    
    plain_list = [""] * len(cipher_text)
    
    k = 0
    for col_number in key:
        col_index = col_number - 1
        for r in range(rows):
            char_index = r * n + col_index
            plain_list[char_index] = cipher_text[k]
            k += 1
            
    return "".join(plain_list).rstrip("x")


def encrypt_bytes(data_bytes, key):

    validate_key(key, len(data_bytes))
    
    n = len(key)
    
    if len(data_bytes) % n != 0:
        padding_needed = n - (len(data_bytes) % n)
        data_bytes += b"x" * padding_needed
        
    rows = len(data_bytes) // n
    
    cipher_byte_array = bytearray(len(data_bytes))
    k = 0 
    
    for col_number in key:
        col_index = col_number - 1
        for r in range(rows):
            byte_index = r * n + col_index
            cipher_byte_array[k] = data_bytes[byte_index]
            k += 1 

    return bytes(cipher_byte_array)

def decrypt_bytes(cipher_bytes, key):

    validate_key(key, len(cipher_bytes))
    
    n = len(key)
    rows = len(cipher_bytes) // n
    
    plain_byte_array = bytearray(len(cipher_bytes))
    
    k = 0
    
    for col_number in key:
        col_index = col_number - 1
        for r in range(rows):
            byte_index = r * n + col_index
            plain_byte_array[byte_index] = cipher_bytes[k]
            k += 1
            
    return bytes(plain_byte_array).rstrip(b"x")

