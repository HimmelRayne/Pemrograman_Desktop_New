import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from repository import KaryawanRepository, GajiRepository
from views.karyawan import KaryawanView
from views.gaji import GajiView
from views.laporan import LaporanView
from ui_common import aman
from model import rupiah

class PenggajianApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SiGaji — Penggajian Karyawan")
        self.geometry("1120x700");self.minsize(850,550)
        self.karyawan_repo = KaryawanRepository();self.gaji_repo = GajiRepository()
        self.content = ttk.Frame(self);self.content.pack(fill="both",expand=True)
        self.status = tk.StringVar(value="Siap")
        ttk.Label(self,textvariable=self.status,relief="sunken",anchor="w").pack(fill="x",side="bottom")
        self.buat_menu();self.protocol("WM_DELETE_WINDOW",self.keluar);self.dashboard()

    def buat_menu(self):
        bar = tk.Menu(self)
        file = tk.Menu(bar,tearoff=False)
        file.add_command(label="Dashboard / Muat Ulang",command=self.dashboard)
        file.add_separator();file.add_command(label="Keluar",command=self.keluar)
        bar.add_cascade(label="File",menu=file)
        master = tk.Menu(bar,tearoff=False)
        master.add_command(label="Data Karyawan",command=lambda:self.tampil(KaryawanView,self.karyawan_repo))
        bar.add_cascade(label="Master Data",menu=master)
        transaksi = tk.Menu(bar,tearoff=False)
        transaksi.add_command(label="Proses Gaji",command=lambda:self.tampil(GajiView,self.karyawan_repo,self.gaji_repo))
        bar.add_cascade(label="Transaksi",menu=transaksi)
        laporan = tk.Menu(bar,tearoff=False)
        laporan.add_command(label="Riwayat, Slip, dan Rekap",command=lambda:self.tampil(LaporanView,self.gaji_repo))
        bar.add_cascade(label="Laporan",menu=laporan)
        bantuan = tk.Menu(bar,tearoff=False)
        bantuan.add_command(label="Tentang",command=lambda:messagebox.showinfo("SiGaji","Proyek Modul 5 — simulasi penggajian lokal.\nSemua nominal rupiah bulat. Riwayat gaji disimpan sebagai snapshot.",parent=self))
        bar.add_cascade(label="Bantuan",menu=bantuan)
        self.config(menu=bar)

    def bersihkan(self):
        for child in self.content.winfo_children():child.destroy()

    def tampil(self,view,*args):
        def proses():
            self.bersihkan();view(self.content,*args).pack(fill="both",expand=True)
            self.status.set(view.__name__)
        aman(self,proses)

    def dashboard(self):
        self.bersihkan()
        frame = ttk.Frame(self.content,padding=25);frame.pack(fill="both",expand=True)
        ttk.Label(frame,text="Dashboard Penggajian",font=("Arial",20,"bold")).pack(anchor="w")
        periode = date.today().strftime("%Y-%m")
        ttk.Label(frame,text=f"Ringkasan periode {periode}. Gunakan menu untuk mengelola data.").pack(anchor="w",pady=10)
        self.status.set("Dashboard")
        def proses():
            r = self.gaji_repo.ringkasan(periode)
            ttk.Label(frame,text=f"Karyawan aktif: {r['aktif']}\nSlip tersimpan: {r['slip']}\nTotal netto: {rupiah(r['netto'])}",font=("Arial",14)).pack(anchor="w",pady=15)
        aman(self,proses)

    def keluar(self):
        if messagebox.askyesno("Keluar","Tutup aplikasi? Pastikan form sudah disimpan.",parent=self):self.destroy()

if __name__ == "__main__":
    PenggajianApp().mainloop()