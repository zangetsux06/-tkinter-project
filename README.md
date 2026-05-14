# Tkinter Project - Laufey Lyrics Popup

Project ini adalah aplikasi desktop sederhana berbasis Python Tkinter yang menampilkan lirik lagu dalam bentuk popup berurutan sambil memutar musik latar. Setiap baris lirik muncul satu per satu dengan jeda tertentu, lalu ada efek visual seperti shake dan flash di bagian tertentu untuk bikin tampilannya lebih hidup.

## Tentang Project

Tujuan utama project ini adalah bikin tampilan lirik yang lebih menarik daripada teks biasa. Jadi, bukan cuma tampil statis, tapi liriknya muncul bertahap, jendelanya berpindah posisi secara acak, dan ada efek warna serta getar saat bagian tertentu dari lagu diputar.

## Fitur Utama

- Menampilkan lirik secara bertahap per kata
- Popup window muncul di posisi acak
- Musik latar diputar otomatis saat aplikasi dijalankan
- Efek shake dan flash di bagian lirik tertentu
- Tampilan full screen style tanpa border window

## Teknologi yang Dipakai

- Python
- Tkinter
- `threading`
- `ctypes` untuk memutar audio lewat Windows API

## Cara Menjalankan

1. Pastikan Python sudah terpasang.
2. Jalankan file utama:

```bash
python laufey_lyrics.py
```

Kalau kamu mau pakai versi backup, tinggal ganti nama file yang dijalankan.

## Catatan

File musik harus tetap ada di folder project supaya audio bisa diputar dengan benar.
