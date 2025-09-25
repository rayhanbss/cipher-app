from flask import Flask, render_template, request, jsonify
import base64
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'cipher'))
from cipher.shift_cipher import encrypt_shift_bytes
from cipher.shift_cipher import decrypt_shift_bytes
from cipher.shift_cipher import encrypt_shift_text
from cipher.shift_cipher import decrypt_shift_text

from cipher.subtitution_chipper import encrypt_substitution as encrypt_substitution_text
from cipher.subtitution_chipper import decrypt_substitution as decrypt_substitution_text
from cipher.subtitution_chipper import encrypt_bytes_file as encrypt_substitution_bytes
from cipher.subtitution_chipper import decrypt_bytes_file as decrypt_substitution_bytes

from cipher.affine_cipher import encrypt_affine_text
from cipher.affine_cipher import decrypt_affine_text
from cipher.affine_cipher import encrypt_affine_bytes
from cipher.affine_cipher import decrypt_affine_bytes

from cipher.permutation_chipper import encrypt_text as encrypt_permutation_text
from cipher.permutation_chipper import decrypt_text as decrypt_permutation_text
from cipher.permutation_chipper import encrypt_bytes as encrypt_permutation_bytes
from cipher.permutation_chipper import decrypt_bytes as decrypt_permutation_bytes

from cipher.vigenere_cipher import encrypt_vigenere_text, decrypt_vigenere_text, encrypt_vigenere_bytes, decrypt_vigenere_bytes
from cipher.hill_cipher import encrypt_hill_text, decrypt_hill_text, encrypt_hill_bytes, decrypt_hill_bytes


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def execute_cipher(function, data, key, is_bytes):
    mode = request.get_json(silent=True) and request.get_json().get('mode', 'encrypt')
    
    if function == "shift-cipher" or function == "substitution-cipher":
        try: key = int(key)
        except Exception: pass
    elif function == "permutation-cipher":
        if isinstance(key, str): key = [int(x) for x in key.split(',') if x.strip()]
    elif function == "affine-cipher":
        if isinstance(key, str):
            parts = key.split(',')
            if len(parts) == 2:
                try: key = (int(parts[0]), int(parts[1]))
                except Exception: pass

    try:
        match function:
            case "shift-cipher":
                if is_bytes: return decrypt_shift_bytes(data, key) if mode == 'decrypt' else encrypt_shift_bytes(data, key)
                else: return decrypt_shift_text(data, key) if mode == 'decrypt' else encrypt_shift_text(data, key)
            
            case "substitution-cipher":
                if is_bytes: return decrypt_substitution_bytes(data, key) if mode == 'decrypt' else encrypt_substitution_bytes(data, key)
                else: return decrypt_substitution_text(data, key) if mode == 'decrypt' else encrypt_substitution_text(data, key)
            
            case "permutation-cipher":
                if is_bytes: return decrypt_permutation_bytes(data, key) if mode == 'decrypt' else encrypt_permutation_bytes(data, key)
                else: return decrypt_permutation_text(data, key) if mode == 'decrypt' else encrypt_permutation_text(data, key)
            
            case "affine-cipher":
                if is_bytes: return decrypt_affine_bytes(data, key) if mode == 'decrypt' else encrypt_affine_bytes(data, key)
                else: return decrypt_affine_text(data, key) if mode == 'decrypt' else encrypt_affine_text(data, key)

            case "vigenere-cipher":
                if is_bytes: return decrypt_vigenere_bytes(data, key) if mode == 'decrypt' else encrypt_vigenere_bytes(data, key)
                else: return decrypt_vigenere_text(data, key) if mode == 'decrypt' else encrypt_vigenere_text(data, key)
            
            case "hill-cipher":
                if is_bytes: return decrypt_hill_bytes(data, key) if mode == 'decrypt' else encrypt_hill_bytes(data, key)
                else: return decrypt_hill_text(data, key) if mode == 'decrypt' else encrypt_hill_text(data, key)
            
            case _:
                return "Unknown cipher function"
    except Exception as e:
        return str(e)

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    cipher_function = data.get("cipher_function", "shift-cipher")
    key = data.get("key", "")


    if 'input_bytes_b64' in data:
        input_bytes = base64.b64decode(data['input_bytes_b64'])
        output_bytes = execute_cipher(cipher_function, input_bytes, key, is_bytes=True)

        if isinstance(output_bytes, str):
            output_bytes = output_bytes.encode('utf-8')
            
        output_bytes_b64 = base64.b64encode(output_bytes).decode('utf-8')
        return jsonify({"output_bytes_b64": output_bytes_b64})

    else:
        input_text = data.get("input_text", "")
        output = execute_cipher(cipher_function, input_text, key, is_bytes=False)
        return jsonify({"output_text": output})

if __name__ == "__main__":
    app.run(debug=True)