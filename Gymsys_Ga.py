import random
import numpy as np
from Gymsys_manager import *
import matplotlib.pyplot as plt

# Define a função fitness do algoritmo genético
def funcao_fitness(individual):
    fitness = nota_fitness(individual)
    return fitness

# Cria um indivíduo, composto por 7 genes (6 horarios(lista) e qntd de descartes(int))
def create_individual(espaco_solucao):
    print(len(espaco_solucao))
    x = 0
    copia_range = espaco_solucao.copy()
    individuo = [[], [], [], [], [], [], 0]
    for _ in range(len(copia_range)):
        x = x + 1
        print("aluno: ", x)
        aluno = copia_range.pop(0)
        horarios_possiveis_not_list = (aluno[0].copy())
        horarios_possiveis = horarios_possiveis_not_list.tolist()
        aluno_nao_processado = True
        while(aluno_nao_processado):
            if(len(horarios_possiveis) > 0):
                rng = np.random.default_rng()
                index_horario_escolhido = rng.integers(low=0, high=len(horarios_possiveis))
                horario_escolhido = aluno[0][index_horario_escolhido]
                index_horario_individuo = (horario_escolhido-12)
                if(len(individuo[index_horario_individuo]) < 20):
                            individuo[index_horario_individuo].append(aluno)
                            aluno_nao_processado = False
                else:
                     print("horario testado esta cheio, buscando novo horario...")
                     print("tamanho do array de horários possíveis: ", len(horarios_possiveis))
                     print("index do horário a ser removido: ", index_horario_escolhido)
                     horarios_possiveis.pop(index_horario_escolhido)
                     if(len(horarios_possiveis) == 0):
                        individuo[6] += 1
                        print("não há horários disponíveis para este aluno.")
                        aluno_nao_processado = False                         
    return individuo

# Realiza o crossover de forma entrelaçada entre 2 solucoes para gerar 2 novas solucoes
#
#                       Crossover entrelaçado: 
#                       -Distribuimos o aluno no filho1 com base em sua posição no parente1
#                       -Distribuimos o aluno no filho2 com base em sua posicao no parente2
#
#                       Para o próximo aluno fazemos o oposto:
#                       -Distribuimos o aluno no filho1 com base em sua posição no parente2
#                       -Distribuimos o aluno no filho2 com base em sua posicao no parente1
#                       e assim por diante até todos os alunos serem processados.
def crossover_entrelacado(parente1, parente2, espaco_solucao):
    copia_espaco_solucao = espaco_solucao.copy()
    filho1 = [[], [], [], [], [], [], 0]
    filho2 = [[], [], [], [], [], [], 0]
    for x in range(len(copia_espaco_solucao)):
        aluno = copia_espaco_solucao.pop(0)
        index_aluno_em_parente1 = encontrar_aluno_solucao(aluno, parente1)
        index_aluno_em_parente2 = encontrar_aluno_solucao(aluno, parente2)
        if(x % 2 == 0):
            filho1 = anexar_aluno(index_aluno_em_parente1, aluno, filho1)
            filho2 = anexar_aluno(index_aluno_em_parente2, aluno, filho2)
        else:
            filho2 = anexar_aluno(index_aluno_em_parente1, aluno, filho1)
            filho1 = anexar_aluno(index_aluno_em_parente2, aluno, filho2)
    return filho1, filho2

def crossover_um_ponto(parente1, parente2, espaco_solucao):
    copia_espaco_solucao = espaco_solucao.copy()
    filho1 = [[], [], [], [], [], [], 0]
    filho2 = [[], [], [], [], [], [], 0]
    index_meio_espaco_solucao = len(copia_espaco_solucao)/2
    for x in range(len(copia_espaco_solucao)):
        aluno = copia_espaco_solucao.pop(0)
        index_aluno_em_parente1 = encontrar_aluno_solucao(aluno, parente1)
        index_aluno_em_parente2 = encontrar_aluno_solucao(aluno, parente2)
        if (x < index_meio_espaco_solucao):
            filho1 = anexar_aluno(index_aluno_em_parente1, aluno, filho1)
            filho2 = anexar_aluno(index_aluno_em_parente2, aluno, filho2)
        else:
            filho2 = anexar_aluno(index_aluno_em_parente1, aluno, filho1)
            filho1 = anexar_aluno(index_aluno_em_parente2, aluno, filho2)
    return filho1, filho2

# Realiza a mutação em uma solução selecionando um aluno aleatório e trocando sua posição
# com outro aluno aleatório que seja compatível (ambos tem o horário do outro como disponível e estão em horários diferentes)
def mutacao(individual, taxa_mutacao):
    if random.random() < taxa_mutacao:
        index_aluno1 = index_aluno_aleatorio(individual)
        aluno1 = individual[index_aluno1[0]][index_aluno1[1]]
        index_aluno2 = index_aluno_aleatorio(individual)
        aluno2 = individual[index_aluno2[0]][index_aluno2[1]]
        #testamos separadamente se o aluno1 tem disponibilidade em mais de 1 horário pois este é o único caso
        #que não pode ser tratado gerando um novo aluno2
        while (len(aluno1[0]) == 1):
            index_aluno1 = index_aluno_aleatorio(individual)
            aluno1 = individual[index_aluno1[0]][index_aluno1[1]]
        fator_break = 0
        #Não é necessário testar se os alunos são iguais pois neste caso eles teriam o mesmo index na solucao
        while (not alunos_trocaveis(aluno1, index_aluno1[0], aluno2, index_aluno2[0])):
            index_aluno2 = index_aluno_aleatorio(individual)
            aluno2 = individual[index_aluno2[0]][index_aluno2[1]]
            #Utilizamos o fator_break para tratar o extremamente improvável caso de não existir aluno trocável com o aluno1
            fator_break += 1
            if(fator_break > 100):
                return mutacao(individual, 1)
        #Aqui é realizada a troca
        individual[index_aluno1[0][index_aluno1[1]]] = aluno2
        individual[index_aluno2[0][index_aluno2[1]]] = aluno1
    return individual


#NÃO IMPLEMENTADO
# Realiza a seleçao torneio de 2 indivíduos
def selecao_torneio(populacao):
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: funcao_fitness(x), reverse=True)
    return tournament[0], tournament[1]

#NÃO IMPLEMENTADO
# Genetic algorithm to evolve a population of individuals
def genetic_algorithm(num_generacoes, tam_populacao, espaco_solucao, taxa_mutacao):
    # Initialize population
    population = [create_individual(espaco_solucao) for _ in range(tam_populacao)]
    
    for generation in range(num_generacoes):
        # Evaluate fitness of the population
        population.sort(key=lambda x: funcao_fitness(x), reverse=True)
        best_individual = population[0]
        print(f"Generation {generation}: Best Fitness = {funcao_fitness(best_individual)}")
        
        # Create new population through crossover and mutation
        new_population = []
        
        while (len(new_population) < tam_populacao):
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutacao(child1, taxa_mutacao))
            if (len(new_population) < tam_populacao):
                new_population.append(mutacao(child2, taxa_mutacao))
        
        population = new_population

    # Return the best individual found
    best_individual = min(population, key=lambda x: funcao_fitness(x))
    return best_individual

# Parametros
num_generacoes = 100
tam_populacao = 50
espaco_solucao = gerar_alunos()  # Possible values for the tuples
taxa_mutacao = 0.1

# Roda o algoritmo genético:
#best_individual = genetic_algorithm(num_generations, population_size, value_range, mutation_rate)
#print(f"Best Individual: {best_individual}")
#print(f"Best Fitness: {fitness_function(best_individual)}")

#testes:
array_fitness = []
for x in range(5000):
     individuo = create_individual(espaco_solucao)
     array_fitness.append(funcao_fitness(individuo))
array_fitness_sorted = np.sort(array_fitness)

plt.plot(array_fitness_sorted)
plt.ylabel('resultados fitness para individuos')
plt.show()