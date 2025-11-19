import tkinter as tk
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("1000x800")
root.configure(background="#5d615e")
animation_job=[None]
#title
title = tk.Label(root, text="TIC TAC TOE",
                 font=("Arial", 30, "bold"),
                 bg="#5d615e", fg="#064439"
)
title.pack(pady=(20, 5))

#status (winner)
status = tk.Label(root, text="Turn: X",
                  font=("Arial", 20, "bold"),
                  bg="#5d615e", fg="#0a2f2b")
status.pack(pady=(0, 15))

#game box
box = tk.Frame(root, bg="white", bd=7, relief=tk.SOLID)
box.place(relx=0.5, rely=0.52, anchor="center", width=800, height=600
)
box.pack_propagate(False)

#current game state
current_player = ["X"]


def check_winner():
    board = [[buttons[r][c]["text"] for c in range(3)] for r in range(3)]

    wins = [
        # rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        # columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        # diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for line in wins:
        a, b, c = line
        if (
            board[a[0]][a[1]] != "" and
            board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]]
        ):
            return board[a[0]][a[1]], line
        
    if all(board[r][c]!="" for r in range(3) for c in range(3)):
        return "Draw",None

    return None, None


def highlight_line(line_coords):
    # winning cells
    for (r, c) in line_coords:
        buttons[r][c].config(bg="#b9ffd0")

    # dim the rest
    for r in range(3):
        for c in range(3):
            if (r, c) not in line_coords:
                buttons[r][c].config(bg="#e3f9ef"
)

#disable board
def disable_board():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(state="disabled")

#reset board
def reset_board():
    if animation_job[0] is not None:
        root.after_cancel(animation_job[0])
        animation_job[0]=None
    current_player[0]="X"
    status.config(text="Turn: X")

    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="",bg="lightgrey",fg="black",state="normal")

#to show the win
def animate_win(line_coords,step=0):
    colors=["#ffd27f", "#ffe9b3"]
    current_color=colors[step%len(colors)]

    for (r,c) in line_coords:
        buttons[r][c].config(bg=current_color)

    job=root.after(300,lambda: animate_win(line_coords,step+1))
    animation_job[0]=job

def on_click(btn):
    if btn["text"] == "":
        btn["text"] = current_player[0]
        btn["fg"] = ("#2a6fdb" if current_player[0] == "X" else "#d64545")
        #Draw Case
        winner, line = check_winner()
        if winner=="Draw":
            status.config(text="It's a Draw!fuhhh🥀")
            disable_board()
            for r in range(3):
                for c in range(3):
                    buttons[r][c].config(bg="#e3f9ef")
            return 
        #Win Case
        if winner:
            status.config(text=f"Winner is: {winner}")
            highlight_line(line)
            disable_board()
            animate_win(line)
            return

        # Switch player turn
        current_player[0] = "O" if current_player[0] == "X" else "X"
        status.config(text=f"Turn: {current_player[0]}")


#box creation
buttons = [[None for _ in range(3)] for _ in range(3)]

for row in range(3):
    box.rowconfigure(row, weight=1)
    for col in range(3):
        box.columnconfigure(col, weight=1)
        btn = tk.Button(box, text="",
                        font=("Arial", 48, "bold"),
                        bg="lightgrey", bd=2, relief=tk.SOLID)
        btn.grid(row=row, column=col, sticky="nsew")
        btn.config(command=lambda b=btn: on_click(b))
        buttons[row][col] = btn

reset_btn=tk.Button(root,text="Play Again",font=("Arial",18,"bold"),bg="#e8fff4",fg="#1e3b2f",bd=4,relief=tk.RAISED,command=lambda: reset_board())
reset_btn.place(relx=0.5,rely=0.95,anchor="center")

root.mainloop()