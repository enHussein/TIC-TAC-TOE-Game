import tkinter as tk
import time
import random
from functools import partial

class TIC_TAC_TOE:
    def __init__(self, root):
        self.root = root
        self.root.title("TIC TAC TOE")
        for i in range(3):
            self.root.rowconfigure(i, minsize=50)
        for i in range(3):
            self.root.columnconfigure(i, minsize=50)
        self.player_symbol = "X"
        self.computer_symbol = "O"
        self.player_wins = 0
        self.computer_wins = 0

        label_font = ("Helvetica", 16)

        self.player_display = tk.Label(root, text="YOU WINS: ", font=label_font)
        self.player_display.grid(row=0, column=0, padx=20, pady=10, sticky="we")

        self.computer_display = tk.Label(root, text="COMPUTER WINS: ", font=label_font)
        self.computer_display.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        get_text_button = tk.Button(root, text="Restart", font=label_font, command=self.restart_game)
        get_text_button.grid(row=2, column=1, padx=0, pady=0, sticky="w")

        self.win_label = tk.Label(root, text="", font=label_font)
        self.win_label.grid(row=1, column=1, padx=0, pady=0, sticky="w")

        self.playboard_frame = tk.Frame(root)
        self.playboard_frame.grid(row=3, column=0, columnspan=3, sticky="we")

        self.buttons = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]

        self.current_player = self.player_symbol

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.playboard_frame, text="", font=label_font, width=6, height=3,
                                              command=partial(self.on_button_click, i, j), borderwidth=0, relief="flat")
                self.buttons[i][j].grid(row=i, column=j, padx=1, pady=1, sticky="we")

        self.playboard_frame.columnconfigure((0, 1, 2), weight=1)
        self.restart_game()

    def on_button_click(self, row, col):
        button = self.buttons[row][col]
        if not button["text"]:
            button.config(text=self.current_player,background="blue" if self.current_player == self.player_symbol else "red")
            if self.check_winner(self.current_player):
                if self.current_player == self.player_symbol:
                    self.player_wins += 1
                else:
                    self.computer_wins += 1
                self.update_display()
                winner_message = f"{self.current_player} Wins!"
                self.show_winner_message(winner_message)
                self.root.after(2000, self.restart_game)  # Wait for 2 seconds before resetting the game
            elif self.is_board_full():
                self.show_winner_message("It's a draw!")
                self.root.after(2000, self.restart_game)  # Wait for 2 seconds before resetting the game
            else:
                self.current_player = self.computer_symbol if self.current_player == self.player_symbol else self.player_symbol
                self.toggle_board_color()

    def toggle_board_color(self):
        current_color = self.playboard_frame["background"]
        new_color = "black" if current_color == "black" else "black"
        self.playboard_frame.config(background=new_color)

    def computer_move(self):
        available_moves = [(i, j) for i in range(3) for j in range(3) if not self.buttons[i][j]["text"]]
        if available_moves:
            row, col = random.choice(available_moves)
            self.buttons[row][col].config(text=self.computer_symbol)
            if self.check_winner(self.computer_symbol):
                self.computer_wins += 1
                self.update_display()
                winner_message = "Computer Wins!"
                self.show_winner_message(winner_message)
                self.root.after(2000, self.restart_game)  # Wait for 2 seconds before resetting the game
            else:
                self.current_player = self.player_symbol
                self.toggle_board_color()

    def check_winner(self, symbol):
        for i in range(3):
            if all(self.buttons[i][j]["text"] == symbol for j in range(3)) or \
               all(self.buttons[j][i]["text"] == symbol for j in range(3)):
                return True
        if all(self.buttons[i][i]["text"] == symbol for i in range(3)) or \
           all(self.buttons[i][2 - i]["text"] == symbol for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(self.buttons[i][j]["text"] for i in range(3) for j in range(3))

    def restart_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.win_label.config(text="")
        self.current_player = self.player_symbol
        self.playboard_frame.config(background="blue")

    def show_winner_message(self, message):
        self.win_label.config(text=message)

    def update_display(self):
        self.player_display.config(text=f"Player Wins: {self.player_wins}")
        self.computer_display.config(text=f"Computer Wins: {self.computer_wins}")


if __name__ == "__main__":
    root = tk.Tk()
    tic_tac_toe = TIC_TAC_TOE(root)
    root.mainloop()
