import tkinter as tk
import random

class AdvancedTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Vijay's Tic Tac Toe")
        self.root.geometry("420x680")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        # Game state
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current = "X"
        self.game_over = False

        # Modes
        self.vs_ai = True
        self.difficulty = "Hard"

        # Scoreboard
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0

        # Colors
        self.bg = "#0f172a"
        self.card = "#1e293b"
        self.btn = "#334155"
        self.hover = "#475569"
        self.accent = "#22c55e"
        self.win = "#facc15"

        # TITLE
        self.title = tk.Label(root, text="Vijay's Tic Tac Toe",
                              font=("Segoe UI", 22, "bold"),
                              bg=self.bg, fg="white")
        self.title.pack(pady=10)

        # SCOREBOARD
        score_frame = tk.Frame(root, bg=self.bg)
        score_frame.pack()

        self.score_label = tk.Label(
            score_frame,
            text="X: 0   O: 0   Draw: 0",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg,
            fg="#cbd5f5"
        )
        self.score_label.pack()

        # CONTROLS
        control = tk.Frame(root, bg=self.bg)
        control.pack(pady=5)

        self.mode_btn = tk.Button(control, text="Mode: AI",
                                 command=self.toggle_mode,
                                 bg=self.accent, fg="black")
        self.mode_btn.grid(row=0, column=0, padx=5)

        self.diff_btn = tk.Button(control, text="Difficulty: Hard",
                                 command=self.change_difficulty,
                                 bg=self.accent, fg="black")
        self.diff_btn.grid(row=0, column=1, padx=5)

        # CARD
        self.card_frame = tk.Frame(root, bg=self.card)
        self.card_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # BOARD
        self.board_frame = tk.Frame(self.card_frame, bg=self.card)
        self.board_frame.pack(pady=20)

        self.buttons = [[None]*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                btn = tk.Label(
                    self.board_frame,
                    text="",
                    font=("Segoe UI", 32, "bold"),
                    width=4, height=2,
                    bg=self.btn, fg="white"
                )
                btn.grid(row=i, column=j, padx=6, pady=6)

                btn.bind("<Button-1>", lambda e, r=i, c=j: self.play(r, c))
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.hover))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.btn))

                self.buttons[i][j] = btn

        # STATUS
        self.status = tk.Label(self.card_frame,
                               text="Turn: X",
                               font=("Segoe UI", 14),
                               bg=self.card, fg="#cbd5f5")
        self.status.pack(pady=10)

        # BUTTONS
        btn_frame = tk.Frame(root, bg=self.bg)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Restart",
                  bg=self.accent, fg="black",
                  command=self.restart).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Reset Score",
                  bg="#ef4444", fg="white",
                  command=self.reset_score).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Reset Game",
                  bg="#f97316", fg="white",
                  command=self.reset_all).grid(row=0, column=2, padx=5)

    # GAME
    def play(self, r, c):
        if self.game_over or self.board[r][c] != "":
            return

        self.animate_click(r, c)
        self.place(r, c, self.current)

        if self.check_game():
            return

        self.switch_player()

        if self.vs_ai and self.current == "O":
            self.root.after(400, self.ai_move)

    def place(self, r, c, player):
        self.board[r][c] = player
        self.buttons[r][c].config(text=player)

    def switch_player(self):
        self.current = "O" if self.current == "X" else "X"
        self.status.config(text=f"Turn: {self.current}")

    # AI
    def ai_move(self):
        if self.difficulty == "Easy":
            move = self.random_move()
        elif self.difficulty == "Medium":
            move = self.best_move() if random.random() > 0.5 else self.random_move()
        else:
            move = self.best_move()

        if move:
            self.animate_click(move[0], move[1])
            self.place(move[0], move[1], "O")

        if not self.check_game():
            self.switch_player()

    def random_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty) if empty else None

    def best_move(self):
        best_score = -999
        move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, is_max):
        winner = self.get_winner()
        if winner == "O": return 1
        if winner == "X": return -1
        if self.is_full(): return 0

        if is_max:
            best = -999
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        best = max(best, self.minimax(False))
                        self.board[i][j] = ""
            return best
        else:
            best = 999
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        best = min(best, self.minimax(True))
                        self.board[i][j] = ""
            return best

    # LOGIC
    def get_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != "": return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != "": return b[0][i]
        if b[0][0] == b[1][1] == b[2][2] != "": return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != "": return b[0][2]
        return None

    def is_full(self):
        return all(cell != "" for row in self.board for cell in row)

    def check_game(self):
        winner = self.get_winner()

        if winner:
            self.status.config(text=f"{winner} Wins!", fg=self.win)
            self.update_score(winner)
            self.animate_win(winner)
            self.game_over = True
            return True

        if self.is_full():
            self.status.config(text="It's a Tie!", fg=self.win)
            self.score_draw += 1
            self.update_score_label()
            self.game_over = True
            return True

        return False

    # SCORE
    def update_score(self, winner):
        if winner == "X":
            self.score_x += 1
        else:
            self.score_o += 1
        self.update_score_label()

    def update_score_label(self):
        self.score_label.config(
            text=f"X: {self.score_x}   O: {self.score_o}   Draw: {self.score_draw}"
        )

    def reset_score(self):
        self.score_x = self.score_o = self.score_draw = 0
        self.update_score_label()

    def reset_all(self):
        self.reset_score()
        self.restart()

    # ANIMATIONS
    def animate_click(self, r, c):
        self.buttons[r][c].config(bg=self.accent)
        self.root.after(120, lambda: self.buttons[r][c].config(bg=self.btn))

    def animate_win(self, player):
        for _ in range(3):
            self.root.after(200, lambda: self.highlight(player))
            self.root.after(400, lambda: self.reset_colors())

    def highlight(self, player):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == player:
                    self.buttons[i][j].config(bg=self.win)

    def reset_colors(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(bg=self.btn)

    # CONTROLS
    def toggle_mode(self):
        self.vs_ai = not self.vs_ai
        self.mode_btn.config(text="Mode: AI" if self.vs_ai else "Mode: 2 Player")
        self.restart()

    def change_difficulty(self):
        levels = ["Easy", "Medium", "Hard"]
        i = levels.index(self.difficulty)
        self.difficulty = levels[(i+1) % 3]
        self.diff_btn.config(text=f"Difficulty: {self.difficulty}")

    def restart(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current = "X"
        self.game_over = False
        self.status.config(text="Turn: X", fg="white")

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg=self.btn)


# RUN
root = tk.Tk()
app = AdvancedTicTacToe(root)
root.mainloop()