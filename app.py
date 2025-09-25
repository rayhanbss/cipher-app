
from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'encrypt'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'decrypt'))
from encrypt.shift_cipher import shift_cipher as shift_cipher_encrypt
from decrypt.shift_cipher import shift_cipher_decrypt

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
            return "Vigenère cipher not implemented"
        case "hill-cipher":
            return "Hill cipher not implemented"
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

if __name__ == "__main__":
    app.run(debug=True)