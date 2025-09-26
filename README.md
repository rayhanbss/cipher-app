![Matrix](https://i.pinimg.com/originals/b4/e3/71/b4e371619042d1e80918d09904e90f7d.gif)

# Cipher App

A simple flask web application for encrypting and decrypting text and files using various classical ciphers (Affine, Hill, Permutation, Shift, Substitution, Vigenère). Created for Cryptography Course 2025.


## 🚀 Cara Menjalankan Aplikasi

1. **Clone repository ini** (jika belum):
   ```bash
   git clone https://github.com/rayhanbss/cipher-app.git
   cd cipher-app
   ```

2. **Install dependencies Python**
   Pastikan Python 3 sudah terinstall. Install dependencies dengan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**
   ```bash
   python app.py
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:5000/` (atau alamat yang tertera di terminal).

4. **(Opsional) Build CSS dengan Tailwind**
   Jika ingin mengubah style, jalankan:
   ```bash
   npm install
   npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
   ```

## 📝 Cara Menggunakan Aplikasi

1. Buka browser dan akses `http://127.0.0.1:5000/`.
2. Pilih jenis cipher yang ingin digunakan.
3. Masukkan teks yang ingin dienkripsi atau didekripsi.
4. Masukkan kunci (key) jika diperlukan oleh cipher yang dipilih.
5. Klik tombol "Encrypt" untuk mengenkripsi atau "Decrypt" untuk mendekripsi.
6. Hasil akan muncul di field ouput.

## 🔐 Daftar Cipher yang Didukung
- Affine Cipher
- Hill Cipher
- Permutation Cipher
- Shift Cipher
- Substitution Cipher
- Vigenère Cipher

---

Jika ada kendala, silakan buka issue di repository ini.



## ⚙️ Tech Stack 

<p align="left">
   <a href="https://www.python.org/" target="_blank">
      <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
   </a>
   <a href="https://flask.palletsprojects.com/" target="_blank">
      <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
   </a>
   <a href="https://tailwindcss.com/" target="_blank">
      <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS"/>
   </a>
   <a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank">
      <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
   </a>
   <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank">
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
   </a>
</p>

## 👨‍💻 Tim Pengembang

| [<img src="https://github.com/RafiEnhan.png" width="100px"><br><sub><b>Rafi Enhan</b></sub>](https://github.com/RafiEnhan) | [<img src="https://github.com/rayhanbss.png" width="100px"><br><sub><b>Rayhan Bagus Sadewa</b></sub>](https://github.com/rayhanbss) | [<img src="https://github.com/RifqiMakarim.png" width="100px"><br><sub><b>Rifqi Makarim</b></sub>](https://github.com/RifqiMakarim) |
| :---: | :---: | :---: |
