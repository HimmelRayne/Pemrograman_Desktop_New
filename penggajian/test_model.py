import unittest
from model import hitung_gaji, Karyawan, periode_valid

class TestPenggajianLengkap(unittest.TestCase):
    
    def test_hitung_gaji_normal(self):
        # Pengujian perhitungan standar: Pokok 5jt, Tunjangan 500rb, 10 jam lembur @25rb, Potongan 100rb
        h = hitung_gaji(5000000, 500000, 10, 25000, 100000)
        self.assertEqual(h["gaji_pokok"], 5000000)
        self.assertEqual(h["tunjangan"], 500000)
        self.assertEqual(h["jam_lembur"], 10)
        self.assertEqual(h["tarif_lembur"], 25000)
        self.assertEqual(h["uang_lembur"], 250000)
        self.assertEqual(h["potongan"], 100000)
        self.assertEqual(h["bruto"], 5750000)
        self.assertEqual(h["netto"], 5650000)

    def test_hitung_gaji_nol(self):
        # Pengujian dengan komponen bernilai nol
        h = hitung_gaji(0, 0, 0, 0, 0)
        self.assertEqual(h["bruto"], 0)
        self.assertEqual(h["netto"], 0)

    def test_input_lembur_gagal(self):
        # Jam lembur tidak valid (huruf, negatif, desimal, melebihi batas 200)
        for jam_salah in ("abc", "-1", "1.5", "201"):
            with self.subTest(jam=jam_salah):
                with self.assertRaises(ValueError):
                    hitung_gaji(5000000, 500000, jam_salah, 25000, 100000)

    def test_potongan_berlebih(self):
        # Potongan tidak boleh melebihi penghasilan bruto
        with self.assertRaises(ValueError):
            hitung_gaji(1000000, 100000, 0, 0, 2000000)

    def test_periode_validasi(self):
        # Format periode yang benar YYYY-MM
        self.assertEqual(periode_valid("2026-10"), "2026-10")
        
        # Format periode yang salah
        for periode_salah in ("2026-13", "2026-00", "26-10", "2026/10", "ABCD-EF"):
            with self.subTest(periode=periode_salah):
                with self.assertRaises(ValueError):
                    periode_valid(periode_salah)

    def test_model_karyawan_dari_form(self):
        # Pengujian validasi dan pembersihan data form karyawan
        data_valid = {
            "nik": "K001-A",
            "nama": "  Budi Santoso  ",
            "jabatan": "Staf IT",
            "gaji_pokok": "4500000",
            "tunjangan": "500000",
            "aktif": "1"
        }
        k = Karyawan.dari_form(data_valid)
        self.assertEqual(k.nik, "K001-A")
        self.assertEqual(k.nama, "Budi Santoso")  # Di-strip otomatis
        self.assertEqual(k.jabatan, "Staf IT")
        self.assertEqual(k.gaji_pokok, 4500000)
        self.assertEqual(k.tunjangan, 500000)
        self.assertEqual(k.aktif, 1)

    def test_model_karyawan_nik_tidak_valid(self):
        # NIK mengandung spasi atau simbol terlarang harus ditolak
        data_invalid = {
            "nik": "K 001",
            "nama": "Budi",
            "jabatan": "Staf",
            "gaji_pokok": "1000000",
            "tunjangan": "0",
            "aktif": "1"
        }
        with self.assertRaises(ValueError):
            Karyawan.dari_form(data_invalid)

if __name__ == "__main__":
    unittest.main()