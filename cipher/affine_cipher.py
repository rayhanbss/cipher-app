class InvalidKeyError(Exception):
    pass

def validate_affine_key(key):
    if isinstance(key, str):
        parts = key.split(',')
        if len(parts) != 2:
            raise InvalidKeyError('Key must be two integers separated by a comma, e.g. 5,8')
        a, b = map(int, parts)
    elif isinstance(key, (tuple, list)) and len(key) == 2:
        a, b = key
    else:
        raise InvalidKeyError('Key must be two integers (a,b)')
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    if gcd(a, 256) != 1:
        raise InvalidKeyError('a must be coprime with 256 for bytes')
    return a, b

def modinv(a, m):
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise InvalidKeyError('a has no modular inverse')
    if t < 0:
        t = t + m
    return t

def encrypt_affine_bytes(data_bytes, key):
    a, b = validate_affine_key(key)
    return bytes((a * byte + b) % 256 for byte in data_bytes)

def decrypt_affine_bytes(cipher_bytes, key):
    a, b = validate_affine_key(key)
    a_inv = modinv(a, 256)
    return bytes((a_inv * (byte - b)) % 256 for byte in cipher_bytes)
class InvalidKeyError(Exception):
    pass

def encrypt_affine_text(plain_text, key):
    a, b = validate_affine_key(key)
    result = []
    for char in plain_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            enc = (a * x + b) % 26
            result.append(chr(enc + base))
        else:
            result.append(char)
    return ''.join(result)

def decrypt_affine_text(cipher_text, key):
    a, b = validate_affine_key(key)
    a_inv = modinv(a, 26)
    result = []
    for char in cipher_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            y = ord(char) - base
            dec = (a_inv * (y - b)) % 26
            result.append(chr(dec + base))
        else:
            result.append(char)
    return ''.join(result)

