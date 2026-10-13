import tkinter as tk
import random
import time
import math


class PingpongMonster:
    def __init__(self, root):
        self.root = root
        self.root.title("Pingpong Monster Arcade")
        self.root.resizable(False, False)

        self.width = 700
        self.height = 420
        self.running = False
        self.game_over = False

        self.duration = 60
        self.remaining = 60
        self.score = 0
        self.lives = 3
        self.balls = []
        self.last_shot = 0
        self.last_time = time.monotonic()
        self.target_y = 210
        self.keys = set()
        self.frame_id = None
        self.timer_id = None

        panel = tk.Frame(root, padx=10, pady=8)
        panel.pack(fill="x")

        tk.Label(
            panel, text="MODE:",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=(0, 5))

        self.time_choice = tk.IntVar(value=60)

        for label, value in [
            ("1 Menit", 60),
            ("2 Menit", 120),
            ("5 Menit", 300),
            ("Free Mode", 0)
        ]:
            tk.Radiobutton(
                panel,
                text=label,
                variable=self.time_choice,
                value=value
            ).pack(side="left", padx=2)

        self.start_button = tk.Button(
            panel,
            text="Mulai Game",
            command=self.start_game
        )
        self.start_button.pack(side="right")

        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#0b1020",
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=(0, 10))

        self.canvas.bind("<Motion>", self.mouse_move)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())

        self.root.bind("<KeyPress-Up>", lambda e: self.keys.add("up"))
        self.root.bind("<KeyRelease-Up>", lambda e: self.keys.discard("up"))
        self.root.bind("<KeyPress-Down>", lambda e: self.keys.add("down"))
        self.root.bind("<KeyRelease-Down>", lambda e: self.keys.discard("down"))
        self.root.bind("<KeyPress-w>", lambda e: self.keys.add("up"))
        self.root.bind("<KeyRelease-w>", lambda e: self.keys.discard("up"))
        self.root.bind("<KeyPress-s>", lambda e: self.keys.add("down"))
        self.root.bind("<KeyRelease-s>", lambda e: self.keys.discard("down"))

        self.draw_background()
        self.draw_start_screen()

    def draw_background(self):
        self.canvas.delete("all")

        for x in range(0, self.width, 35):
            self.canvas.create_line(
                x, 0, x, self.height,
                fill="#111b30"
            )

        for y in range(0, self.height, 35):
            self.canvas.create_line(
                0, y, self.width, y,
                fill="#111b30"
            )

        self.draw_goal(15, 35, 82, 100, "GOL ATAS")
        self.draw_goal(15, 320, 82, 385, "GOL BAWAH")

    def draw_goal(self, x1, y1, x2, y2, label):
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#12343c",
            outline="#42e8c3",
            width=3
        )

        for x in range(x1 + 12, x2, 12):
            self.canvas.create_line(
                x, y1 + 3, x, y2 - 3,
                fill="#28616b"
            )

        for y in range(y1 + 12, y2, 12):
            self.canvas.create_line(
                x1 + 3, y, x2 - 3, y,
                fill="#28616b"
            )

        self.canvas.create_text(
            (x1 + x2) / 2, y1 - 10,
            text=label,
            fill="#66f5d5",
            font=("Arial", 7, "bold")
        )

    def draw_monster(self):
        c = self.canvas

        c.create_polygon(
            115, 170, 125, 142, 145, 169,
            fill="#8052db", outline="#c6a8ff", width=2
        )
        c.create_polygon(
            165, 169, 188, 142, 196, 175,
            fill="#8052db", outline="#c6a8ff", width=2
        )

        c.create_oval(
            105, 160, 200, 253,
            fill="#8857df", outline="#d0b5ff", width=3
        )

        c.create_oval(126, 178, 150, 205, fill="white")
        c.create_oval(158, 178, 182, 205, fill="white")
        c.create_oval(135, 186, 145, 198, fill="#172039")
        c.create_oval(166, 186, 176, 198, fill="#172039")

        c.create_arc(
            132, 198, 176, 235,
            start=200, extent=140,
            style="arc", outline="#321a59", width=4
        )

        c.create_oval(
            138, 213, 171, 238,
            fill="#43205e", outline="#d0b5ff", width=2
        )

        c.create_polygon(
            145, 214, 153, 226, 160, 214,
            fill="white"
        )

        c.create_oval(
            180, 211, 204, 235,
            fill="#ff647c", outline="#ffd4dc", width=2
        )

        c.create_text(
            150, 265,
            text="MONSTER",
            fill="#c7a8ff",
            font=("Arial", 10, "bold")
        )

    def draw_start_screen(self):
        self.draw_background()
        self.draw_monster()

        self.canvas.create_text(
            430, 145,
            text="PINGPONG",
            fill="#64ddff",
            font=("Arial", 28, "bold")
        )

        self.canvas.create_text(
            430, 185,
            text="Monster menembakkan bola setiap 5 detik",
            fill="white", font=("Arial", 10)
        )

        self.canvas.create_text(
            430, 215,
            text="Pantulkan bola ke salah satu keranjang",
            fill="#b8c8e8", font=("Arial", 10)
        )

        self.canvas.create_text(
            430, 245,
            text="Bola api memberikan 5 skor bonus!",
            fill="#ff9955", font=("Arial", 11, "bold")
        )

        self.canvas.create_text(
            430, 275,
            text="Gerakkan mouse atau gunakan W / S",
            fill="#b8c8e8", font=("Arial", 9)
        )

    def start_game(self):
        if self.running:
            return

        self.stop_callbacks()

        self.duration = self.time_choice.get()
        self.remaining = self.duration
        self.score = 0
        self.lives = 3
        self.balls = []
        self.keys.clear()
        self.target_y = 210

        now = time.monotonic()
        self.last_shot = now
        self.last_time = now

        self.running = True
        self.game_over = False

        self.draw_background()
        self.draw_monster()

        self.paddle = self.canvas.create_rectangle(
            650, 175, 665, 245,
            fill="#e5f7ff",
            outline="#64ddff",
            width=2
        )

        self.score_text = self.canvas.create_text(
            280, 48,
            text="Skor: 0",
            fill="white",
            font=("Arial", 12, "bold")
        )

        self.time_text = self.canvas.create_text(
            410, 48,
            text="Waktu: 01:00",
            fill="#ffd166",
            font=("Arial", 12, "bold")
        )

        self.lives_text = self.canvas.create_text(
            555, 48,
            text="Nyawa: 3",
            fill="#ff8295",
            font=("Arial", 12, "bold")
        )

        self.start_button.config(text="Sedang Bermain")

        self.timer_tick()
        self.game_loop()

    def mouse_move(self, event):
        self.target_y = max(
            35, min(self.height - 35, event.y)
        )

    def move_paddle(self):
        coords = self.canvas.coords(self.paddle)
        center = (coords[1] + coords[3]) / 2

        if "up" in self.keys:
            self.target_y -= 7

        if "down" in self.keys:
            self.target_y += 7

        self.target_y = max(
            35, min(self.height - 35, self.target_y)
        )

        difference = self.target_y - center
        self.canvas.move(self.paddle, 0, difference * 0.25)

    def shoot_ball(self, bonus=False):
        x = 199
        y = 223

        ball_id = self.canvas.create_oval(
            x - 8, y - 8,
            x + 8, y + 8,
            fill="#ff8c32" if bonus else "#65e5ff",
            outline="#fff0a0" if bonus else "white",
            width=2
        )

        flame_id = None

        if bonus:
            flame_id = self.canvas.create_polygon(
                x - 8, y,
                x - 22, y - 7,
                x - 17, y,
                x - 22, y + 7,
                fill="#ff3b22",
                outline="#ffd166"
            )

        self.balls.append({
            "id": ball_id,
            "flame": flame_id,
            "x": x,
            "y": y,
            "dx": random.uniform(3.5, 4.5),
            "dy": random.uniform(-2.5, 2.5),
            "returned": False,
            "bonus": bonus
        })

    def update_score(self, points):
        old_score = self.score
        self.score += points

        self.canvas.itemconfig(
            self.score_text,
            text=f"Skor: {self.score}"
        )

        # Setiap melewati kelipatan 3 skor,
        # monster menembakkan satu bola bonus.
        old_milestone = old_score // 3
        new_milestone = self.score // 3

        if new_milestone > old_milestone:
            self.shoot_ball(bonus=True)

    def update_ball(self, ball):
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]

        x = ball["x"]
        y = ball["y"]
        radius = 8

        if y <= radius:
            ball["y"] = radius
            ball["dy"] = abs(ball["dy"])

        elif y >= self.height - radius:
            ball["y"] = self.height - radius
            ball["dy"] = -abs(ball["dy"])

        coords = self.canvas.coords(self.paddle)
        px1, py1, px2, py2 = coords

        x = ball["x"]
        y = ball["y"]

        # Bola menabrak paddle.
        if (
            not ball["returned"]
            and ball["dx"] > 0
            and x + radius >= px1
            and x - radius <= px2
            and y + radius >= py1
            and y - radius <= py2
        ):
            ball["x"] = px1 - radius - 1
            ball["dx"] = -abs(ball["dx"])
            ball["returned"] = True

            impact = (
                (y - (py1 + py2) / 2)
                / ((py2 - py1) / 2)
            )

            ball["dy"] += impact * 2.5
            ball["dy"] = max(
                -5.5, min(5.5, ball["dy"])
            )

        # Bola yang dipukul mencapai area keranjang kiri.
        if ball["returned"] and ball["x"] <= 85:
            in_top_goal = (
                35 + radius <= ball["y"] <= 100 - radius
            )

            in_bottom_goal = (
                320 + radius <= ball["y"] <= 385 - radius
            )

            if in_top_goal or in_bottom_goal:
                self.update_score(5 if ball["bonus"] else 1)
                self.remove_ball(ball)
                return False

            # Gagal masuk gol: bola memantul ke kanan.
            ball["x"] = 86
            ball["dx"] = abs(ball["dx"])
            ball["returned"] = False

        # Bola yang lolos dari sisi kanan mengurangi nyawa.
        if not ball["returned"] and ball["x"] >= self.width - radius:
            self.lives -= 1

            self.canvas.itemconfig(
                self.lives_text,
                text=f"Nyawa: {self.lives}"
            )

            self.remove_ball(ball)

            if self.lives <= 0:
                self.end_game("Semua nyawa habis!")

            return False

        x = ball["x"]
        y = ball["y"]

        self.canvas.coords(
            ball["id"],
            x - radius, y - radius,
            x + radius, y + radius
        )

        # Animasi sederhana ekor api pada bola bonus.
        if ball["bonus"] and ball["flame"] is not None:
            flicker = random.randint(4, 10)

            self.canvas.coords(
                ball["flame"],
                x - 7, y,
                x - flicker - 8, y - 7,
                x - flicker, y,
                x - flicker - 8, y + 7
            )

        return True

    def remove_ball(self, ball):
        self.canvas.delete(ball["id"])

        if ball["flame"] is not None:
            self.canvas.delete(ball["flame"])

    def game_loop(self):
        if not self.running:
            return

        now = time.monotonic()

        if now - self.last_shot >= 5:
            self.shoot_ball()
            self.last_shot = now

        self.move_paddle()

        remaining_balls = []

        for ball in self.balls:
            if self.update_ball(ball):
                remaining_balls.append(ball)

            if not self.running:
                break

        self.balls = remaining_balls

        if self.running:
            self.frame_id = self.root.after(
                16, self.game_loop
            )

    def timer_tick(self):
        if not self.running:
            return

        if self.duration == 0:
            self.canvas.itemconfig(
                self.time_text,
                text="Waktu: ∞"
            )

            self.timer_id = self.root.after(
                100, self.timer_tick
            )
            return

        now = time.monotonic()
        elapsed = now - self.last_time

        if elapsed >= 1:
            seconds = int(elapsed)
            self.remaining -= seconds
            self.last_time += seconds

        self.remaining = max(0, self.remaining)

        minutes = self.remaining // 60
        seconds = self.remaining % 60

        self.canvas.itemconfig(
            self.time_text,
            text=f"Waktu: {minutes:02d}:{seconds:02d}"
        )

        if self.remaining <= 0:
            self.end_game("Waktu habis!")
            return

        self.timer_id = self.root.after(
            100, self.timer_tick
        )

    def stop_callbacks(self):
        for callback in (self.frame_id, self.timer_id):
            if callback is not None:
                try:
                    self.root.after_cancel(callback)
                except tk.TclError:
                    pass

        self.frame_id = None
        self.timer_id = None

    def end_game(self, message):
        if not self.running:
            return

        self.running = False
        self.game_over = True
        self.stop_callbacks()

        self.canvas.create_rectangle(
            180, 135, 520, 290,
            fill="#121b32",
            outline="#64ddff",
            width=2
        )

        self.canvas.create_text(
            350, 165,
            text="GAME OVER",
            fill="#ff647c",
            font=("Arial", 24, "bold")
        )

        self.canvas.create_text(
            350, 205,
            text=message,
            fill="white",
            font=("Arial", 12)
        )

        self.canvas.create_text(
            350, 235,
            text=f"Skor akhir: {self.score}",
            fill="#64ddff",
            font=("Arial", 16, "bold")
        )

        self.canvas.create_text(
            350, 265,
            text="Klik Main Lagi untuk bermain kembali",
            fill="#ffd166",
            font=("Arial", 10)
        )

        self.start_button.config(text="Main Lagi")


if __name__ == "__main__":
    root = tk.Tk()
    app = PingpongMonster(root)
    root.mainloop()