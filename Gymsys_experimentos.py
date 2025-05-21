import threading
import threading
import tkinter as tk
import matplotlib.pyplot as plt
from Gymsys_manager import gerar_alunos
from Gymsys_Ga import algoritmo_genetico
from Gymsys_simulacao import simulacao_individuo
from Gymsys_greedy import algoritmo_guloso

# Parametros
num_generacoes = 200
tam_populacao = 50
espaco_solucao = gerar_alunos()  # Lista de alunos a serem agendados
taxa_mutacao = 0.2
elitismo = 2
peso_descarte = 500 # Peso da penalidade por aluno descartado

def iniciar_simulacao(funcao_simulacao, individuo_solucao):
    canvas_holder_ready = {
        "canvas": None,
        "ready": threading.Event()
    }

    def gui_thread():
        window = tk.Tk()
        window.title("Academia Gymsys")

        canvas = tk.Canvas(window, width=1200, height=400, bg="white")
        canvas.pack()

        canvas_holder_ready["canvas"] = canvas
        canvas_holder_ready["ready"].set()

        window.mainloop()

    threading.Thread(target=gui_thread, daemon=True).start()

    # Espera o canvas estar pronto
    canvas_holder_ready["ready"].wait()

    # Pega o canvas e chama a simulação
    canvas = canvas_holder_ready["canvas"]
    espera_total = funcao_simulacao(canvas, individuo_solucao)
    return espera_total

resultados_gen1 = []
resultados_gen100 = []
resultados_greedy = []
espaco_solucao = gerar_alunos()
individuo1, individuo200 = algoritmo_genetico(num_generacoes, tam_populacao, espaco_solucao, taxa_mutacao, elitismo)
individuo_greedy = algoritmo_guloso(espaco_solucao)
resultados_gen1.append(iniciar_simulacao(simulacao_individuo, individuo1))
resultados_gen100.append(iniciar_simulacao(simulacao_individuo, individuo200))
resultados_greedy.append(iniciar_simulacao(simulacao_individuo, individuo_greedy))
print("Resultados da simulação para o primeiro indivíduo:")
print(resultados_gen1)
print("Resultados da simulação para o último indivíduo:")
print(resultados_gen100)
print("Resultados da simulação para o indivíduo gerado pelo algoritmo guloso:")
print(resultados_greedy)