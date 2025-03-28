import numpy as np
import matplotlib.pyplot as plt

qntd_maquinas = [1, 1, 1, 1, 1, 1, 2, 3, 3, 5]


# Retorna uma lista de 10 inteiros entre 0 e 9 representando um treino
def gerar_treino():
    rng = np.random.default_rng()
    treino = rng.integers(low=0, high=10, size=10)
    while(bad_rng_check(treino)):
        treino = rng.integers(low=0, high=10, size=10)
    treino = treino.tolist()
    return treino

# Retorna uma tupla de 2 items para representar um aluno no formato (horarios_disponíveis, treino)
def gerar_aluno():
    horarios = gerar_horarios()
    treino = gerar_treino()
    aluno = (horarios, treino)
    return aluno

# Retorna uma lista de 90 a 130 alunos, representando a quantidade variável de alunos
def gerar_alunos():
    rng = np.random.default_rng()
    qntd_alunos = rng.integers(low=90, high=130, endpoint=True)
    alunos = []
    for x in range(qntd_alunos):
        alunos.append(gerar_aluno())
    return alunos

# Retorna uma lista com o número de colisões de máquina entre dois treinos, cada posição da lista representa a máquina do seu digito
def comparar_treino(treino1, treino2):
    resultado = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(10):
        for y in range(10):
            if(treino1[x] == treino2[y]):
                resultado[treino1[x]] +=1
    return resultado

# Retorna uma lista com o número de colisões de máquina entre dois treinos pulando elementos duplicados do primeiro treino
def comparar_treino2(treino1, treino2):
    resultado = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    treino_sem_dupes = list(set(treino1))
    for x in range(len(treino_sem_dupes)):
        for y in range(10):
            if(treino_sem_dupes[x] == treino2[y]):
                resultado[treino_sem_dupes[x]] +=1
    return resultado

# Analisa o treino quando comparado aos outros alunos do horário para dar uma nota
def nota_recomendacao(treinos_horario, treino_aluno):
    nota = 0
    tam = len(treinos_horario)
    for x in range(tam):
        comparacao = comparar_treino(treinos_horario[x], treino_aluno)
        nota += np.sum(comparacao)
    return nota

# Recebe um treino e retorna True quando alguma máquina aparece no treino mais de 3 vezes
def bad_rng_check(treino):
    for x in range(10):
        indexes = len(np.where(treino == x)[0])
        if (indexes > 3):
            return True
    return False

# Retorna uma lista contendo o horário em que está alocado e seu index neste horário de um aluno aleatório de um individuo ([horario, index])
def index_aluno_aleatorio(individuo):
    index_aluno = []
    rng = np.random.default_rng()
    index_horario = rng.integers(low=0, high=6)
    if(len(individuo[index_horario]) > 0):
        index_aluno_no_horario =rng.integers(low=0, high=len(individuo[index_horario]))  # Randomly pick a gene to mutate
        index_aluno.append(index_horario)
        index_aluno.append(index_aluno_no_horario)
    else:
        index_aluno = index_aluno_aleatorio(individuo)
    return index_aluno

# Retorna uma boolean dizendo se 2 alunos são trocáveis (estão em 2 horários diferentes em que ambos tem disponibilidade)
def alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2):
    horarios_aluno1 = aluno1[0]
    horarios_aluno2 = aluno2[0]
    horarios_comuns = [x for x in horarios_aluno1 if x in horarios_aluno2]
    if (index_aluno1[0] != index_aluno2[0] and ((index_aluno1[0]+12) in horarios_comuns) and ((index_aluno2[0]+12) in horarios_comuns)):
        return True
    return False

# Retorna uma lista de horários para representar a disponibilidade de um aluno, o aluno estará disponível em pelo menos um horário
def gerar_horarios():
    rng = np.random.default_rng()
    disponibilidade = rng.integers(low=1, high=6, endpoint=True)
    horarios = rng.choice([12, 13, 14, 15, 16, 17], disponibilidade, replace=False)
    horarios = horarios.tolist()
    return horarios

# Calcula o número de colisões em uma lista de alunos usando comparar_treino2(), retorna uma lista com as colisões para cada máquina.
# Uma especificidade da implementação é que no loop onde um aluno x é comparado com todos os outros o aluno x será tratado como se tivesse cada
# máquina no máximo uma vez em seu treino, ou seja, se uma máquina aparecer 2 vezes em seu treino ele será tratado como se fosse 1 em seu loop.
# Isto ocorre pois um aluno não compete consigo mesmo por uma máquina. Quando outros alunos forem comparados com o aluno x em
# seus respectivos loops o aluno x será processado normalmente.
def calcular_colisões(treinos):
    colisoes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(len(treinos)):
        treino_testado = treinos[x][1]
        treinos_testado = treinos.copy()
        treinos_testado.pop(x)
        for y in range(len(treinos_testado)):
            colisoes = np.add(colisoes, (comparar_treino2(treino_testado, treinos_testado[y][1])))
    return colisoes

# Retorna o index de um aluno em um horário, retorna None caso o aluno não esteja no horário.
def encontrar_aluno_horario(aluno, horario):
    try:
        index_horario = horario.index(aluno)
        return index_horario
    except ValueError:
        return None

# Retorna o horário em que está um aluno em um indivíduo, retorna None caso o aluno tenha sido descartado.
def encontrar_aluno_individuo(aluno, individuo):
    index_horario = None
    horario = None
    for x in range(6):
        if (index_horario == None):
            index_horario = encontrar_aluno_horario(aluno, individuo[x])
            if (index_horario != None):
                horario = x
                break
    return horario

# Adiciona um aluno a um horário caso haja espaço. Se não houver espaço o aluno é adicionado a lista de repescagem.
def anexar_aluno(index_horario, aluno, individuo, repescagem):
    if (index_horario == None):
        repescagem.append(aluno)
    elif(len(individuo[index_horario]) < 20):
        individuo[index_horario].append(aluno)
    else:
        repescagem.append(aluno)
    return individuo

# Distribui no indivíduo os alunos de uma lista de repescagem.
def repescagem(individuo, repescagem):
    x = 0
    #print("Alunos enviados para repescagem")
    #print(len(repescagem))
    for _ in range(len(repescagem)):
        x = x + 1
        aluno = repescagem.pop(0)
        #print("aluno: (repescagem) ")
        #print(aluno)
        horarios_possiveis= (aluno[0].copy())
        aluno_nao_processado = True
        while(aluno_nao_processado):
            if(len(horarios_possiveis) > 0):
                rng = np.random.default_rng()
                #print("horarios possiveis:(repescagem) ")
                #print(horarios_possiveis)
                index_horario_escolhido = rng.integers(low=0, high=len(horarios_possiveis))
                #print("index horario escolhido:(repescagem) ")
                #print(index_horario_escolhido)
                horario_escolhido = horarios_possiveis[index_horario_escolhido]
                #print("horarios escolhido:(repescagem) ")
                #print(horario_escolhido)
                index_horario_individuo = (horario_escolhido-12)
                if(len(individuo[index_horario_individuo]) < 20):
                            individuo[index_horario_individuo].append(aluno)
                            aluno_nao_processado = False
                else:
                     #print("horario testado esta cheio, buscando novo horario...")
                     #print("tamanho da lista de horários possíveis: ", len(horarios_possiveis))
                     #print("index do horário a ser removido: ", index_horario_escolhido)
                     horarios_possiveis.pop(index_horario_escolhido)
                     if(len(horarios_possiveis) == 0):
                        individuo[6] += 1
                        #print("não há horários disponíveis para este aluno.")
                        aluno_nao_processado = False

# Método auxiliar usado para imprimir os individuos
def imprimir(lista):
    for horario, elem in enumerate(lista):
        if (type(elem) == list):
            print(f'Alunos agendados as {(horario + 12)}h: ')
            imprimir(elem)
        else:
            print(elem)
    print()