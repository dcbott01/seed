# Mine SEED Bot

Register: [Mine SEED](t.me/seed_coin_bot/app?startapp=5504248798)

## Installation

1. **Download Python 3.6+**
   - Pastikan kamu sudah memiliki Python versi 3.6 atau yang lebih baru. Kamu bisa mendownloadnya dari [python.org](https://www.python.org/downloads/).

2. **Install Modules**
   - Buka command prompt atau terminal, lalu jalankan perintah:
     ```bash
     pip install -r requirements.txt
     ```
   - Ini akan menginstal modul yang diperlukan: `requests` untuk melakukan permintaan HTTP, `colorama` untuk memberi warna teks di konsol, dan `pytz` untuk manajemen zona waktu.

3. **Ambil query_id**
   - Buka Bot Mine SEED dan lakukan inspeksi elemen di halaman tersebut.
   - Pergi ke tab Application (biasanya di browser, ada di bagian atas inspector).
   - Pilih `session storage` dan kemudian `cf.seeddao.org`.
   - Di dalamnya, cari `__telegram_initparam` dan temukan `tgwebappdata`.
   - Ambil nilai `query_id=xxx` atau `user=xxx` (ambil semua nilai ini kecuali `tgwebappnya`).
   - Masukkan nilai `query_id=xxx` atau `user=xxx` ke dalam file `query.txt`

## Running the Script

1. **Jalankan Skrip**
   - Jalankan skrip dengan perintah berikut di terminal:
     ```bash
     python bot.py
     ```

2. **Konfirmasi Aksi Otomatis**
   - Setelah menjalankan skrip, kamu akan diminta untuk mengonfirmasi beberapa tindakan otomatis
   - Masukkan `y` untuk mengaktifkan tindakan otomatis atau `n` untuk menonaktifkannya.

## Features
- **Auto Upgrade Storage**
- **Auto Upgrade Mining**
- **Auto Upgrade Holy**
- **Auto Claim**
- **Auto Catch Worm**
- **Auto Check-in Daily**
- **Multi Account** 

## Notes
- Pastikan token dalam file `query.txt` valid dan tidak kadaluwarsa.

## Contributing

Jika kamu menemukan bug atau ingin menambahkan fitur baru, silakan buat issue atau pull request di repositori ini.


