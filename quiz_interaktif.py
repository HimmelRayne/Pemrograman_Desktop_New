import tkinter as tk
from tkinter import messagebox, ttk
import random


class QuizApp:
    WAKTU_PER_SOAL = 30      # detik
    JEDA_ANIMASI = 150       # milidetik antar tahap animasi

    # Tahap animasi feedback: (warna latar, warna teks)
    FRAME_BENAR = [("#c8e6c9", "black"), ("#a5d6a7", "black"), ("#66bb6a", "white"),
                   ("#43a047", "white"), ("#2e7d32", "white"), ("#2e7d32", "white"),
                   ("#2e7d32", "white"), ("#2e7d32", "white")]
    FRAME_SALAH = [("#c62828", "white"), ("#ffcdd2", "black"), ("#c62828", "white"),
                   ("#ffcdd2", "black"), ("#c62828", "white"), ("#c62828", "white"),
                   ("#c62828", "white"), ("#c62828", "white")]
    FRAME_LEWAT = [("#eeeeee", "black"), ("#bdbdbd", "black"), ("#757575", "white"),
                   ("#757575", "white"), ("#757575", "white")]

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("700x500")
        self.window.resizable(False, False)

        self.questions = [
            {
                "question": "Apa itu event-driven programming?",
                "options": [
                    "Program yang berjalan berurutan",
                    "Program yang merespons kejadian",
                    "Program tanpa GUI",
                    "Program berbasis web"
                ],
                "correct": 1
            },
            {
                "question": "Apa perbedaan utama pemrograman prosedural dan event-driven?",
                "options": [
                    "Event-driven alurnya ditentukan oleh kejadian, prosedural oleh urutan kode",
                    "Prosedural alurnya ditentukan oleh kejadian, event-driven oleh urutan kode",
                    "Keduanya tidak memiliki perbedaan",
                    "Event-driven tidak boleh memakai fungsi"
                ],
                "correct": 0
            },
            {
                "question": "Apa yang dimaksud dengan event handler?",
                "options": [
                    "Widget untuk menampilkan teks",
                    "Jendela utama aplikasi",
                    "Fungsi yang dijalankan ketika suatu event terjadi",
                    "Variabel untuk menyimpan skor"
                ],
                "correct": 2
            },
            {
                "question": "Apa fungsi parameter command pada tk.Button?",
                "options": [
                    "Mengatur warna tombol",
                    "Menentukan fungsi yang dipanggil saat tombol diklik",
                    "Mengatur ukuran jendela",
                    "Menutup program secara otomatis"
                ],
                "correct": 1
            },
            {
                "question": "Method apa yang digunakan untuk menghubungkan event keyboard, "
                            "misalnya <Return>, dengan sebuah fungsi?",
                "options": [
                    "pack()",
                    "config()",
                    "grid()",
                    "bind()"
                ],
                "correct": 3
            },
            {
                "question": "Apa tugas utama mainloop() pada Tkinter?",
                "options": [
                    "Menjalankan event loop yang menunggu dan memproses event",
                    "Membuat semua widget secara otomatis",
                    "Menghapus semua widget dari jendela",
                    "Mengulang program dari awal setiap detik"
                ],
                "correct": 0
            },
            {
                "question": "Method apa yang dipakai untuk memantau perubahan nilai "
                            "StringVar atau IntVar?",
                "options": [
                    "trace_add()",
                    "after_cancel()",
                    "winfo_width()",
                    "pack_forget()"
                ],
                "correct": 0
            },
            {
                "question": "Mengapa timer di Tkinter memakai after() dan bukan time.sleep()?",
                "options": [
                    "Karena time.sleep() tidak bisa dipanggil",
                    "Karena after() membuat jendela lebih besar",
                    "Karena after() menghentikan semua widget",
                    "Karena after() menjadwalkan fungsi tanpa membekukan GUI"
                ],
                "correct": 3
            },
            {
                "question": "Apa yang dimaksud dengan state management pada aplikasi GUI?",
                "options": [
                    "Mengatur warna tema aplikasi",
                    "Mengelola data status aplikasi seperti skor, soal aktif, dan sisa waktu",
                    "Menyimpan aplikasi ke dalam file .exe",
                    "Menghubungkan aplikasi ke internet"
                ],
                "correct": 1
            },
            {
                "question": "Mengapa error handling (try-except) berguna pada validasi input?",
                "options": [
                    "Agar program tidak berhenti mendadak saat input tidak valid",
                    "Agar program berjalan lebih cepat",
                    "Agar widget berubah warna",
                    "Agar mainloop() tidak diperlukan"
                ],
                "correct": 0
            },
        ]
        self.total_questions = len(self.questions)

        # ---- State aplikasi ----
        self.current_question = 0
        self.score = 0
        self.time_left = self.WAKTU_PER_SOAL
        self.selected_answer = tk.IntVar(value=-1)

        self.processed_count = 0      # jumlah soal yang sudah selesai diproses
        self.correct_count = 0
        self.wrong_count = 0
        self.skipped_count = 0        # dilewati atau waktu habis
        self.is_processing = False    # True saat feedback sedang tampil
        self.quiz_finished = False
        self.quiz_started = False     # True setelah tombol Mulai Kuis ditekan
        self.player_name = ""
        self.name_var = tk.StringVar()
        self.timer_id = None          # ID callback after() untuk timer
        self.anim_id = None           # ID callback after() untuk animasi

        self.buat_menu_awal()
        self.buat_interface()
        self.pasang_shortcut()
        self.window.protocol("WM_DELETE_WINDOW", self.tutup_aplikasi)

        # Soal dan timer baru aktif setelah tombol Mulai Kuis ditekan
        self.tampilkan_menu()

    # ------------------------------------------------------------------
    # Antarmuka
    # ------------------------------------------------------------------
    def buat_menu_awal(self):
        warna_banner = "#1a237e"
        warna_kartu = "#e8eaf6"
        self.menu_frame = tk.Frame(self.window)

        banner = tk.Frame(self.menu_frame, bg=warna_banner)
        banner.pack(fill="x")
        tk.Label(banner, text="QUIZ INTERAKTIF", font=("Arial", 26, "bold"),
                 bg=warna_banner, fg="white").pack(pady=(25, 5))
        tk.Label(banner, text="Uji Pengetahuanmu tentang Event-Driven Programming",
                 font=("Arial", 12, "italic"), bg=warna_banner,
                 fg="#c5cae9").pack(pady=(0, 20))

        isi = tk.Frame(self.menu_frame, padx=30)
        isi.pack(fill="both", expand=True)
        tk.Label(isi, text="Kuis pilihan ganda untuk menguji pemahamanmu tentang event handler, "
                           "bind(), mainloop(), IntVar, dan timer after() pada Tkinter.",
                 font=("Arial", 11), wraplength=620, justify="center").pack(pady=(15, 10))

        kartu = tk.Frame(isi, bg=warna_kartu, padx=15, pady=10)
        kartu.pack(fill="x", pady=5)
        info = [
            f"Jumlah soal: {self.total_questions} soal pilihan ganda",
            f"Waktu: {self.WAKTU_PER_SOAL} detik untuk setiap soal",
            "Penilaian: jawaban benar +1 poin; salah atau dilewati 0 poin",
            "Shortcut: Enter = kirim jawaban, Esc = lewati soal",
        ]
        for teks in info:
            tk.Label(kartu, text=teks, bg=warna_kartu, font=("Arial", 11),
                     anchor="w").pack(fill="x")

        baris_nama = tk.Frame(isi)
        baris_nama.pack(pady=12)
        tk.Label(baris_nama, text="Nama pemain:", font=("Arial", 12, "bold")).pack(side="left")
        self.name_entry = tk.Entry(baris_nama, textvariable=self.name_var, width=25,
                                   font=("Arial", 12))
        self.name_entry.pack(side="left", padx=10)

        baris_tombol = tk.Frame(isi)
        baris_tombol.pack(pady=5)
        tk.Button(baris_tombol, text="Mulai Kuis", width=16, bg="#1565c0", fg="white",
                  font=("Arial", 11, "bold"), command=self.mulai_kuis).pack(side="left", padx=10)
        tk.Button(baris_tombol, text="Keluar", width=16, font=("Arial", 11),
                  command=self.tutup_aplikasi).pack(side="left", padx=10)

    def buat_interface(self):
        # ----- Frame kuis (ditampilkan setelah Mulai Kuis) -----
        self.quiz_frame = tk.Frame(self.window, padx=20)
        self.header_label = tk.Label(self.quiz_frame, text="Quiz Interaktif",
                                     font=("Arial", 16, "bold"), fg="#1a237e")
        self.header_label.pack(pady=(10, 5))

        baris_info = tk.Frame(self.quiz_frame)
        baris_info.pack(fill="x")
        self.number_label = tk.Label(baris_info, text="", font=("Arial", 12, "bold"))
        self.number_label.pack(side="left")
        self.score_label = tk.Label(baris_info, text="", font=("Arial", 12, "bold"),
                                    fg="#2e7d32")
        self.score_label.pack(side="right")

        self.progress = ttk.Progressbar(self.quiz_frame, orient="horizontal",
                                        maximum=self.total_questions, value=0)
        self.progress.pack(fill="x", pady=6)

        baris_timer = tk.Frame(self.quiz_frame)
        baris_timer.pack(fill="x")
        self.timer_label = tk.Label(baris_timer, text="", font=("Arial", 12, "bold"))
        self.timer_label.pack(side="left")
        self.processed_label = tk.Label(baris_timer, text="", font=("Arial", 11))
        self.processed_label.pack(side="right")

        self.question_label = tk.Label(self.quiz_frame, text="", font=("Arial", 13),
                                       wraplength=640, justify="left", anchor="w",
                                       height=3)
        self.question_label.pack(fill="x", pady=(8, 4))

        self.option_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.quiz_frame, text="", variable=self.selected_answer,
                                value=i, font=("Arial", 11), anchor="w", justify="left",
                                wraplength=620)
            rb.pack(fill="x", pady=2)
            self.option_buttons.append(rb)

        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Arial", 12, "bold"),
                                       wraplength=640, height=2)
        self.feedback_label.pack(fill="x", pady=8)

        baris_tombol = tk.Frame(self.quiz_frame)
        baris_tombol.pack(pady=2)
        self.submit_button = tk.Button(baris_tombol, text="Submit (Enter)", width=16,
                                       bg="#1565c0", fg="white", font=("Arial", 11, "bold"),
                                       command=self.submit_answer)
        self.submit_button.pack(side="left", padx=10)
        self.skip_button = tk.Button(baris_tombol, text="Skip (Esc)", width=16,
                                     font=("Arial", 11), command=self.skip_question)
        self.skip_button.pack(side="left", padx=10)

        # ----- Frame hasil (ditampilkan saat kuis selesai) -----
        self.result_frame = tk.Frame(self.window, padx=20)
        tk.Label(self.result_frame, text="Kuis Selesai!",
                 font=("Arial", 18, "bold")).pack(pady=(15, 2))
        self.result_greeting_label = tk.Label(self.result_frame, text="",
                                              font=("Arial", 14, "bold"), fg="#2e7d32")
        self.result_greeting_label.pack(pady=(0, 5))
        self.result_score_label = tk.Label(self.result_frame, text="",
                                           font=("Arial", 16, "bold"), fg="#1a237e")
        self.result_score_label.pack(pady=3)
        self.result_percent_label = tk.Label(self.result_frame, text="", font=("Arial", 13))
        self.result_percent_label.pack(pady=3)
        self.result_eval_label = tk.Label(self.result_frame, text="",
                                          font=("Arial", 13, "bold"), wraplength=600)
        self.result_eval_label.pack(pady=8)
        self.result_detail_label = tk.Label(self.result_frame, text="", font=("Arial", 12),
                                            justify="left")
        self.result_detail_label.pack(pady=8)
        baris_hasil = tk.Frame(self.result_frame)
        baris_hasil.pack(pady=15)
        tk.Button(baris_hasil, text="Ulangi Kuis", width=14, bg="#1565c0", fg="white",
                  font=("Arial", 11, "bold"), command=self.restart_quiz).pack(side="left", padx=8)
        tk.Button(baris_hasil, text="Menu Utama", width=14, font=("Arial", 11),
                  command=self.kembali_ke_menu).pack(side="left", padx=8)
        tk.Button(baris_hasil, text="Keluar", width=14, font=("Arial", 11),
                  command=self.tutup_aplikasi).pack(side="left", padx=8)

    def pasang_shortcut(self):
        # Enter: di menu awal = Mulai Kuis, saat kuis = Submit
        self.window.bind("<Return>", self.tekan_enter)
        self.window.bind("<KP_Enter>", self.tekan_enter)
        # Esc melewati soal
        self.window.bind("<Escape>", self.skip_question)

    # ------------------------------------------------------------------
    # Menampilkan soal dan status
    # ------------------------------------------------------------------
    def load_question(self):
        soal = self.questions[self.current_question]
        self.selected_answer.set(-1)  # reset pilihan jawaban
        self.question_label.config(text=soal["question"])
        for i, rb in enumerate(self.option_buttons):
            rb.config(text=soal["options"][i], state="normal")
        self.feedback_label.config(text="", bg=self.window.cget("bg"), fg="black")
        self.submit_button.config(state="normal")
        self.skip_button.config(state="normal")
        self.update_status()

    def update_status(self):
        self.number_label.config(
            text=f"Soal {self.current_question + 1} dari {self.total_questions}")
        self.score_label.config(text=f"Skor: {self.score}")
        self.processed_label.config(
            text=f"Diproses: {self.processed_count}/{self.total_questions}")
        self.progress["value"] = self.processed_count

    def update_timer_label(self):
        warna = "#c62828" if self.time_left <= 10 else "#1a237e"
        self.timer_label.config(text=f"Waktu tersisa: {self.time_left} detik", fg=warna)

    def set_input_state(self, state):
        for rb in self.option_buttons:
            rb.config(state=state)
        self.submit_button.config(state=state)
        self.skip_button.config(state=state)

    # ------------------------------------------------------------------
    # Timer (after / after_cancel)
    # ------------------------------------------------------------------
    def start_timer(self):
        self.cancel_timer()  # pastikan tidak ada timer ganda
        self.time_left = self.WAKTU_PER_SOAL
        self.update_timer_label()
        self.timer_id = self.window.after(1000, self.tick)

    def tick(self):
        self.timer_id = None
        if self.quiz_finished or self.is_processing:
            return
        self.time_left -= 1
        self.update_timer_label()
        if self.time_left <= 0:
            self.finish_question("timeout")
        else:
            self.timer_id = self.window.after(1000, self.tick)

    def cancel_timer(self):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    def cancel_animation(self):
        if self.anim_id is not None:
            self.window.after_cancel(self.anim_id)
            self.anim_id = None

    # ------------------------------------------------------------------
    # Event handler jawaban
    # ------------------------------------------------------------------
    def submit_answer(self, event=None):
        # Abaikan jika kuis belum dimulai, feedback sedang tampil, atau kuis selesai
        if not self.quiz_started or self.quiz_finished or self.is_processing:
            return

        pilihan = self.selected_answer.get()
        if pilihan == -1:
            # Hentikan timer sementara selama dialog tampil, lalu lanjutkan
            self.cancel_timer()
            messagebox.showwarning("Belum Memilih",
                                   "Pilih salah satu jawaban terlebih dahulu!")
            if not self.quiz_finished and not self.is_processing:
                self.timer_id = self.window.after(1000, self.tick)
            return

        benar = self.questions[self.current_question]["correct"]
        if pilihan == benar:
            self.finish_question("benar")
        else:
            self.finish_question("salah")

    def skip_question(self, event=None):
        if not self.quiz_started or self.quiz_finished or self.is_processing:
            return
        self.finish_question("lewat")

    def finish_question(self, hasil):
        """Memproses satu soal tepat satu kali, lalu menjalankan animasi feedback."""
        self.is_processing = True
        self.cancel_timer()
        self.set_input_state("disabled")

        self.processed_count += 1
        if hasil == "benar":
            self.score += 1
            self.correct_count += 1
            teks, frames = "Benar! +1 poin", self.FRAME_BENAR
        elif hasil == "salah":
            self.wrong_count += 1
            soal = self.questions[self.current_question]
            jawaban = soal["options"][soal["correct"]]
            teks, frames = f"Kurang tepat! Jawaban benar: {jawaban}", self.FRAME_SALAH
        elif hasil == "lewat":
            self.skipped_count += 1
            teks, frames = "Soal dilewati.", self.FRAME_LEWAT
        else:  # timeout
            self.skipped_count += 1
            teks, frames = "Waktu habis!", self.FRAME_LEWAT

        self.update_status()
        self.animate_feedback(teks, frames, 0)

    # ------------------------------------------------------------------
    # Animasi feedback berbasis after()
    # ------------------------------------------------------------------
    def animate_feedback(self, teks, frames, tahap):
        if self.quiz_finished:
            return
        if tahap < len(frames):
            latar, huruf = frames[tahap]
            self.feedback_label.config(text=teks, bg=latar, fg=huruf)
            self.anim_id = self.window.after(self.JEDA_ANIMASI, self.animate_feedback,
                                             teks, frames, tahap + 1)
        else:
            self.anim_id = None
            self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question >= self.total_questions:
            self.show_result()
            return
        self.is_processing = False
        self.load_question()
        self.start_timer()

    # ------------------------------------------------------------------
    # Hasil akhir dan ulang kuis
    # ------------------------------------------------------------------
    def show_result(self):
        self.quiz_finished = True
        self.cancel_timer()
        self.cancel_animation()

        persen = self.score / self.total_questions * 100
        if persen >= 80:
            sapaan = f"Selamat, {self.player_name}!"
            evaluasi = "Sangat baik! Pemahaman Anda tentang materi sudah kuat."
        elif persen >= 60:
            sapaan = f"Bagus, {self.player_name}!"
            evaluasi = "Baik. Tinjau kembali beberapa materi agar lebih mantap."
        else:
            sapaan = f"Tetap semangat, {self.player_name}!"
            evaluasi = "Perlu belajar lagi. Pelajari ulang materi Event-Driven Programming."

        self.result_greeting_label.config(text=sapaan)
        self.result_score_label.config(text=f"Skor: {self.score}/{self.total_questions}")
        self.result_percent_label.config(text=f"Persentase nilai: {persen:.0f}%")
        self.result_eval_label.config(text=evaluasi)
        self.result_detail_label.config(
            text=f"Jawaban benar: {self.correct_count}\n"
                 f"Jawaban salah: {self.wrong_count}\n"
                 f"Dilewati / waktu habis: {self.skipped_count}")

        self.quiz_frame.pack_forget()
        self.result_frame.pack(fill="both", expand=True)

    def tekan_enter(self, event=None):
        # Satu pintu untuk Enter agar tidak diproses dua kali
        if not self.quiz_started:
            self.mulai_kuis()
        else:
            self.submit_answer()

    def tampilkan_menu(self):
        self.quiz_frame.pack_forget()
        self.result_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)
        self.name_entry.focus_set()

    def mulai_kuis(self, event=None):
        if self.quiz_started:
            return
        nama = self.name_var.get().strip()
        if not nama:
            messagebox.showwarning("Nama Kosong", "Masukkan nama pemain terlebih dahulu!")
            self.name_entry.focus_set()
            return
        self.player_name = nama[:20]
        self.header_label.config(text=f"Quiz Interaktif - Pemain: {self.player_name}")
        self.menu_frame.pack_forget()
        self.mulai_sesi()

    def reset_state(self):
        # Batalkan semua callback sesi sebelumnya
        self.cancel_timer()
        self.cancel_animation()

        # Reset seluruh state
        self.current_question = 0
        self.score = 0
        self.processed_count = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.skipped_count = 0
        self.is_processing = False
        self.quiz_finished = False
        self.selected_answer.set(-1)
        random.shuffle(self.questions)
        self.progress["value"] = 0

    def mulai_sesi(self):
        self.reset_state()
        self.result_frame.pack_forget()
        self.quiz_frame.pack(fill="both", expand=True)
        self.quiz_started = True
        self.load_question()
        self.start_timer()

    def restart_quiz(self):
        self.mulai_sesi()

    def kembali_ke_menu(self):
        self.reset_state()
        self.quiz_started = False
        self.tampilkan_menu()

    def tutup_aplikasi(self):
        self.quiz_finished = True
        self.cancel_timer()
        self.cancel_animation()
        self.window.destroy()

    def jalankan(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()
