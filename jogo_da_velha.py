import tkinter as tk
from tkinter import messagebox
import random

def verificar_vencedor():
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            destacar_vencedor([(i, 0), (i, 1), (i, 2)])
            return buttons[i][0]['text']
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            destacar_vencedor([(0, i), (1, i), (2, i)])
            return buttons[0][i]['text']
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        destacar_vencedor([(0, 0), (1, 1), (2, 2)])
        return buttons[0][0]['text']
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        destacar_vencedor([(0, 2), (1, 1), (2, 0)])
        return buttons[0][2]['text']
    return None

def destacar_vencedor(casas):
    for casa in casas:
        buttons[casa[0]][casa[1]].config(bg='#FFEB3B', fg='black')  # Destaque em amarelo

def verificar_jogada_vencedora(jogador):
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                buttons[i][j]['text'] = jogador
                if verificar_vencedor() == jogador:
                    buttons[i][j]['text'] = ""
                    return (i, j)
                buttons[i][j]['text'] = ""
    return None

def ao_clicar_botao(linha, coluna):
    if buttons[linha][coluna]['text'] == "" and not verificar_vencedor():
        buttons[linha][coluna]['text'] = jogador_atual.get()
        buttons[linha][coluna].config(fg='white')  # Cor do texto dos botões
        vencedor = verificar_vencedor()
        if vencedor:
            messagebox.showinfo("Fim de Jogo", f"{vencedor} ganhou!")
            atualizar_pontuacao(vencedor)
        elif all(buttons[i][j]['text'] != "" for i in range(3) for j in range(3)):
            messagebox.showinfo("Fim de Jogo", "Empate!")
            atualizar_pontuacao("Empate")
        else:
            jogador_atual.set("O" if jogador_atual.get() == "X" else "X")
            if jogador_atual.get() == "O":
                app.after(500, movimento_computador)

def movimento_computador():
    jogada = verificar_jogada_vencedora("O")
    if not jogada:
        jogada = verificar_jogada_vencedora("X")
    if not jogada:
        jogadas_disponiveis = [(i, j) for i in range(3) for j in range(3) if buttons[i][j]['text'] == ""]
        if jogadas_disponiveis:
            jogada = random.choice(jogadas_disponiveis)
    if jogada:
        buttons[jogada[0]][jogada[1]]['text'] = "O"
        buttons[jogada[0]][jogada[1]].config(fg='white')
        vencedor = verificar_vencedor()
        if vencedor:
            messagebox.showinfo("Fim de Jogo", f"{vencedor} ganhou!")
            atualizar_pontuacao(vencedor)
        elif all(buttons[i][j]['text'] != "" for i in range(3) for j in range(3)):
            messagebox.showinfo("Fim de Jogo", "Empate!")
            atualizar_pontuacao("Empate")
        else:
            jogador_atual.set("X")

def atualizar_pontuacao(vencedor):
    global pontuacao_x, pontuacao_o, pontuacao_empate
    if vencedor == "X":
        pontuacao_x += 1
    elif vencedor == "O":
        pontuacao_o += 1
    elif vencedor == "Empate":
        pontuacao_empate += 1
    rotulo_pontuacao.config(text=f"X: {pontuacao_x}  O: {pontuacao_o}  Empates: {pontuacao_empate}")

def reiniciar_jogo():
    for i in range(3):
        for j in range(3):
            buttons[i][j]['text'] = ""
            buttons[i][j].config(bg='black')  # Cor de fundo dos botões
    jogador_atual.set("X")

app = tk.Tk()
app.title("Jogo da Velha")
app.geometry('400x500')
app.configure(bg='#2196F3')  # Cor de fundo azul

jogador_atual = tk.StringVar(value="X")

pontuacao_x = 0
pontuacao_o = 0
pontuacao_empate = 0

rotulo_titulo = tk.Label(app, text="Jogo da Velha", font=('Helvetica', 24, 'bold'), bg='#2196F3', fg='white')
rotulo_titulo.pack(pady=10)

quadro_pontuacao = tk.Frame(app, bg='#2196F3')
quadro_pontuacao.pack(pady=10)

rotulo_pontuacao = tk.Label(quadro_pontuacao, text=f"X: {pontuacao_x}  O: {pontuacao_o}  Empates: {pontuacao_empate}", font=('Helvetica', 18), bg='#2196F3', fg='white')
rotulo_pontuacao.pack()

quadro_botoes = tk.Frame(app, bg='#2196F3')
quadro_botoes.pack()

buttons = [[tk.Button(quadro_botoes, text="", width=6, height=3, font=('Helvetica', 24), bg='black', fg='white', relief='raised', bd=2, command=lambda linha=row, coluna=col: ao_clicar_botao(linha, coluna)) for col in range(3)] for row in range(3)]

for linha in range(3):
    for coluna in range(3):
        buttons[linha][coluna].grid(row=linha, column=coluna, padx=5, pady=5)

botao_reiniciar = tk.Button(app, text="Reiniciar Jogo", font=('Helvetica', 16), bg='#FF5722', fg='white', relief='raised', bd=2, command=reiniciar_jogo)
botao_reiniciar.pack(pady=10)

app.mainloop()
