import random
import numpy as np
import copy
import matplotlib.pyplot as plt
from Gymsys_manager import *
from Gymsys_simulacao import *

def funcao_fitness(individuo):
    """
    Calcula a fitness de um indivíduo no algoritmo genético.

    Aplica a fórmula C/M² para cada máquina em cada horário, onde C é o número de colisões
    e M é a quantidade de instâncias de uma máquina. Depois, aplica uma penalidade para cada aluno
    que precisou ser descartado durante o processo de agendamento.

    Parâmetros:
        individuo (list): Representação de um indivíduo (solução de agendamento).

    Retorna:
        float: A nota fitness do indivíduo.
    """
    fitness = 0
    individuo_sem_descarte = individuo.copy()
    descarte = individuo_sem_descarte.pop(len(individuo_sem_descarte)-1)
    for x in range(6):
        colisoes = calcular_colisões(individuo_sem_descarte[x])
        maqs_quadrado = np.square(qntd_maquinas)
        lista_resultado = colisoes/maqs_quadrado
        fitness += np.sum(lista_resultado)
    fitness += (descarte * peso_descarte)
    return fitness

def criar_individuo(espaco_solucao):
    """
    Cria um novo indivíduo para o algoritmo genético.

    Um indivíduo é composto por 6 horários e a quantidade de alunos descartados.

    Parâmetros:
        espaco_solucao (list): Lista de alunos com seus horários disponíveis.

    Retorna:
        list: Representação de um indivíduo (solução de agendamento).
    """
    copia_espaco_solucao = espaco_solucao.copy()
    individuo = [[], [], [], [], [], [], 0]
    for _ in range(len(copia_espaco_solucao)):
        aluno = copia_espaco_solucao.pop(0)
        horarios_possiveis = aluno[0].copy()
        aluno_nao_processado = True
        while(aluno_nao_processado):
            if(len(horarios_possiveis) > 0):
                rng = np.random.default_rng()
                index_horario_escolhido = rng.integers(low=0, high=len(horarios_possiveis))
                horario_escolhido = horarios_possiveis[index_horario_escolhido]
                index_horario_individuo = (horario_escolhido - 12)
                if(len(individuo[index_horario_individuo]) < 20):
                    individuo[index_horario_individuo].append(aluno)
                    aluno_nao_processado = False
                else:
                    horarios_possiveis.pop(index_horario_escolhido)
                    if(len(horarios_possiveis) == 0):
                        individuo[6] += 1
                        aluno_nao_processado = False
    return individuo

def crossover_entrelacado(parente1, parente2, espaco_solucao):
    """
    Realiza o crossover entrelaçado entre dois indivíduos para gerar dois novos indivíduos.

    A distribuição dos alunos ocorre de forma alternada entre os pais, onde a posição de um aluno no primeiro parente
    é trocada com a posição de um aluno no segundo parente.

    Parâmetros:
        parente1 (list): Primeiro indivíduo (parent).
        parente2 (list): Segundo indivíduo (parent).
        espaco_solucao (list): Lista de alunos disponíveis para agendamento.

    Retorna:
        tuple: Dois novos indivíduos gerados pelo crossover.
    """
    copia_espaco_solucao = random.sample(espaco_solucao, len(espaco_solucao))
    filho1 = [[], [], [], [], [], [], 0]
    repescagem_filho1 = []
    filho2 = [[], [], [], [], [], [], 0]
    repescagem_filho2 = []
    for x in range(len(copia_espaco_solucao)):
        aluno = copia_espaco_solucao.pop(0)
        index_aluno_em_parente1 = encontrar_aluno_individuo(aluno, parente1)
        index_aluno_em_parente2 = encontrar_aluno_individuo(aluno, parente2)
        if(x % 2 == 0):
            filho1 = anexar_aluno(index_aluno_em_parente1, aluno, filho1, repescagem_filho1)
            filho2 = anexar_aluno(index_aluno_em_parente2, aluno, filho2, repescagem_filho2)
        else:
            filho2 = anexar_aluno(index_aluno_em_parente1, aluno, filho2, repescagem_filho2)
            filho1 = anexar_aluno(index_aluno_em_parente2, aluno, filho1, repescagem_filho1)
    repescagem(filho1, repescagem_filho1)
    repescagem(filho2, repescagem_filho2)
    return filho1, filho2

def crossover_um_ponto(parente1, parente2, espaco_solucao):
    """
    Realiza o crossover de um ponto entre dois indivíduos para gerar dois novos indivíduos.

    O espaço solução é cortado em duas metades e a primeira metade é copiada de um parente
    para o filho1 e a segunda metade é copiada de outro parente para o filho2. O oposto ocorre
    na segunda metade do crossover.

    Parâmetros:
        parente1 (list): Primeiro indivíduo (parent).
        parente2 (list): Segundo indivíduo (parent).
        espaco_solucao (list): Lista de alunos disponíveis para agendamento.

    Retorna:
        tuple: Dois novos indivíduos gerados pelo crossover.
    """
    copia_espaco_solucao = espaco_solucao.copy()
    filho1 = [[], [], [], [], [], [], 0]
    repescagem_filho1 = []
    filho2 = [[], [], [], [], [], [], 0]
    repescagem_filho2 = []
    index_meio_espaco_solucao = len(copia_espaco_solucao) / 2
    for x in range(len(copia_espaco_solucao)):
        aluno = copia_espaco_solucao.pop(0)
        index_aluno_em_parente1 = encontrar_aluno_individuo(aluno, parente1)
        index_aluno_em_parente2 = encontrar_aluno_individuo(aluno, parente2)
        if (x < index_meio_espaco_solucao):
            filho1 = anexar_aluno(index_aluno_em_parente1, aluno, filho1, repescagem_filho1)
            filho2 = anexar_aluno(index_aluno_em_parente2, aluno, filho2, repescagem_filho2)
        else:
            filho2 = anexar_aluno(index_aluno_em_parente1, aluno, filho2, repescagem_filho2)
            filho1 = anexar_aluno(index_aluno_em_parente2, aluno, filho1, repescagem_filho1)
    repescagem(filho1, repescagem_filho1)
    repescagem(filho2, repescagem_filho2)
    return filho1, filho2

def mutacao(individuo, taxa_mutacao):
    """
    Realiza a mutação de um indivíduo selecionando dois alunos aleatórios e trocando suas posições.

    A troca ocorre apenas se ambos os alunos possuem horários compatíveis para a troca.

    Parâmetros:
        individuo (list): O indivíduo (solução de agendamento) que será mutado.
        taxa_mutacao (float): A probabilidade de ocorrer a mutação.

    Retorna:
        list: O indivíduo após a mutação.
    """
    if random.random() < taxa_mutacao:
        index_aluno1 = index_aluno_aleatorio(individuo)
        aluno1 = individuo[index_aluno1[0]][index_aluno1[1]]
        index_aluno2 = index_aluno_aleatorio(individuo)
        aluno2 = individuo[index_aluno2[0]][index_aluno2[1]]
        while (len(aluno1[0]) == 1):
            index_aluno1 = index_aluno_aleatorio(individuo)
            aluno1 = individuo[index_aluno1[0]][index_aluno1[1]]
        fator_break = 0
        while (not alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2)):
            index_aluno2 = index_aluno_aleatorio(individuo)
            aluno2 = individuo[index_aluno2[0]][index_aluno2[1]]
            fator_break += 1
            if(fator_break > 100):
                return mutacao(individuo, 1)
        individuo[index_aluno1[0]][index_aluno1[1]] = aluno2
        individuo[index_aluno2[0]][index_aluno2[1]] = aluno1
    return individuo

def selecao_torneio(populacao):
    """
    Realiza a seleção por torneio de 2 indivíduos.

    Parâmetros:
        populacao (list): A população de indivíduos.

    Retorna:
        tuple: Os dois indivíduos selecionados para o torneio.
    """
    tam_torneio = 7
    torneio = random.sample(populacao, tam_torneio)
    torneio.sort(key=lambda x: funcao_fitness(x))
    return torneio[0], torneio[1]

def selecao_rank(populacao, num_pais):   
    """
    Realiza a seleção por ranking em uma população usando uma função de fitness definida previamente.
    
    Parâmetros:
        population (list): Lista de indivíduos da população.
        num_pais (int): Número de pais a serem selecionados.

    Retorna:
        list: Indivíduos selecionados (pais) da população.
    """
    # Calcula a aptidão (fitness) de cada indivíduo
    fitness_scores = [funcao_fitness(ind) for ind in populacao]

    # Obtém os índices que ordenam os indivíduos por fitness (do maior para o menor)
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)

    # Cria a lista de ranks (1 = melhor, N = pior)
    ranks = list(range(1, len(populacao) + 1))
    total_rank = sum(ranks)

    # Calcula as probabilidades com base nos ranks (maior rank → maior probabilidade)
    probabilities = [(len(populacao) - rank + 1) / total_rank for rank in ranks]

    # Reordena a população e as probabilidades com base na ordem dos índices ordenados
    ranked_population = [populacao[i] for i in sorted_indices]
    ranked_probabilities = [probabilities[i] for i in sorted_indices]

    # Seleciona os pais usando as probabilidades baseadas no ranking
    selected = random.choices(ranked_population, weights=ranked_probabilities, k=num_pais)

    return selected

def selecao_rank_com_elitismo(population, num_pais, elitismo):
    """
    Realiza a seleção por ranking com elitismo em uma população usando uma função de fitness definida previamente.
    
    Parâmetros:
        population (list): Lista de indivíduos da população.
        num_pais (int): Número de pais a serem selecionados.
        elitismo (int): Número de indivíduos a serem garantidos como elites na seleção.

    Retorna:
        list: Indivíduos selecionados (pais) da população.
    """
    # Calcula a aptidão (fitness) de cada indivíduo
    fitness_scores = [funcao_fitness(ind) for ind in population]

    # Obtém os índices que ordenam os indivíduos por fitness (do maior para o menor)
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)

    # Seleciona os elites diretamente
    elites = [population[sorted_indices[i]] for i in range(elitismo)]

    # Cria a lista de ranks (1 = melhor, N = pior)
    ranks = list(range(1, len(population) + 1))
    total_rank = sum(ranks)

    # Calcula as probabilidades com base nos ranks
    probabilities = [(len(population) - rank + 1) / total_rank for rank in ranks]

    # Reordena a população e as probabilidades com base na ordem dos índices ordenados
    ranked_population = [population[i] for i in sorted_indices]
    ranked_probabilities = [probabilities[i] for i in sorted_indices]

    # Seleciona os demais pais (não incluindo os elites)
    remaining_parents = num_pais - elitismo
    selected_others = random.choices(ranked_population, weights=ranked_probabilities, k=remaining_parents)

    return elites + selected_others

def selecao_roleta(populacao, num_pais):
    """
    Realiza seleção por roleta (roulette wheel selection).
    
    Parâmetros:
        populacao (list): Lista de indivíduos.
        num_pais (int): Número de pais a serem selecionados.

    Retorna:
        list: Indivíduos selecionados (pais) da população.
    """
    # Calcula a aptidão de cada indivíduo
    fitness_scores = [funcao_fitness(ind) for ind in populacao]

    # Normaliza os valores de fitness para criar uma distribuição de probabilidade
    total_fitness = sum(fitness_scores)
    probabilities = [f / total_fitness for f in fitness_scores]

    # Seleciona os pais com base nas probabilidades
    selected = random.choices(populacao, weights=probabilities, k=num_pais)

    return selected

def selecao_roleta_com_elitismo(populacao, num_pais, elitismo):
    """
    Realiza seleção por roleta com elitismo.
    
    Parâmetros:
        populacao (list): Lista de indivíduos.
        num_pais (int): Número de pais a serem selecionados.
        elitismo (int): Número de indivíduos a serem garantidos como elites na seleção.

    Retorna:
        list: Indivíduos selecionados (pais) da população.
    """
    # Calcula a aptidão de cada indivíduo
    fitness_scores = [funcao_fitness(ind) for ind in populacao]

    # Encontra os índices ordenados por fitness (maior para menor)
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)

    # Seleciona os indivíduos elites
    elites = [populacao[sorted_indices[i]] for i in range(elitismo)]

    # Remove os elites da população para a roleta
    non_elite_population = [populacao[i] for i in range(len(populacao)) if i not in sorted_indices[:elitismo]]
    non_elite_fitness = [fitness_scores[i] for i in range(len(populacao)) if i not in sorted_indices[:elitismo]]

    # Proteção contra divisão por zero
    if sum(non_elite_fitness) == 0:
        probabilities = [1 / len(non_elite_population)] * len(non_elite_population)
    else:
        total_fitness = sum(non_elite_fitness)
        probabilities = [f / total_fitness for f in non_elite_fitness]

    # Seleciona os restantes via roleta
    selected_others = random.choices(non_elite_population, weights=probabilities, k=num_pais - elitismo)

    return elites + selected_others

# Algoritmo genético para a evolução de uma grade de agendamentos de alunos em uma academia
def algoritmo_genetico(num_generacoes, tam_populacao, espaco_solucao, taxa_mutacao):
    """
    Executa o algoritmo genético para otimizar a grade de agendamentos.

    O algoritmo evolui uma população de soluções (agendamentos de alunos), usando seleção,
    crossover e mutação para gerar novos agendamentos, buscando melhorar a fitness a cada geração.

    Parâmetros:
        num_generacoes (int): Número de gerações para o algoritmo executar.
        tam_populacao (int): Tamanho da população de indivíduos.
        espaco_solucao (list): Lista de alunos a serem agendados.
        taxa_mutacao (float): Taxa de mutação de cada indivíduo.

    Retorna:
        list: O melhor indivíduo encontrado.
    """
    lista_pre = []
    lista_pos = []
    lista_valor_otimizacao = []
    melhor_individuo = None
    for j in range(10):
        print("execução atual:")
        print(j)
        espaco_solucao2 = gerar_alunos()
        populacao = [criar_individuo(random.sample(espaco_solucao2, len(espaco_solucao2))) for _ in range(tam_populacao)]
        populacao.sort(key=lambda x: funcao_fitness(x))
        lista_pre.append(funcao_fitness(populacao[0]))
        copia_individuo = copy.deepcopy(populacao[0])
        create_window(iniciar_simulacao, copia_individuo)
        for geracao in range(num_generacoes):
            populacao.sort(key=lambda x: funcao_fitness(x))
            melhor_individuo = populacao[0]
            print(f"Generation {geracao}: Best Fitness = {funcao_fitness(melhor_individuo)}")
            nova_populacao = []
            for i in range(elitismo):
                nova_populacao.append(populacao[i])
            while (len(nova_populacao) < tam_populacao):
                parente1, parente2 = selecao_torneio(populacao)
                filho1, filho2 = crossover_entrelacado(parente1, parente2, espaco_solucao2)
                nova_populacao.append(mutacao(filho1, taxa_mutacao))
                if (len(nova_populacao) < tam_populacao):
                    nova_populacao.append(mutacao(filho2, taxa_mutacao))
            populacao = nova_populacao

        melhor_individuo = min(populacao, key=lambda x: funcao_fitness(x))
        create_window(iniciar_simulacao, melhor_individuo)
        lista_pos.append(funcao_fitness(melhor_individuo))
        lista_valor_otimizacao.append(lista_pre[j] - lista_pos[j])
    return melhor_individuo

# Parametros
num_generacoes = 100
tam_populacao = 50
espaco_solucao = gerar_alunos()  # Lista de alunos a serem agendados
taxa_mutacao = 0.2
elitismo = 2
peso_descarte = 500 # Peso da penalidade por aluno descartado
