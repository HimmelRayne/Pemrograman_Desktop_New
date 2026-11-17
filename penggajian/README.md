# Sistem Manajemen Penggajian Karyawan

Aplikasi desktop pembelajaran menggunakan Python Tkinter dan MySQL.

## Persyaratan
- Python 3.10 atau lebih baru
- MySQL Server 8.x (atau versi yang mendukung CHECK constraint)
- Tkinter (umumnya sudah tersedia pada instalasi Python Windows)

## Instalasi di Windows
Buka Command Prompt/PowerShell pada folder `penggajian`, lalu jalankan:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Konfigurasi
Buka `config.ini`, sesuaikan `host`, `port`, `user`, `password`, dan `database`.
Contoh konfigurasi awal menggunakan akun `root` tanpa password. Sesuaikan dengan MySQL lokal Anda.

## Membuat database
Jalankan MySQL, kemudian impor `schema.sql` melalui MySQL Workbench atau terminal:

```bash
mysql -u root -p < schema.sql
```

Jika akun MySQL tidak memakai password, tekan Enter ketika diminta. Pastikan nama database pada `config.ini` sama dengan `db_penggajian_modul5`.

## Memeriksa koneksi
```bash
python cek_koneksi.py
```

## Menjalankan aplikasi
```bash
python app.py
```

## Menjalankan unit test
```bash
python -m unittest -v test_model.py
```

## Modul
- Data Karyawan: tambah, edit, hapus, dan pencarian.
- Transaksi Penggajian: pilih karyawan aktif, hitung lembur, potongan, bruto, dan netto.
- Laporan: filter periode, ekspor CSV, dan cetak slip ke TXT.
- Dashboard: ringkasan karyawan aktif dan total penggajian bulan berjalan.

## Aturan perhitungan
Upah lembur = gaji pokok / 173 × 1,5 × jam lembur.
Nilai 173 jam dan pengali 1,5 merupakan asumsi contoh untuk kebutuhan praktikum.
Sesuaikan dengan kebijakan perusahaan dan ketentuan ketenagakerjaan yang berlaku sebelum digunakan secara operasional.

## Catatan integritas data
- NIK bersifat unik.
- Penghapusan karyawan yang sudah memiliki transaksi penggajian ditolak oleh foreign key RESTRICT.
- Satu karyawan hanya dapat memiliki satu transaksi penggajian per periode.
- Identitas dan gaji pokok disimpan sebagai snapshot pada transaksi.
- Ekspor CSV menetralkan awalan formula yang umum digunakan untuk mengurangi risiko CSV formula injection.
