import random
import numpy as np
from Gymsys_manager import *
import matplotlib.pyplot as plt

# Define a função fitness do algoritmo genético
# Aplica a fórmula C/M² para cada máquina em cada horário e realiza a soma de todos os valores obtidos para obter uma nota.
# A esta nota é então aplicada uma penalidade para cada aluno que precisou ser descartado do agendamento.
# O resultado final é a nota fitness do indivíduo.
# C = Colisões e M = quantidade de instâncias de uma máquina.
# Detalhes do cálculo de colisões estão disponíveis no comentário do método calcular_colisões()
def funcao_fitness(individuo):
    fitness = 0
    individuo_sem_descarte = individuo.copy()
    descarte = individuo_sem_descarte.pop(len(individuo_sem_descarte)-1)
    for x in range(6):
        colisoes = calcular_colisões(individuo_sem_descarte[x])
        maqs_quadrado = np.square(qntd_maquinas)
        lista_resultado = colisoes/maqs_quadrado
        fitness += np.sum(lista_resultado)
    fitness += (descarte*peso_descarte)
    return fitness

# Cria um indivíduo, composto por 7 genes (6 horarios(lista) e quantidade de descartes(int))
def criar_individuo(espaco_solucao):
    copia_espaco_solucao = espaco_solucao.copy()
    individuo = [[], [], [], [], [], [], 0]
    for _ in range(len(copia_espaco_solucao)):
        aluno = copia_espaco_solucao.pop(0)
        horarios_possiveis= (aluno[0].copy())
        aluno_nao_processado = True
        while(aluno_nao_processado):
            if(len(horarios_possiveis) > 0):
                rng = np.random.default_rng()
                index_horario_escolhido = rng.integers(low=0, high=len(horarios_possiveis))
                horario_escolhido = horarios_possiveis[index_horario_escolhido]
                index_horario_individuo = (horario_escolhido-12)
                if(len(individuo[index_horario_individuo]) < 20):
                            individuo[index_horario_individuo].append(aluno)
                            aluno_nao_processado = False
                else:
                     horarios_possiveis.pop(index_horario_escolhido)
                     if(len(horarios_possiveis) == 0):
                        individuo[6] += 1
                        aluno_nao_processado = False                
    return individuo

# Realiza o crossover de forma entrelaçada entre 2 indivíduos para gerar 2 novos indivíduos
#
#   Crossover entrelaçado: 
#       -Distribuimos o aluno no filho1 com base em sua posição no parente1
#       -Distribuimos o aluno no filho2 com base em sua posicao no parente2
#
#   Para o próximo aluno fazemos o oposto:
#       -Distribuimos o aluno no filho1 com base em sua posição no parente2
#       -Distribuimos o aluno no filho2 com base em sua posicao no parente1
#   e assim por diante até todos os alunos serem processados.
#   Por fim, realizamos a repescagem dos alunos descartados.
def crossover_entrelacado(parente1, parente2, espaco_solucao):
    copia_espaco_solucao = espaco_solucao.copy()
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

# Realiza o crossover um ponto entre 2 indivíduos para gerar 2 novos indivíduos
#
#   Crossover um ponto: 
#       -Cortamos o espaço solução em 2 metades
#       -Na primeira metade distribuimos os alunos no filho1 com base nas suas posições no parente1
#       -Distribuímos os alunos no filho2 com base nas suas posições no parente2
#
#   Na segunda metade fazemos o oposto:
#       -Distribuimos os alunos no filho1 com base em suas posições no parente2
#       -Distribuimos os alunos no filho2 com base em suas posições no parente1
#   e por fim realizamos a repescagem dos alunos descartados.
def crossover_um_ponto(parente1, parente2, espaco_solucao):
    copia_espaco_solucao = espaco_solucao.copy()
    filho1 = [[], [], [], [], [], [], 0]
    repescagem_filho1 = []
    filho2 = [[], [], [], [], [], [], 0]
    repescagem_filho2 = []
    index_meio_espaco_solucao = len(copia_espaco_solucao)/2
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

# Realiza a mutação em um indivíduo selecionando um aluno aleatório e trocando sua posição
# com outro aluno aleatório que seja compatível (ambos tem o horário do outro como disponível e estão em horários diferentes)
def mutacao(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        index_aluno1 = index_aluno_aleatorio(individuo)
        aluno1 = individuo[index_aluno1[0]][index_aluno1[1]]
        index_aluno2 = index_aluno_aleatorio(individuo)
        aluno2 = individuo[index_aluno2[0]][index_aluno2[1]]
        # testamos separadamente se o aluno1 tem disponibilidade em mais de 1 horário pois este é o único caso
        # que não pode ser tratado gerando um novo aluno2
        while (len(aluno1[0]) == 1):
            index_aluno1 = index_aluno_aleatorio(individuo)
            aluno1 = individuo[index_aluno1[0]][index_aluno1[1]]
        fator_break = 0
        # Não é necessário testar se os alunos são iguais pois neste caso eles teriam o mesmo index no indivíduo
        while (not alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2)):
            index_aluno2 = index_aluno_aleatorio(individuo)
            aluno2 = individuo[index_aluno2[0]][index_aluno2[1]]
            # Utilizamos o fator_break para tratar o extremamente improvável caso de não existir aluno trocável com o aluno1
            fator_break += 1
            if(fator_break > 100):
                return mutacao(individuo, 1)
        # Aqui é realizada a troca
        individuo[index_aluno1[0]][index_aluno1[1]] = aluno2
        individuo[index_aluno2[0]][index_aluno2[1]] = aluno1
    return individuo


# Realiza a seleçao torneio de 2 indivíduos
def selecao_torneio(populacao):
    tam_torneio = 3
    torneio = random.sample(populacao, tam_torneio)
    torneio.sort(key=lambda x: funcao_fitness(x))
    return torneio[0], torneio[1]

# NÃO IMPLEMENTADO
def selecao_rank(populacao, array_fitness):
    # Get the indices that would sort the fitness values in descending order
    sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)
    
    # Rank the individuals based on their fitness (1 is the best rank)
    ranks = [0] * len(fitness_values)
    for rank, index in enumerate(sorted_indices):
        ranks[index] = rank + 1  # Rank starts from 1
    
    # Calculate the total sum of ranks
    total_rank_sum = sum(ranks)
    
    # Generate a random number between 0 and the total rank sum
    rand = random.uniform(0, total_rank_sum)
    
    # Find the individual that corresponds to the random number based on ranks
    cumulative_sum = 0
    for individual, rank in zip(population, ranks):
        cumulative_sum += rank
        if cumulative_sum > rand:
            return individual
        
# NÃO IMPLEMENTADO
def selecao_roleta(populacao, array_fitness):
    # Step 1: Normalize fitness values to create selection probabilities
    fitness_total = sum(array_fitness)
    prob_selecao = [fitness / fitness_total for fitness in array_fitness]
    
    # Step 2: Create a cumulative distribution of probabilities
    probs_acumulativa = []
    soma_acumulativa = 0
    for prob in prob_selecao:
        soma_acumulativa += prob
        probs_acumulativa.append(soma_acumulativa)
    
    # Step 3: Select a random number and find the corresponding individual
    rand_value = random.random()  # Random number between 0 and 1
    
    for i, prob_acumulativa in enumerate(probs_acumulativa):
        if rand_value < prob_acumulativa:
            individuo_selecionado = populacao[i]
            break
    
    return individuo_selecionado

# Algoritmo genético para a evolução de uma grade de agendamentos de alunos em uma academia
def algoritmo_genetico(num_generacoes, tam_populacao, espaco_solucao, taxa_mutacao):
    lista_pre = []
    lista_pos = []
    lista_valor_otimizacao = []
    melhor_individuo = None
    for j in range(10):
        print("execução atual:")
        print(j)
        espaco_solucao2 = gerar_alunos()
        # Inicializa a população
        populacao = [criar_individuo(espaco_solucao2) for _ in range(tam_populacao)]
        populacao.sort(key=lambda x: funcao_fitness(x))
        lista_pre.append(funcao_fitness(populacao[0]))
        for geracao in range(num_generacoes):
            # Calcula a nota fitness da população
            populacao.sort(key=lambda x: funcao_fitness(x))
            melhor_individuo = populacao[0]
            print(f"Generation {geracao}: Best Fitness = {funcao_fitness(melhor_individuo)}")
            
            # Cria uma nova população através dos operadores de crossover e mutação
            nova_populacao = []
            # Aqui implementamos o elitismo:
            for i in range(elitismo):
                nova_populacao.append(populacao[i])
            
            while (len(nova_populacao) < tam_populacao):
                # O método de seleção pode ser alterado na próxima linha:
                parente1, parente2 = selecao_torneio(populacao)
                filho1, filho2 = crossover_entrelacado(parente1, parente2, espaco_solucao2)
                nova_populacao.append(mutacao(filho1, taxa_mutacao))
                if (len(nova_populacao) < tam_populacao):
                    nova_populacao.append(mutacao(filho2, taxa_mutacao))
            
            populacao = nova_populacao

        # Retorna o melhor indivíduo encontrado
        melhor_individuo = min(populacao, key=lambda x: funcao_fitness(x))
        lista_pos.append(funcao_fitness(melhor_individuo))
        lista_valor_otimizacao.append(lista_pre[j] - lista_pos[j])
    return melhor_individuo

# Parametros
num_generacoes = 100
tam_populacao = 50
espaco_solucao = gerar_alunos()  # Lista de alunos a serem agendados
taxa_mutacao = 0.1
elitismo = 2
peso_descarte = 500 # Peso da penalidade por aluno descartado