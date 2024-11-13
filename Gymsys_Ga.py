import random
import numpy as np
from Gymsys_manager import *
import matplotlib.pyplot as plt

# Define the problem-specific fitness function
def fitness_function(individual):
    total_fitness = nota_fitness(individual)
    return total_fitness

# Create an individual, which consists of 6 genes
def create_individual(value_range):
    print(len(value_range))
    x = 0
    copia_range = value_range.copy()
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

#NÃO IMPLEMENTADO
# Crossover two individuals to create a child
def crossover(parent1, parent2):
    # Perform a crossover between the two parents at the gene level
    crossover_point = random.randint(1, len(parent1) - 1)  # Crossover at the gene level
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

#NÃO IMPLEMENTADO
# Mutate an individual by modifying one of its genes
def mutate(individual, mutation_rate, value_range):
    if random.random() < mutation_rate:
        gene_index = random.randint(0, len(individual) - 1)  # Randomly pick a gene to mutate
        individual[gene_index] = create_gene(len(individual[gene_index]), value_range)
    return individual

#NÃO IMPLEMENTADO
# Tournament selection of two individuals
def select_parents(population):
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda x: fitness_function(x), reverse=True)
    return tournament[0], tournament[1]

#NÃO IMPLEMENTADO
# Genetic algorithm to evolve a population of individuals
def genetic_algorithm(num_generations, population_size, value_range, mutation_rate):
    # Initialize population
    population = [create_individual(value_range) for _ in range(population_size)]
    
    for generation in range(num_generations):
        # Evaluate fitness of the population
        population.sort(key=lambda x: fitness_function(x), reverse=True)
        best_individual = population[0]
        print(f"Generation {generation}: Best Fitness = {fitness_function(best_individual)}")
        
        # Create new population through crossover and mutation
        new_population = []
        
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate, value_range))
            if len(new_population) < population_size:
                new_population.append(mutate(child2, mutation_rate, value_range))
        
        population = new_population

    # Return the best individual found
    best_individual = min(population, key=lambda x: fitness_function(x))
    return best_individual

# Parameters
num_generations = 100
population_size = 50
value_range = gerar_alunos()  # Possible values for the tuples
mutation_rate = 0.1

# Run the genetic algorithm
#best_individual = genetic_algorithm(num_generations, population_size, value_range, mutation_rate)
#print(f"Best Individual: {best_individual}")
#print(f"Best Fitness: {fitness_function(best_individual)}")

#testes:
array_fitness = []
for x in range(5000):
     individuo = create_individual(value_range)
     array_fitness.append(fitness_function(individuo))
array_fitness_sorted = np.sort(array_fitness)

plt.plot(array_fitness_sorted)
plt.ylabel('resultados fitness para individuos')
plt.show()