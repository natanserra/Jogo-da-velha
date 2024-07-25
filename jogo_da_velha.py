import tkinter as tk
from tkinter import messagebox
import random

def check_winner():
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            highlight_winner([(i, 0), (i, 1), (i, 2)])
            return buttons[i][0]['text']
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            highlight_winner([(0, i), (1, i), (2, i)])
            return buttons[0][i]['text']
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        highlight_winner([(0, 0), (1, 1), (2, 2)])
        return buttons[0][0]['text']
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        highlight_winner([(0, 2), (1, 1), (2, 0)])
        return buttons[0][2]['text']
    return None

def highlight_winner(cells):
    for cell in cells:
        buttons[cell[0]][cell[1]].config(bg='#FFEB3B', fg='black')  # Destaque em amarelo

def check_winning_move(player):
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                buttons[i][j]['text'] = player
                if check_winner() == player:
                    buttons[i][j]['text'] = ""
                    return (i, j)
                buttons[i][j]['text'] = ""
    return None

def on_button_click(row, col):
    if buttons[row][col]['text'] == "" and not check_winner():
        buttons[row][col]['text'] = current_player.get()
        buttons[row][col].config(fg='blue' if current_player.get() == 'X' else 'red')
        winner = check_winner()
        if winner:
            messagebox.showinfo("Fim de Jogo", f"{winner} ganhou!")
            update_score(winner)
        elif all(buttons[i][j]['text'] != "" for i in range(3) for j in range(3)):
            messagebox.showinfo("Fim de Jogo", "Empate!")
            update_score("Empate")
        else:
            current_player.set("O" if current_player.get() == "X" else "X")
            if current_player.get() == "O":
                app.after(500, computer_move)

def computer_move():
    move = check_winning_move("O")
    if not move:
        move = check_winning_move("X")
    if not move:
        available_moves = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]['text'] == ""]
        if available_moves:
            move = random.choice(available_moves)
    if move:
        buttons[move[0]][move[1]]['text'] = "O"
        buttons[move[0]][move[1]].config(fg='red')
        winner = check_winner()
        if winner:
            messagebox.showinfo("Fim de Jogo", f"{winner} ganhou!")
            update_score(winner)
        elif all(buttons[i][j]['text'] != "" for i in range(3) for j in range(3)):
            messagebox.showinfo("Fim de Jogo", "Empate!")
            update_score("Empate")
        else:
            current_player.set("X")

def update_score(winner):
    global score_x, score_o, score_draw
    if winner == "X":
        score_x += 1
    elif winner == "O":
        score_o += 1
    elif winner == "Empate":
        score_draw += 1
    score_label.config(text=f"X: {score_x}  O: {score_o}  Empates: {score_draw}")

def reset_game():
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ""
            buttons[i][j].config(bg='#B0BEC5')  # Cor de fundo cinza claro
    current_player.set("X")

app = tk.Tk()
app.title("Jogo da Velha")
app.geometry('400x500')
app.configure(bg='#E0F7FA')  # Cor de fundo azul claro

current_player = tk.StringVar(value="X")

score_x = 0
score_o = 0
score_draw = 0

title_label = tk.Label(app, text="Jogo da Velha", font=('Helvetica', 24, 'bold'), bg='#E0F7FA', fg='#00796B')
title_label.pack(pady=10)

score_frame = tk.Frame(app, bg='#E0F7FA')
score_frame.pack(pady=10)

score_label = tk.Label(score_frame, text=f"X: {score_x}  O: {score_o}  Empates: {score_draw}", font=('Helvetica', 18), bg='#E0F7FA', fg='#00796B')
score_label.pack()

buttons_frame = tk.Frame(app, bg='#E0F7FA')
buttons_frame.pack()

buttons = [[tk.Button(buttons_frame, text="", width=6, height=3, font=('Helvetica', 24), bg='#B0BEC5', fg='black', relief='raised', bd=2, command=lambda row=row, col=col: on_button_click(row, col)) for col in range(3)] for row in range(3)]

for row in range(3):
    for col in range(3):
        buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

reset_button = tk.Button(app, text="Reiniciar Jogo", font=('Helvetica', 16), bg='#FF5722', fg='white', relief='raised', bd=2, command=reset_game)
reset_button.pack(pady=10)

app.mainloop()
