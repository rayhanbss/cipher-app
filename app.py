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


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def execute_cipher(function, text, key, is_bytes):
    mode = request.get_json(silent=True) and request.get_json().get('mode', 'encrypt')
    # Convert key to correct type for bytes mode
    if function == "shift-cipher":
        try:
            key = int(key)
        except Exception:
            pass
    elif function == "substitution-cipher":
        try:
            key = int(key)
        except Exception:
            pass
    elif function == "permutation-cipher":
        if isinstance(key, str):
            key = [int(x) for x in key.split(',') if x.strip()]
    elif function == "affine-cipher":
        if isinstance(key, str):
            parts = key.split(',')
            if len(parts) == 2:
                try:
                    key = (int(parts[0]), int(parts[1]))
                except Exception:
                    pass
    match function:
        case "shift-cipher":
            if is_bytes:
                if mode == 'decrypt':
                    return decrypt_shift_bytes(text, key)
                else:
                    return encrypt_shift_bytes(text, key)
            else:
                if mode == 'decrypt':
                    return decrypt_shift_text(text, key)
                else:
                    return encrypt_shift_text(text, key)
        case "substitution-cipher":
            if is_bytes:
                if mode == 'decrypt':
                    return decrypt_substitution_bytes(text, key)
                else:
                    return encrypt_substitution_bytes(text, key)
            else:
                if mode == 'decrypt':
                    return decrypt_substitution_text(text, key)
                else:
                    return encrypt_substitution_text(text, key)
        case "permutation-cipher":
            if is_bytes:
                if mode == 'decrypt':
                    return decrypt_permutation_bytes(text, key)
                else:
                    return encrypt_permutation_bytes(text, key)
            else:
                if mode == 'decrypt':
                    return decrypt_permutation_text(text, key)
                else:
                    return encrypt_permutation_text(text, key)
        case "affine-cipher":
            if is_bytes:
                if mode == 'decrypt':
                    return decrypt_affine_bytes(text, key)
                else:
                    return encrypt_affine_bytes(text, key)
            else:
                if mode == 'decrypt':
                    return decrypt_affine_text(text, key)
                else:
                    return encrypt_affine_text(text, key)
        case "vigenere-cipher":
            return vigenere_decrypt(text, key) if mode == 'decrypt' else vigenere_encrypt(text, key)
        case "hill-cipher":
            return "Hill cipher not implemented"
        case _:
            return "Unknown cipher function"
        

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    cipher_function = data.get("cipher_function", "shift-cipher")
    key = data.get("key", "")

    # If input_bytes_b64 is present, treat as bytes (file mode)
    if 'input_bytes_b64' in data:
        input_bytes = base64.b64decode(data['input_bytes_b64'])
        output_bytes = execute_cipher(cipher_function, input_bytes, key, is_bytes=True)
        # If output is not bytes, convert to bytes
        if isinstance(output_bytes, str):
            output_bytes = output_bytes.encode('utf-8')
        output_bytes_b64 = base64.b64encode(output_bytes).decode('utf-8')
        return jsonify({"output_bytes_b64": output_bytes_b64})
    else:
        input_text = data.get("input_text", "")
        output = execute_cipher(cipher_function, input_text, key, is_bytes=False)
        return jsonify({"output_text": output})

@app.route("/execute_file", methods=["POST"])
def execute_file():
    if 'file-input' not in request.files:
        return "No file part", 400
    
    file = request.files['file-input']
    if file.filename == '':
        return "No selected file", 400
        
    # Ambil data dari form
    key = request.form.get("key", "")
    cipher_function = request.form.get("cipher_function", "shift-cipher")
    mode = request.form.get("mode", "encrypt")
    
    input_bytes = file.read()
    output_bytes = b""

    try:
        match cipher_function:
            case "vigenere-cipher":
                output_bytes = vigenere_decrypt_file(input_bytes, key) if mode == 'decrypt' else vigenere_encrypt_file(input_bytes, key)
            case "hill-cipher":
                output_bytes = hill_decrypt_file(input_bytes, key) if mode == 'decrypt' else hill_encrypt_file(input_bytes, key)
            case _:
                return f"Cipher {cipher_function} not implemented for files.", 400
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    # Siapkan file untuk diunduh
    output_filename = f"encrypted_{file.filename}" if mode == 'encrypt' else f"decrypted_{file.filename}"
    
    return send_file(
        io.BytesIO(output_bytes),
        as_attachment=True,
        download_name=output_filename
    )

if __name__ == "__main__":
    app.run(debug=True)