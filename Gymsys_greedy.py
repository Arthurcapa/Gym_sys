import copy
from Gymsys_manager import *
from Gymsys_Ga import *

def algoritmo_guloso(espaco_solucao):
    """
    Executa o algoritmo genético para otimizar a grade de agendamentos.

    O algoritmo guloso analisa a nota fitness da solução atual com cada possível inserção de um aluno entre os horários disponíveis do mesmo.
    A alocação com a melhor nota fitness é escolhida e o processo se repete até que todos os alunos sejam alocados ou descartados.
    
    Parâmetros:
        espaco_solucao (list): Lista de indivíduos.

    Retorna:
        list: solução final encontrada pelo algoritmo guloso.
    """
    lista_alunos = copy.deepcopy(espaco_solucao)
    solucao_final = [[], [], [], [], [], [], 0]  # Inicializa a solução final com horários vazios
    i = 0
    while(lista_alunos):
        i += 1
        aluno = lista_alunos.pop(0)
        solucao_temp = criar_nova_solucao(solucao_final, aluno)
        if (solucao_temp != None):
            solucao_final = solucao_temp
        else:
            solucao_final[6] += 1
        print(f"Fitness iteração {i}: {funcao_fitness(solucao_final)}")
    return solucao_final

def criar_nova_solucao(solucao_atual, aluno):
    """
    Cria uma lista de soluções com as possíveis alocações de um aluno na solução atual.
    As soluções são ordenadas pela nota fitness, e a melhor solução é retornada.

    Parâmetros:
        solucao_atual (list): Solução parcial encontrada até o momento durante a execução do algoritmo.
        aluno (tuple): O aluno a ser adicionado à solução.

    Retorna:
        list or None: A melhor solução encontrada ou None se não houver espaço para o aluno.
    """
    solucoes = []
    horarios_aluno = aluno[0]

    # Adiciona o aluno a todos os horários em que ele pode treinar
    for horario in horarios_aluno:
        nova_solucao = copy.deepcopy(solucao_atual)
        if(len(solucao_atual[horario-12]) < 20):
            nova_solucao[horario-12].append(aluno)
            solucoes.append(nova_solucao)
    # Se não houver espaço em nenhum horário, o aluno é descartado
    if (len(solucoes) == 0):
        return None
    # Retorna a melhor solução encontrada
    else:
        solucoes.sort(key=lambda x: funcao_fitness(x))
        return solucoes[0]
