import random
import numpy as np
from Gymsys_manager import *
import matplotlib.pyplot as plt
from Gymsys_Ga import *
import time

# Algoritmo Genético:
def teste_algoritmo_genetico():  
    start_time = time.process_time()
    melhor_individuo = algoritmo_genetico(num_generacoes, tam_populacao, espaco_solucao, taxa_mutacao)
    print("Melhor indivíduo: ")
    imprimir(melhor_individuo)
    print(f"Fitness do melhor indivíduo: {funcao_fitness(melhor_individuo)}")
    print("tempo de execução:")
    print(time.process_time() - start_time, "segundos")


# Crossover um ponto:
def teste_crossover_um_ponto():
    solucao1 = criar_individuo(espaco_solucao)
    solucao2 = criar_individuo(espaco_solucao)
    imprimir(solucao1)
    print()
    imprimir(solucao2)
    print()
    print("filhos:")
    filho1, filho2 = crossover_um_ponto(solucao1, solucao2, espaco_solucao)
    imprimir(filho1)
    print()
    imprimir(filho2)

    print("primeiros 2 alunos: ")
    print(espaco_solucao[0])
    print()
    print(espaco_solucao[1])
    print()
    print("últimos 2 alunos: (1º penúltimo 2º último)")
    print(espaco_solucao[(len(espaco_solucao))-2])
    print()
    print(espaco_solucao[(len(espaco_solucao))-1])

# Crossover entrelaçado:
def teste_crossover_entrelacado():
    solucao1 = criar_individuo(espaco_solucao)
    solucao2 = criar_individuo(espaco_solucao)
    imprimir(solucao1)
    print()
    imprimir(solucao2)
    print("filhos:")
    filho1, filho2 = crossover_entrelacado(solucao1, solucao2, espaco_solucao)
    imprimir(filho1)
    print()
    imprimir(filho2)
    print()
    print("fitness parente 1: ")
    print(funcao_fitness(solucao1))
    print()
    print("fitness parente 2: ")
    print(funcao_fitness(solucao2))
    print()
    print("fitness filho 1: ")
    print(funcao_fitness(filho1))
    print()
    print("fitness filho2: ")
    print(funcao_fitness(filho2))
    print("primeiros 4 alunos: ")
    print(espaco_solucao[0])
    print()
    print(espaco_solucao[1])
    print()
    print(espaco_solucao[2])
    print()
    print(espaco_solucao[3])

# Mutacao:
def teste_mutacao():
    solucao1 = criar_individuo(gerar_alunos())
    imprimir(solucao1)
    print()
    solucao1 = mutacao(solucao1, 1)
    imprimir(solucao1)

#def teste_repescagem():

teste_algoritmo_genetico()