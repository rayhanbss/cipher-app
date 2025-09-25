
class InvalidKeyError(Exception):
    pass

def validate_vigenere_key(key):
    if not isinstance(key, str) or not key.isalpha():
        raise InvalidKeyError("Kunci Vigenère harus berupa kata (hanya huruf).")
    return key.upper()

# Teks (Modulo 26)
def encrypt_vigenere_text(text, key):
    try:
        valid_key = validate_vigenere_key(key)
    except InvalidKeyError as e:
        return str(e)
    
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            text_offset = ord(char) - base
            key_offset = ord(valid_key[key_index % len(valid_key)]) - ord('A')
            
            encrypted_char = chr(((text_offset + key_offset) % 26) + base)
            result.append(encrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def decrypt_vigenere_text(text, key):
    try:
        valid_key = validate_vigenere_key(key)
    except InvalidKeyError as e:
        return str(e)

    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            text_offset = ord(char) - base
            key_offset = ord(valid_key[key_index % len(valid_key)]) - ord('A')
            
            decrypted_char = chr(((text_offset - key_offset + 26) % 26) + base)
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

# Bytes (Modulo 256)
def encrypt_vigenere_bytes(data_bytes, key):
    try:
        valid_key = validate_vigenere_key(key)
        key_bytes = valid_key.encode('utf-8')
    except InvalidKeyError as e:
        return str(e)

    result_bytes = bytearray()
    key_len = len(key_bytes)
    for i, byte in enumerate(data_bytes):
        key_byte = key_bytes[i % key_len]
        new_byte = (byte + key_byte) % 256
        result_bytes.append(new_byte)
    return bytes(result_bytes)

def decrypt_vigenere_bytes(data_bytes, key):
    try:
        valid_key = validate_vigenere_key(key)
        key_bytes = valid_key.encode('utf-8')
    except InvalidKeyError as e:
        return str(e)
        
    result_bytes = bytearray()
    key_len = len(key_bytes)
    for i, byte in enumerate(data_bytes):
        key_byte = key_bytes[i % key_len]
        new_byte = (byte - key_byte + 256) % 256
        result_bytes.append(new_byte)
    return bytes(result_bytes)