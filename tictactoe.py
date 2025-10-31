import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")

        self.current = "X"               # current player: "X" or "O"
        self.board = [""] * 9            # 0..8 positions
        self.buttons = [None] * 9
        self.scores = {"X": 0, "O": 0, "Draws": 0}

        self.create_ui()

    def create_ui(self):
        # top frame for scoreboard and reset
        top = tk.Frame(self.root)
        top.pack(padx=10, pady=8)

        self.info_label = tk.Label(top, text=f"Turn: {self.current}", font=("Helvetica", 14))
        self.info_label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.score_label = tk.Label(top, text=self.score_text(), font=("Helvetica", 12))
        self.score_label.grid(row=1, column=0, columnspan=2, sticky="w")

        reset_btn = tk.Button(top, text="Reset Board", command=self.reset_board)
        reset_btn.grid(row=0, column=2, rowspan=2, padx=(10,0))

        # board frame
        board_frame = tk.Frame(self.root)
        board_frame.pack(padx=10, pady=6)

        for i in range(9):
            btn = tk.Button(board_frame, text="", font=("Helvetica", 24), width=5, height=2,
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons[i] = btn

    def score_text(self):
        return f"Scores — X: {self.scores['X']}   O: {self.scores['O']}   Draws: {self.scores['Draws']}"

    def on_click(self, idx):
        if self.board[idx] != "":
            return  # already occupied

        # mark
        self.board[idx] = self.current
        self.buttons[idx].config(text=self.current, disabledforeground="black")
        self.buttons[idx]["state"] = "disabled"

        winner, win_line = self.check_winner()
        if winner:
            self.handle_win(winner, win_line)
            return

        if all(cell != "" for cell in self.board):
            # draw
            self.scores["Draws"] += 1
            self.score_label.config(text=self.score_text())
            messagebox.showinfo("Draw", "The game is a draw.")
            self.disable_all_buttons()
            return

        # switch player
        self.current = "O" if self.current == "X" else "X"
        self.info_label.config(text=f"Turn: {self.current}")

    def check_winner(self):
        # returns (winner_symbol or None, winning_line_indices or None)
        lines = [
            (0,1,2), (3,4,5), (6,7,8),  # rows
            (0,3,6), (1,4,7), (2,5,8),  # cols
            (0,4,8), (2,4,6)            # diagonals
        ]
        for a,b,c in lines:
            if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], (a,b,c)
        return None, None

    def handle_win(self, winner, win_line):
        # highlight winning buttons
        for i in win_line:
            self.buttons[i].config(bg="lightgreen")
        self.scores[winner] += 1
        self.score_label.config(text=self.score_text())
        messagebox.showinfo("Winner", f"Player {winner} wins!")
        self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn["state"] = "disabled"

    def reset_board(self):
        # clear board for next round (keep scores)
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", state="normal", bg=self.root.cget("bg"))
        # X always starts new round (optional — you can alternate if you prefer)
        self.current = "X"
        self.info_label.config(text=f"Turn: {self.current}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
