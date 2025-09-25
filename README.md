# Cipher App

A simple web application for encrypting and decrypting text using various classical ciphers (Affine, Hill, Permutation, Shift, Substitution, Vigenère).

## Cara Menjalankan Aplikasi

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

## Cara Menggunakan Aplikasi

1. Buka browser dan akses `http://127.0.0.1:5000/`.
2. Pilih jenis cipher yang ingin digunakan.
3. Masukkan teks yang ingin dienkripsi atau didekripsi.
4. Masukkan kunci (key) jika diperlukan oleh cipher yang dipilih.
5. Klik tombol "Encrypt" untuk mengenkripsi atau "Decrypt" untuk mendekripsi.
6. Hasil akan muncul di field ouput.

## Daftar Cipher yang Didukung
- Affine Cipher
- Hill Cipher
- Permutation Cipher
- Shift Cipher
- Substitution Cipher
- Vigenère Cipher

---

Jika ada kendala, silakan buka issue di repository ini.

## 👩‍💻 Tim Pengembang

| [<img src="https://github.com/RafiEnhan.png" width="100px"><br><sub><b>Rafi Enhan</b></sub>](https://github.com/RafiEnhan) | [<img src="https://github.com/rayhanbss.png" width="100px"><br><sub><b>Rayhan Bagus Sadewa</b></sub>](https://github.com/rayhanbss) | [<img src="https://github.com/RifqiMakarim.png" width="100px"><br><sub><b>Rifqi Makarim</b></sub>](https://github.com/RifqiMakarim) |
| :---: | :---: | :---: |
