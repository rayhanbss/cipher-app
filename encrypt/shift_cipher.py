def shift_cipher(text, key):
    # Simple Caesar cipher
    try:
        shift = int(key)
        result = ''
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result
    except Exception:
        return "Invalid key for shift cipher"