import numpy as np

#retorna um array de 10 inteiros entre 0 e 9 representando um treino
def gerar_treino():
    rng = np.random.default_rng()
    treino = rng.integers(low=0, high=10, size=10)
    while(bad_rng_check(treino)):
        treino = rng.integers(low=0, high=10, size=10)
    return treino

#retorna uma tupla de 2 items para representar um aluno no formato (horarios_disponíveis, treino)
def gerar_aluno():
    horarios = gerar_horarios()
    treino = gerar_treino()
    aluno = (horarios, treino)
    return aluno

#retorna um array de 60 a 130 treinos, representando a quantidade variável de alunos
def gerar_alunos():
    rng = np.random.default_rng()
    qntd_alunos = rng.integers(low=10, high=20, endpoint=True)
    alunos = []
    for x in range(qntd_alunos):
        alunos.append(gerar_aluno())
    return alunos

#retorna um array com o número de colisões de máquina entre dois treinos, cada posição do array representa a máquina do seu digito
def comparar_treino(treino1, treino2):
    resultado = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(10):
        for y in range(10):
            if(treino1[x] == treino2[y]):
                resultado[treino1[x]] +=1
    return resultado

#retorna um array com o número de colisões de máquina entre dois treinos pulando elementos duplicados do primeiro treino
def comparar_treino2(treino1, treino2):
    resultado = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    treino_sem_dupes = list(set(treino1))
    for x in range(len(treino_sem_dupes)):
        for y in range(10):
            if(treino_sem_dupes[x] == treino2[y]):
                resultado[treino_sem_dupes[x]] +=1
    return resultado

#analisa o treino quando comparado aos outros alunos do horário para dar uma nota
def nota_recomendacao(treinos_horario, treino_aluno):
    nota = 0
    tam = len(treinos_horario)
    for x in range(tam):
        comparacao = comparar_treino(treinos_horario[x], treino_aluno)
        nota += np.sum(comparacao)
    return nota

#recebe um treino e retorna True quando alguma máquina aparece no treino mais de 3 vezes
def bad_rng_check(treino):
    for x in range(10):
        indexes = len(np.where(treino == x)[0])
        if (indexes > 3):
            return True
    return False

#retorna um array de horários para representar a disponibilidade de um aluno, o aluno estará disponível em pelo menos um horário
def gerar_horarios():
    rng = np.random.default_rng()
    disponibilidade = rng.integers(low=1, high=6, endpoint=True)
    horarios = rng.choice(['h12', 'h13', 'h14', 'h15', 'h16', 'h17'], disponibilidade, replace=False)
    return horarios

#calcula o número de colisões em um array de treinos usando comparar_treino2(), retorna um array com as colisões para cada elemento
def calcular_colisões(treinos):
    colisoes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(len(treinos)):
        print("tamanho:")
        print(len(treinos))
        treino_testado = treinos[x][1]
        treinos_testado = treinos.copy()
        treinos_testado.pop(x)
        print(x)
        for y in range(len(treinos_testado)):
            colisoes = np.add(colisoes, (comparar_treino2(treino_testado, treinos_testado[y][1])))
            print(colisoes)
    return colisoes

#Testes:

alunos = gerar_alunos()
resultado = calcular_colisões(alunos)
print(resultado)
#treinoTeste1 = gerar_treino()
#treinoTeste2 = gerar_treino()
#print(treinoTeste1)
#print(treinoTeste2)
#output = comparar_treino(treinoTeste1, treinoTeste2)
#print(output)


#treinos_14h = gerar_alunos()
#tam = len(treinos_14h)
#for x in range(tam): 
#     print (f"treino {x}: {treinos_14h[x]}")
#amanda = gerar_treino()
#print(f"Treino da Amanda: {amanda}")
#nota = nota_recomendacao(treinos_14h, amanda)
#print(nota)

