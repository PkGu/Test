import tkinter as tk
from tkinter import messagebox
import time
import threading

class ChessClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("체스 시계")
        self.root.geometry("300x500")  # 세로로 길게

        self.time_white = 0
        self.time_black = 0
        self.increment = 0
        self.active_player = 1  # 1: White, 2: Black
        self.running = False
        self.paused = False
        self.lock = threading.Lock()
        self.timer_thread = None

        # 모드 선택 UI
        self.mode_label = tk.Label(root, text="체스 시계 모드를 선택하세요:", font=("Helvetica", 14))
        self.mode_label.pack(pady=(10,5))

        self.mode_var = tk.IntVar(value=1)

        self.radio1 = tk.Radiobutton(root, text="1. 각 선수 10분", variable=self.mode_var, value=1, font=("Helvetica", 12))
        self.radio2 = tk.Radiobutton(root, text="2. 각 선수 90분 + 수마다 30초 추가", variable=self.mode_var, value=2, font=("Helvetica", 12))
        self.radio3 = tk.Radiobutton(root, text="3. 각 선수 3분 + 수마다 2초 추가", variable=self.mode_var, value=3, font=("Helvetica", 12))
        self.radio1.pack(pady=2)
        self.radio2.pack(pady=2)
        self.radio3.pack(pady=2)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=15)

        self.start_button = tk.Button(self.button_frame, text="시작하기", font=("Helvetica", 14), width=8, command=self.start_game)
        self.pause_button = tk.Button(self.button_frame, text="중지", font=("Helvetica", 14), width=8, state="disabled", command=self.toggle_pause)
        self.turn_button = tk.Button(self.button_frame, text="턴 전환", font=("Helvetica", 14), width=8, state="disabled", command=self.switch_turn)

        self.start_button.pack(side="left", padx=8)
        self.pause_button.pack(side="left", padx=8)
        self.turn_button.pack(side="left", padx=8)

        self.white_label = tk.Label(root, text="White", font=("Helvetica", 18))
        self.white_label.pack(pady=(10,0))
        self.white_time_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.white_time_label.pack(pady=(0,20))

        self.black_label = tk.Label(root, text="Black", font=("Helvetica", 18))
        self.black_label.pack(pady=(10,0))
        self.black_time_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.black_time_label.pack(pady=(0,20))

        self.root.bind("<space>", self.space_switch_turn)

        self.update_colors()

    def start_game(self):
        if self.running:
            self.running = False
            if self.timer_thread is not None:
                self.timer_thread.join()

        mode = self.mode_var.get()

        if mode == 1:
            self.time_white = 10 * 60
            self.time_black = 10 * 60
            self.increment = 0
        elif mode == 2:
            self.time_white = 90 * 60  # 90분 = 5400초
            self.time_black = 90 * 60
            self.increment = 30
        elif mode == 3:
            self.time_white = 3 * 60
            self.time_black = 3 * 60
            self.increment = 2

        self.active_player = 1
        self.running = True
        self.paused = False

        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal", text="중지")
        self.turn_button.config(state="normal")

        self.update_timer_label()
        self.update_colors()

        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def toggle_pause(self):
        if not self.running:
            return
        with self.lock:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.config(text="재개")
                self.turn_button.config(state="disabled")
                self.start_button.config(state="normal")
            else:
                self.pause_button.config(text="중지")
                self.turn_button.config(state="normal")
                self.start_button.config(state="disabled")

    def format_time(self, seconds):
        if seconds < 0:
            seconds = 0
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def switch_turn(self):
        if not self.running or self.paused:
            return
        with self.lock:
            if self.increment > 0:
                if self.active_player == 1:
                    self.time_white += self.increment
                else:
                    self.time_black += self.increment

            self.active_player = 2 if self.active_player == 1 else 1

        self.update_colors()

    def space_switch_turn(self, event):
        self.switch_turn()

    def run_timer(self):
        last_time = time.time()
        while self.running:
            time.sleep(0.05)
            with self.lock:
                if self.paused:
                    last_time = time.time()
                    continue

                now = time.time()
                elapsed = now - last_time
                last_time = now

                if self.active_player == 1:
                    self.time_white -= elapsed
                    if self.time_white <= 0:
                        self.running = False
                        self.show_winner("Black")
                else:
                    self.time_black -= elapsed
                    if self.time_black <= 0:
                        self.running = False
                        self.show_winner("White")

            self.update_timer_label()

    def update_timer_label(self):
        white_str = self.format_time(self.time_white)
        black_str = self.format_time(self.time_black)

        self.root.after(0, lambda: self.white_time_label.config(text=white_str))
        self.root.after(0, lambda: self.black_time_label.config(text=black_str))

    def update_colors(self):
        if self.active_player == 1:
            bg_color = "white"
            fg_color = "black"
            label_fg_inactive = "gray"
            btn_bg = "lightgray"
        else:
            bg_color = "black"
            fg_color = "white"
            label_fg_inactive = "gray"
            btn_bg = "gray"

        self.root.configure(bg=bg_color)

        for rb in [self.radio1, self.radio2, self.radio3]:
            rb.configure(bg=bg_color, fg=fg_color, selectcolor=bg_color, activebackground=bg_color, activeforeground=fg_color)

        self.mode_label.configure(bg=bg_color, fg=fg_color)

        self.button_frame.configure(bg=bg_color)
        for btn in [self.start_button, self.pause_button, self.turn_button]:
            btn.configure(bg=btn_bg, fg=fg_color, activebackground=btn_bg, activeforeground=fg_color, highlightthickness=0, bd=1)

        self.white_label.configure(bg=bg_color, fg=fg_color if self.active_player == 1 else label_fg_inactive)
        self.white_time_label.configure(bg=bg_color, fg=fg_color if self.active_player == 1 else label_fg_inactive)

        self.black_label.configure(bg=bg_color, fg=fg_color if self.active_player == 2 else label_fg_inactive)
        self.black_time_label.configure(bg=bg_color, fg=fg_color if self.active_player == 2 else label_fg_inactive)

    def show_winner(self, winner):
        def popup():
            messagebox.showinfo("게임 종료", f"{winner} 승리! 상대방 시간 초과")
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled", text="중지")
            self.turn_button.config(state="disabled")
            self.time_white = 0
            self.time_black = 0
            self.update_timer_label()
        self.root.after(0, popup)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessClockGUI(root)
    root.mainloop()
