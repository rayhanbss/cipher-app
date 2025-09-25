import re

def vigenere_decrypt(text, key):
    if not key.isalpha():
        return "Error: Kunci Vigenère hanya boleh berisi huruf alfabet."

    key = key.upper()
    result = ""
    key_index = 0
    
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            
            text_offset = ord(char) - base
            key_offset = ord(key[key_index % len(key)]) - ord('A')

            decrypted_char = chr(((text_offset - key_offset + 26) % 26) + base)
            result += decrypted_char
            
            key_index += 1
        else:
            result += char
            
    return result

def vigenere_decrypt_file(data_bytes, key):
    key_bytes = key.encode('utf-8')
    if not key_bytes:
        raise ValueError("Kunci tidak boleh kosong.")
    
    result_bytes = bytearray()
    key_len = len(key_bytes)
    
    for i, byte in enumerate(data_bytes):
        key_byte = key_bytes[i % key_len]
        # Rumus dekripsi byte: (C - K) mod 256
        new_byte = (byte - key_byte + 256) % 256
        result_bytes.append(new_byte)
        
    return bytes(result_bytes)