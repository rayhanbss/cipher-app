class InvalidKeyError(Exception):
    pass

def validate_shift_key(key):
    if not isinstance(key, int):
        try:
            key = int(key)
        except Exception:
            raise InvalidKeyError("Key harus berupa integer!")
    if not (0 <= int(key) < 26):
        raise InvalidKeyError("Key harus antara 0 dan 25!")
    return int(key)

def encrypt_shift_text(plain_text, key):
    shift = validate_shift_key(key)
    result = []
    for char in plain_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

def decrypt_shift_text(cipher_text, key):
    shift = validate_shift_key(key)
    result = []
    for char in cipher_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

def encrypt_shift_bytes(data_bytes, key):
    shift = validate_shift_key(key)
    return bytes((b + shift) % 256 for b in data_bytes)

def decrypt_shift_bytes(cipher_bytes, key):
    shift = validate_shift_key(key)
    return bytes((b - shift) % 256 for b in cipher_bytes)