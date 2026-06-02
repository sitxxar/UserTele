# Telegram Username Checker

Alat berbasis Command Line Interface (CLI) untuk mengecek ketersediaan username Telegram secara massal, efisien, dan aman menggunakan pustaka resmi **Telethon**.

## Fitur Utama
* **Akurat 100%**: Menggunakan API resmi `CheckUsernameRequest` dari Telegram, bukan scraper web yang tidak akurat.
* **Auto Flood Handling**: Mendeteksi limit rate (`FloodWaitError`) dari Telegram secara otomatis dan menjeda pengecekan sesuai dengan durasi yang diinstruksikan oleh Telegram.
* **Warna Output Interaktif**: Status pengecekan diberi warna berbeda (`AVAILABLE` hijau, `TAKEN` merah, `FLOOD` magenta) untuk keterbacaan tinggi.
* **Konfigurasi Aman**: Dukungan berkas `.gitignore` untuk mencegah berkas sensitif (`config.json` & berkas sesi `.session`) terdorong ke repositori publik.

---

## Panduan Instalasi & Konfigurasi

### Langkah 1: Kloning Repositori
Jalankan perintah berikut pada terminal Anda untuk mengkloning proyek ini:
```bash
git clone https://github.com/sitxxar/UserTele.git
cd UserTele
```

### Langkah 2: Instalasi Dependensi
Pastikan Anda sudah menginstal Python (versi 3.8 ke atas). Kemudian pasang dependensi yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### Langkah 3: Membuat Berkas Konfigurasi
Duplikat berkas templat `config.json.example` menjadi `config.json`:
* **Windows (PowerShell)**:
  ```powershell
  Copy-Item config.json.example config.json
  ```
* **Windows (CMD)**:
  ```cmd
  copy config.json.example config.json
  ```
* **Linux / macOS**:
  ```bash
  cp config.json.example config.json
  ```

### Langkah 4: Mendapatkan API Credentials Telegram
Untuk berkomunikasi dengan API Telegram, Anda memerlukan `api_id` dan `api_hash`:
1. Buka situs resmi **[my.telegram.org](https://my.telegram.org)**.
2. Masukkan nomor telepon akun Telegram Anda (dengan kode negara, contoh: `+628xxxxxxxx`).
3. Masukkan kode konfirmasi yang dikirimkan ke aplikasi Telegram Anda untuk masuk.
4. Pilih menu **API development tools**.
5. Isi formulir pembuatan aplikasi (isi bagian `App title` dan `Short name` secara bebas).
6. Salin kode **App api_id** (angka) dan **App api_hash** (string alfanumerik) yang Anda dapatkan.

### Langkah 5: Mengonfigurasi `config.json`
Buka berkas `config.json` yang baru dibuat menggunakan teks editor (Notepad, VS Code, dll.) dan ganti nilainya dengan API credentials Anda:
```json
{
  "api_id": 0,
  "api_hash": "YOUR_API_HASH_HERE",
  "min_delay": 2.0,
  "max_delay": 5.0
}
```
* `min_delay` & `max_delay` adalah waktu jeda acak (dalam detik) antar request untuk meminimalisasi risiko terkena pemblokiran sementara (FloodWait).

---

## Cara Menjalankan

### 1. Persiapkan Daftar Username
Edit berkas `usernames.txt` dan isi dengan daftar username yang ingin Anda cek (satu username per baris). Contoh:
```text
Aetheron
Novachain
Veltrix
```
*(Catatan: Karakter `@` di depan username akan diabaikan secara otomatis oleh skrip).*

### 2. Jalankan Skrip Utama
Jalankan program dengan perintah berikut:
```bash
python main.py
```

### 3. Login Pertama Kali (Interaktif)
Pada saat pertama kali dijalankan, Telethon akan meminta Anda untuk memasukkan:
1. Nomor telepon akun Telegram Anda.
2. Kode verifikasi OTP yang dikirimkan ke aplikasi Telegram.
3. Password verifikasi dua langkah (2FA) jika Anda mengaktifkannya.

Setelah berhasil masuk, berkas sesi bernama `tg_checker_session.session` akan dibuat secara lokal. Pengecekan berikutnya tidak akan meminta login ulang selama berkas sesi ini tidak dihapus.

### 4. Hasil Output
Semua username yang berstatus **Tersedia (Available)** akan langsung disimpan ke berkas `available.txt` secara realtime.

---

## Opsi Argumen CLI Tambahan
Anda dapat memodifikasi parameter jalannya skrip secara fleksibel tanpa mengubah berkas konfigurasi melalui argumen CLI berikut:
* **Mengubah berkas input username**:
  ```bash
  python main.py -f file_custom.txt
  ```
* **Mengecek username langsung tanpa file**:
  ```bash
  python main.py -u user1,user2,user3
  ```
* **Mengubah berkas output hasil**:
  ```bash
  python main.py -o hasil_tersedia.txt
  ```
* **Mengubah rentang delay**:
  ```bash
  python main.py --min-delay 3.0 --max-delay 10.0
  ```

---

## Keamanan & Kepercayaan
> [!CAUTION]
> **JANGAN PERNAH** membagikan atau mengunggah berkas `config.json` dan `tg_checker_session.session` Anda ke publik (seperti GitHub). Berkas tersebut mengandung akses penuh ke akun Telegram Anda. Berkas ini sudah dimasukkan ke `.gitignore` demi keamanan Anda.
