
import tkinter as tkinter
import random

class AnimasiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pingpong 1.1.1")
        self.root.resizable(False, False)

        self.lebar = 600
        self.tinggi = 400

        self.canvas = tkinter.Canvas(
            root,
            width=self.lebar,
            height=self.tinggi,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        self.canvas.create_text(
            300, 20,
            text="PINGPONG",
            fill="white",
            font=("Arial", 16, "bold")
        )

        self.skor = 0
        self.teks_skor = self.canvas.create_text(
            300, 50,
            text="Skor: 0",
            fill="white",
            font=("Arial", 14)
        )

        self.paddle = self.canvas.create_rectangle(
            560, 160, 575, 240,
            fill="white",
            outline="white"
        )

        self.bola = self.canvas.create_oval(
            100, 180, 120, 200,
            fill="cyan",
            outline="cyan"
        )

        self.dx = 4
        self.dy = 3

        self.kecepatan_paddle = 8
        self.target_y = 200
        self.tombol = set()
        self.game_over = False

        self.root.bind("<KeyPress-Up>", lambda e: self.tombol.add("up"))
        self.root.bind("<KeyRelease-Up>", lambda e: self.tombol.discard("up"))
        self.root.bind("<KeyPress-Down>", lambda e: self.tombol.add("down"))
        self.root.bind("<KeyRelease-Down>", lambda e: self.tombol.discard("down"))

        self.root.bind("<KeyPress-w>", lambda e: self.tombol.add("up"))
        self.root.bind("<KeyRelease-w>", lambda e: self.tombol.discard("up"))
        self.root.bind("<KeyPress-s>", lambda e: self.tombol.add("down"))
        self.root.bind("<KeyRelease-s>", lambda e: self.tombol.discard("down"))
        self.root.bind("<KeyPress-W>", lambda e: self.tombol.add("up"))
        self.root.bind("<KeyRelease-W>", lambda e: self.tombol.discard("up"))
        self.root.bind("<KeyPress-S>", lambda e: self.tombol.add("down"))
        self.root.bind("<KeyRelease-S>", lambda e: self.tombol.discard("down"))

        self.canvas.bind("<Motion>", self.gerak_mouse)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())

        self.root.bind("<r>", self.ulangi)
        self.root.bind("<R>", self.ulangi)

        self.gerakkan_bola()

    def gerak_mouse(self, event):
        self.target_y = max(
            40,
            min(self.tinggi - 40, event.y)
        )

    def gerakkan_paddle(self):
        posisi = self.canvas.coords(self.paddle)
        tengah = (posisi[1] + posisi[3]) / 2

        if "up" in self.tombol:
            self.target_y = max(40, self.target_y - self.kecepatan_paddle)

        if "down" in self.tombol:
            self.target_y = min(360, self.target_y + self.kecepatan_paddle)

        selisih = self.target_y - tengah
        gerakan = selisih * 0.25

        if abs(selisih) < 0.5:
            gerakan = selisih

        self.canvas.move(self.paddle, 0, gerakan)

    def gerakkan_bola(self):
        if self.game_over:
            return

        self.gerakkan_paddle()
        self.canvas.move(self.bola, self.dx, self.dy)

        posisi = self.canvas.coords(self.bola)

        if posisi[1] <= 0:
            self.canvas.move(self.bola, 0, -posisi[1])
            self.dy = abs(self.dy)

        elif posisi[3] >= self.tinggi:
            self.canvas.move(self.bola, 0, self.tinggi - posisi[3])
            self.dy = -abs(self.dy)

        if posisi[0] <= 0:
            self.canvas.move(self.bola, -posisi[0], 0)
            self.dx = abs(self.dx)

        paddle = self.canvas.coords(self.paddle)
        posisi = self.canvas.coords(self.bola)

        if (
            self.dx > 0
            and posisi[2] >= paddle[0]
            and posisi[0] <= paddle[2]
            and posisi[3] >= paddle[1]
            and posisi[1] <= paddle[3]
        ):
            self.canvas.move(
                self.bola,
                paddle[0] - posisi[2],
                0
            )
            self.dx = -abs(self.dx)
            self.skor += 1

            self.canvas.itemconfig(
                self.teks_skor,
                text=f"Skor: {self.skor}"
            )

            if self.skor % 5 == 0:
                self.dx *= 1.1
                self.dy *= 1.1

        posisi = self.canvas.coords(self.bola)

        if posisi[0] >= self.lebar:
            self.game_over = True

            self.canvas.create_text(
                300, 170,
                text="GAME OVER",
                fill="red",
                font=("Arial", 28, "bold")
            )

            self.canvas.create_text(
                300, 210,
                text=f"Skor akhir: {self.skor}",
                fill="white",
                font=("Arial", 16)
            )

            self.canvas.create_text(
                300, 245,
                text="Tekan R untuk bermain lagi",
                fill="yellow",
                font=("Arial", 12)
            )
            return

        self.root.after(16, self.gerakkan_bola)

    def ulangi(self, event):
        if not self.game_over:
            return

        self.canvas.delete("all")

        self.skor = 0
        self.game_over = False
        self.target_y = 200
        self.tombol.clear()

        self.canvas.create_text(
            300, 20,
            text="PINGPONG",
            fill="white",
            font=("Arial", 16, "bold")
        )

        self.teks_skor = self.canvas.create_text(
            300, 50,
            text="Skor: 0",
            fill="white",
            font=("Arial", 14)
        )

        self.paddle = self.canvas.create_rectangle(
            560, 160, 575, 240,
            fill="white",
            outline="white"
        )

        self.bola = self.canvas.create_oval(
            100, 180, 120, 200,
            fill="cyan",
            outline="cyan"
        )

        self.dx = 4
        self.dy = random.choice([-3, 3])

        self.gerakkan_bola()


if __name__ == "__main__":
    root = tkinter.Tk()
    app = AnimasiApp(root)
    root.mainloop()