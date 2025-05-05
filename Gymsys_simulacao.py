import threading
import random
import time
import tkinter as tk
from Gymsys_manager import *
from Gymsys_Ga import *
from Gymsys_render import *

#Lista do tempo necessário para realizar o treino em cada máquina
tempo_maquinas = [0.3, 0.3, 0.4, 0.4, 0.5, 0.5, 0.7, 1.0, 1.2, 1.5]

shared_data = {
    "espera_total": 0,  # Tempo de espera total dos alunos
    "mutex": threading.Lock()  # Mutex para acesso concorrente a shared_data
    }

def criar_maquinas(canvas):
    """
    Cria uma lista de semáforos com os valores especificados
    """
    max_permits = [1, 1, 1, 1, 1, 1, 2, 3, 3, 5]
    maquinas = [VisualSemaphore(canvas, 50 + i * 200, 100, max_permits=permits, machine_id=i) 
                for i, permits in enumerate(max_permits)]
    return maquinas


def simulacao_horario(canvas, alunos_horario, shared_data):
    """
    Realiza a simulação de uma lista de alunos em um horário
    """
    print(f"Alunos: {len(alunos_horario)}")

    # Create a list to hold the thread objects
    threads = []

    # Cria uma lista de máquinas para representar as máquinas da academia.
    maquinas = criar_maquinas(canvas)

    # Update the canvas size after creating the machines
    update_canvas_size(maquinas, canvas)

    # Create up to 20 threads
    for i in range(0, len(alunos_horario)):
        thread = threading.Thread(target=treino, args=(alunos_horario[i], i, maquinas, shared_data, canvas))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    print("Todos os alunos terminaram de treinar!")

def simulacao_individuo(canvas, individuo):
    """
    Realiza a simulação da solução representada por um indivíduo
    """
    global shared_data
    # Realiza a simulação para todos os horários do indivíduo
    # Simulações não são feitas em paralelo para evitar gargalos que podem afetar o tempo de espera.
    for i in range(0, len(individuo)-1):
        canvas.delete("clear")  # Limpa o canvas antes de cada simulação
        simulacao_horario(canvas, individuo[i], shared_data)  # shared_data é passada para cada simulação

    return shared_data["espera_total"]  # Retorna o tempo total de espera dos alunos

def iniciar_simulacao(canvas, solucao):
    """
    Limpa o Canvas e inicia a simulação
    """
    # Inicia a simulação
    return simulacao_individuo(canvas, solucao)


def calcular_tempo_treino(aluno):
    """
    Calcula o tempo total de treino de um aluno com base nas máquinas em seu treino
    """

    tempo_total = 0
    for i in range(0, len(aluno[1])):
        tempo_total += tempo_maquinas[aluno[1][i]]
    return tempo_total

def treino(aluno, id, maquinas, shared_data, canvas):
    """
    Função que simula a realização de um treino por um aluno
    """
    tempo_treinando = calcular_tempo_treino(aluno) # Calculate the total training time for the student
    print(f"Treino do aluno {id}: {aluno[1]}")

    try:
        print(f"O aluno {id} veio treinar!")
        tempo_inicial = time.time() # Record the start time
        while aluno[1]:  # Iterate over the machines the student wants to use
            if not aluno[1]:  # Check if the list is empty
                break  # Exit the loop if the list is empty
            semaphore = maquinas[aluno[1][0]]  # Get the semaphore for the machine the student wants to use
            index = aluno[1][0]  # Get the index of the machine the student wants to use
            if semaphore.acquire(id):  # Pass thread id to acquire
                # Simulate some work being done
                time.sleep(tempo_maquinas[index])  # Simulate the time taken to train
                semaphore.release()
                print(f"O aluno {id} terminou de usar a máquina {index}!")
                aluno[1].pop(0)  # Remove the machine from the list of machines used by the student
            else:
                print(f"A máquina {index} está ocupada! O aluno {id} não pode usá-la agora.")
                aluno[1].append(aluno[1][0])  # Re-add the machine to the list of machines used by the student
                aluno[1].pop(0)  # Remove the machine from the list of machines used by the student
        print(f"O aluno {id} terminou de treinar!")
        tempo_final = time.time()  # Record the end time
        print(f"Tempo inicial do aluno {id}: {tempo_inicial} ms")
        print(f"Tempo final do aluno {id}: {tempo_final} ms")
        print(f"Tempo total do aluno {id}: {tempo_final - tempo_inicial} ms")
        print(f"Tempo de treino do aluno {id}: {tempo_treinando} ms")
        tempo_espera = (tempo_final - tempo_inicial) - tempo_treinando # Calculando o tempo de espera total do aluno
        print(f"Tempo de espera do aluno {id}: {tempo_espera} ms")
        shared_data["mutex"].acquire()  # Acquire the lock
        shared_data["espera_total"] += tempo_espera
        print(f"Tempo de espera acumulado atual: {shared_data["espera_total"]} ms")
        update_corner_label(canvas, shared_data["espera_total"])  # Update the label with the total wait time
        shared_data["mutex"].release()  # Always release the lock, even if an exception occurs


    except Exception as e:
        # Print out the exception and log the values of the variables
        print(f"Exception occurred: {e}")
        print(f"Aluno: {aluno}")
        print(f"ID: {id}")
        print(f"Máquinas: {maquinas}")
        print(f"Índice de máquina: {index}")
        print(f"Tamanho do treino: {len(aluno[1])}")
        print(f"Exception Type: {type(e)}")
        print(f"Exception Args: {e.args}")
