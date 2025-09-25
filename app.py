
from flask import Flask, render_template, request, jsonify , send_file
import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(__file__), 'encrypt'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'decrypt'))

from encrypt.shift_cipher import shift_cipher as shift_cipher_encrypt
from encrypt.vigenere_cipher import vigenere_encrypt , vigenere_encrypt_file
from encrypt.hill_cipher import hill_encrypt , hill_encrypt_file

from decrypt.shift_cipher import shift_cipher_decrypt
from decrypt.vigenere_cipher import vigenere_decrypt , vigenere_decrypt_file
from decrypt.hill_cipher import hill_decrypt, hill_decrypt_file


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def execute_cipher(function, text, key):
    mode = request.get_json(silent=True) and request.get_json().get('mode', 'encrypt')
    match function:
        case "shift-cipher":
            if mode == 'decrypt':
                return shift_cipher_decrypt(text, key)
            else:
                return shift_cipher_encrypt(text, key)
        case "substitution-cipher":
            return "Substitution cipher not implemented"
        case "affine-cipher":
            return "Affine cipher not implemented"
        case "vigenere-cipher":
            return vigenere_decrypt(text, key) if mode == 'decrypt' else vigenere_encrypt(text, key)
        case "hill-cipher":
             return hill_decrypt(text, key) if mode == 'decrypt' else hill_encrypt(text, key)
        case "permutation-cipher":
            return "Permutation cipher not implemented"
        case _:
            return "Unknown cipher function"
        
@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    input_text = data.get("input_text", "")
    cipher_function = data.get("cipher_function", "shift-cipher")
    key = data.get("key", "")

    # Execute cipher
    output = execute_cipher(cipher_function, input_text, key)

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