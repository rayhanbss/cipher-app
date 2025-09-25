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