import string
import random


class InvalidKeyError(Exception):
    pass

def validate_substitution_key(key):
    key = key.strip()
    if len(key) != 26:
        raise InvalidKeyError("Key harus 26 huruf unik (a-z)!")
    if len(set(key)) != 26:
        raise InvalidKeyError("Key mengandung huruf ganda!")
    if not all(ch.isalpha() and ch.islower() for ch in key):
        raise InvalidKeyError("Key hanya boleh huruf kecil a-z!")
    return True

def encrypt_substitution(plainText, key):
    validate_substitution_key(key)
    alpha_lower = string.ascii_lowercase
    alpha_upper = string.ascii_uppercase

    mapping = {}
    for i, k in enumerate(key):
        mapping[alpha_lower[i]] = k
        mapping[alpha_upper[i]] = k.upper()

    out = []
    for ch in plainText:
        out.append(mapping.get(ch, ch))
    return ''.join(out)

def decrypt_substitution(cipherText, key):
    validate_substitution_key(key)
    alpha_lower = string.ascii_lowercase
    alpha_upper = string.ascii_uppercase

    reverse = {}
    for i, k in enumerate(key):
        reverse[k] = alpha_lower[i]
        reverse[k.upper()] = alpha_upper[i]

    out = []
    for ch in cipherText:
        out.append(reverse.get(ch, ch))
    return ''.join(out)


def validate_seed_key(key):
    
    if not isinstance(key, int):
        raise InvalidKeyError("Key harus berupa integer untuk seed PRNG!")
    return True

def generate_byte_mapping(seed):
    random.seed(seed)
    original = list(range(256))
    shuffled = original.copy()
    random.shuffle(shuffled)
    return dict(zip(original, shuffled)), dict(zip(shuffled, original))

def encrypt_bytes_file(data_bytes, key):
    validate_seed_key(key)
    encrypt_map, _ = generate_byte_mapping(key)
    return bytes(encrypt_map[b] for b in data_bytes)

def decrypt_bytes_file(data_bytes, key):
    validate_seed_key(key)
    _, decrypt_map = generate_byte_mapping(key)
    return bytes(decrypt_map[b] for b in data_bytes)