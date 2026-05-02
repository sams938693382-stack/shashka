import tkinter as tk
import winsound
import random

SIZE = 8
CELL = 70

class Checkers:
    def __init__(self, root):
        self.root = root
        self.root.title("♟ Shashka O'yini")
        self.root.configure(bg="#1e1e2f")

        self.canvas = tk.Canvas(root, width=SIZE*CELL, height=SIZE*CELL, bg="#1e1e2f", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.btn = tk.Button(root, text="🔄 Refresh", command=self.reset_game,
                             bg="#00ffcc", fg="black", font=("Arial", 12, "bold"))
        self.btn.pack(pady=5)

        self.board = [[None]*SIZE for _ in range(SIZE)]
        self.turn = 'white'
        self.selected = None
        self.game_over = False

        self.draw_board()
        self.init_pieces()
        self.canvas.bind("<Button-1>", self.click)

    def reset_game(self):
        self.board = [[None]*SIZE for _ in range(SIZE)]
        self.turn = 'white'
        self.selected = None
        self.game_over = False
        self.init_pieces()
        self.draw_board()
        self.draw_pieces()

    def play_move_sound(self):
        winsound.Beep(800, 80)

    def play_capture_sound(self):
        winsound.Beep(400, 180)

    def draw_board(self):
        self.canvas.delete("all")

        for r in range(SIZE):
            for c in range(SIZE):
                color = '#3c3f58' if (r+c)%2==0 else '#f0d9b5'
                self.canvas.create_rectangle(c*CELL, r*CELL, (c+1)*CELL, (r+1)*CELL, fill=color, outline="")

        if self.selected:
            r, c = self.selected
            self.canvas.create_rectangle(c*CELL, r*CELL, (c+1)*CELL, (r+1)*CELL, outline="yellow", width=3)

    def init_pieces(self):
        for r in range(3):
            for c in range(SIZE):
                if (r+c)%2==1:
                    self.board[r][c] = ('black', False)
        for r in range(5,8):
            for c in range(SIZE):
                if (r+c)%2==1:
                    self.board[r][c] = ('white', False)
        self.draw_pieces()

    def draw_pieces(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c]:
                    color, king = self.board[r][c]

                    x1 = c*CELL+10
                    y1 = r*CELL+10
                    x2 = (c+1)*CELL-10
                    y2 = (r+1)*CELL-10

                    fill = '#ffffff' if color=='white' else '#000000'
                    outline = '#00ffcc' if color=='white' else '#ff5555'

                    self.canvas.create_oval(x1,y1,x2,y2, fill=fill, outline=outline, width=2)

                    if king:
                        self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                                text="K", fill="gold",
                                                font=("Arial", 16, "bold"))

    def get_piece_moves(self, r, c):
        piece = self.board[r][c]
        if not piece:
            return [], []

        color, king = piece
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        moves = []
        captures = []

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < SIZE and 0 <= nc < SIZE and not self.board[nr][nc]:
                moves.append((nr, nc))

            nr2, nc2 = r + 2*dr, c + 2*dc
            if (0 <= nr2 < SIZE and 0 <= nc2 < SIZE):
                if self.board[nr][nc] and self.board[nr][nc][0] != color and not self.board[nr2][nc2]:
                    captures.append((nr2, nc2))

        return moves, captures

    def check_win(self):
        white = any(p and p[0]=='white' for row in self.board for p in row)
        black = any(p and p[0]=='black' for row in self.board for p in row)

        if not white or not black:
            self.game_over = True
            winner = "White yutdi!" if white else "Black yutdi!"
            self.animate_win(winner)

    def animate_win(self, text):
        self.canvas.delete("all")

        for i in range(40):
            x = random.randint(0, SIZE*CELL)
            y = random.randint(0, SIZE*CELL)
            self.canvas.create_oval(x, y, x+8, y+8, fill=random.choice(['#00ffcc','#ff5555','#ffffff','#ffd700']))

        self.canvas.create_text(SIZE*CELL//2, SIZE*CELL//2,
                                text=text,
                                fill="gold",
                                font=("Arial", 28, "bold"))

    def click(self, event):
        if self.game_over:
            return

        c = event.x // CELL
        r = event.y // CELL

        if self.selected:
            sr, sc = self.selected
            moves, captures = self.get_piece_moves(sr, sc)

            if (r, c) in captures:
                mr, mc = (sr+r)//2, (sc+c)//2
                self.board[mr][mc] = None

                self.board[r][c] = self.board[sr][sc]
                self.board[sr][sc] = None

                self.play_capture_sound()

                color, king = self.board[r][c]
                if color == 'white' and r == 0:
                    self.board[r][c] = (color, True)
                if color == 'black' and r == SIZE-1:
                    self.board[r][c] = (color, True)

                _, new_caps = self.get_piece_moves(r, c)
                if new_caps:
                    self.selected = (r, c)
                    self.draw_board()
                    self.draw_pieces()
                    return

                self.turn = 'black' if self.turn=='white' else 'white'
                self.selected = None

            elif (r, c) in moves:
                self.board[r][c] = self.board[sr][sc]
                self.board[sr][sc] = None

                self.play_move_sound()

                color, king = self.board[r][c]
                if color == 'white' and r == 0:
                    self.board[r][c] = (color, True)
                if color == 'black' and r == SIZE-1:
                    self.board[r][c] = (color, True)

                self.turn = 'black' if self.turn=='white' else 'white'
                self.selected = None

            else:
                self.selected = None

        else:
            if self.board[r][c] and self.board[r][c][0] == self.turn:
                self.selected = (r,c)

        self.draw_board()
        self.draw_pieces()
        self.check_win()

root = tk.Tk()
Checkers(root)
root.mainloop()