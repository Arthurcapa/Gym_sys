import numpy as np
import matplotlib.pyplot as plt

qntd_maquinas = [1, 1, 1, 1, 1, 1, 2, 3, 3, 5]


def gerar_treino():
    """
    Retorna uma lista de 10 inteiros entre 0 e 9 representando um treino.

    Gera um treino aleatório, garantindo que nenhum número do treino se repita mais de 3 vezes, 
    verificando isso através da função `bad_rng_check`.

    Returns:
        list: Uma lista de 10 inteiros representando o treino gerado.
    """
    rng = np.random.default_rng()
    treino = rng.integers(low=0, high=10, size=10)
    while(bad_rng_check(treino)):
        treino = rng.integers(low=0, high=10, size=10)
    treino = treino.tolist()
    return treino


def gerar_aluno():
    """
    Retorna uma tupla de 2 items para representar um aluno no formato (horarios_disponíveis, treino).

    Utiliza as funções `gerar_horarios` e `gerar_treino` para gerar os horários e o treino do aluno.

    Returns:
        tuple: Uma tupla contendo os horários disponíveis e o treino do aluno.
    """
    horarios = gerar_horarios()
    treino = gerar_treino()
    aluno = (horarios, treino)
    return aluno


def gerar_alunos():
    """
    Retorna uma lista de 90 a 130 alunos, representando a quantidade variável de alunos.

    Gera uma lista de alunos utilizando a função `gerar_aluno` para cada aluno, com o número de 
    alunos variando entre 90 e 130.

    Returns:
        list: Lista de alunos, onde cada aluno é uma tupla com horários e treino.
    """
    rng = np.random.default_rng()
    qntd_alunos = rng.integers(low=90, high=130, endpoint=True)
    alunos = []
    for x in range(qntd_alunos):
        alunos.append(gerar_aluno())
    return alunos


def comparar_treino_recomendacao(treino1, treino2):
    """
    Retorna uma lista com o número de colisões de máquina entre dois treinos, 
    cada posição da lista representa a máquina do seu dígito.

    A comparação é feita verificando se os elementos de `treino1` e `treino2` se repetem.
    Esta função é usada para calcular a nota de recomendação de um horário para um aluno.	

    Args:
        treino1 (list): O primeiro treino a ser comparado.
        treino2 (list): O segundo treino a ser comparado.

    Returns:
        list: Lista com o número de colisões de máquina em cada posição (máquina).
    """
    resultado = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(10):
        for y in range(10):
            if(treino1[x] == treino2[y]):
                resultado[treino1[x]] +=1
    return resultado


def comparar_treino(treino1, treino2):
    """
    Retorna uma lista com o número de colisões de máquina entre dois treinos, 
    pulando elementos duplicados do primeiro treino.

    A comparação é feita entre `treino1` (sem valores duplicados) e `treino2`.

    Args:
        treino1 (list): O primeiro treino a ser comparado, sem elementos duplicados.
        treino2 (list): O segundo treino a ser comparado.

    Returns:
        list: Lista com o número de colisões de máquina em cada posição (máquina).
    """
    resultado = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    treino_sem_dupes = list(set(treino1))
    for x in range(len(treino_sem_dupes)):
        for y in range(10):
            if(treino_sem_dupes[x] == treino2[y]):
                resultado[treino_sem_dupes[x]] +=1
    return resultado


def nota_recomendacao(treinos_horario, treino_aluno):
    """
    Analisa o treino quando comparado aos outros alunos do horário para dar uma nota.

    A função compara o `treino_aluno` com os treinos de outros alunos no mesmo horário e soma as colisões.

    Args:
        treinos_horario (list): Lista de treinos dos alunos no mesmo horário.
        treino_aluno (list): O treino do aluno que está sendo comparado.

    Returns:
        int: A nota de recomendação baseada nas colisões de máquinas.
    """
    nota = 0
    tam = len(treinos_horario)
    for x in range(tam):
        comparacao = comparar_treino_recomendacao(treinos_horario[x], treino_aluno)
        nota += np.sum(comparacao)
    return nota


def bad_rng_check(treino):
    """
    Recebe um treino e retorna True quando alguma máquina aparece no treino mais de 3 vezes.

    Essa verificação é feita para garantir que não haja valores repetidos demais no treino de um aluno.

    Args:
        treino (list): O treino do aluno, representado como uma lista de inteiros.

    Returns:
        bool: Retorna True se algum número no treino aparecer mais de 3 vezes, False caso contrário.
    """
    for x in range(10):
        indexes = len(np.where(treino == x)[0])
        if (indexes > 3):
            return True
    return False


def index_aluno_aleatorio(individuo):
    """
    Retorna uma lista contendo o horário em que está alocado e o index neste horário de um aluno aleatório de um indivíduo.

    Args:
        individuo (list): O indivíduo.

    Returns:
        list: Uma lista contendo o horário e o índice do aluno [horario, index].
    """
    index_aluno = []
    rng = np.random.default_rng()
    index_horario = rng.integers(low=0, high=6)
    if(len(individuo[index_horario]) > 0):
        index_aluno_no_horario = rng.integers(low=0, high=len(individuo[index_horario]))
        index_aluno.append(index_horario)
        index_aluno.append(index_aluno_no_horario)
    else:
        index_aluno = index_aluno_aleatorio(individuo)
    return index_aluno


def alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2):
    """
    Retorna um boolean dizendo se 2 alunos são trocáveis (estão em 2 horários diferentes em que ambos têm disponibilidade).

    Args:
        aluno1 (tuple): O primeiro aluno, contendo horários e treino.
        index_aluno1 (list): O índice do aluno1 em seu horário atual.
        aluno2 (tuple): O segundo aluno, contendo horários e treino.
        index_aluno2 (list): O índice do aluno2 em seu horário atual.

    Returns:
        bool: Retorna True se os alunos podem ser trocados, False caso contrário.
    """
    horarios_aluno1 = aluno1[0]
    horarios_aluno2 = aluno2[0]
    horarios_comuns = [x for x in horarios_aluno1 if x in horarios_aluno2]
    if (index_aluno1[0] != index_aluno2[0] and ((index_aluno1[0] + 12) in horarios_comuns) and ((index_aluno2[0] + 12) in horarios_comuns)):
        return True
    return False


def gerar_horarios():
    """
    Retorna uma lista de horários para representar a disponibilidade de um aluno.

    o aluno estará disponível em pelo menos um horário.

    Returns:
        list: Lista com os horários disponíveis para o aluno.
    """
    rng = np.random.default_rng()
    disponibilidade = rng.integers(low=1, high=6, endpoint=True)
    horarios = rng.choice([12, 13, 14, 15, 16, 17], disponibilidade, replace=False)
    horarios = horarios.tolist()
    return horarios


def calcular_colisões(treinos):
    """
    Calcula o número de colisões em uma lista de alunos usando `comparar_treino()`.

    A função compara o treino de cada aluno com os outros e retorna uma lista com as colisões para cada máquina.

    Uma especificidade da implementação é de no loop onde um aluno x é comparado com todos os outros o aluno x será tratado como se tivesse cada
    máquina no máximo uma vez em seu treino, ou seja, se uma máquina aparecer 2 vezes em seu treino ele será tratado como se fosse 1 em seu loop.
    Isto ocorre pois um aluno não compete consigo mesmo por uma máquina. Quando outros alunos forem comparados com o aluno x em
    seus respectivos loops o aluno x será processado normalmente.


    Args:
        treinos (list): Lista de treinos dos alunos.

    Returns:
        list: Lista com o número de colisões para cada máquina.
    """
    colisoes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(len(treinos)):
        treino_testado = treinos[x][1]
        treinos_testado = treinos.copy()
        treinos_testado.pop(x)
        for y in range(len(treinos_testado)):
            colisoes = np.add(colisoes, (comparar_treino(treino_testado, treinos_testado[y][1])))
    return colisoes


def encontrar_aluno_horario(aluno, horario):
    """
    Retorna o índice de um aluno em um horário, retorna None caso o aluno não esteja no horário.

    Args:
        aluno (tuple): O aluno que está sendo procurado.
        horario (list): O horário onde procurar o aluno.

    Returns:
        int or None: Retorna o índice do aluno no horário ou None caso o aluno não esteja presente.
    """
    try:
        index_horario = horario.index(aluno)
        return index_horario
    except ValueError:
        return None


def encontrar_aluno_individuo(aluno, individuo):
    """
    Retorna o horário em que está um aluno em um indivíduo, retorna None caso o aluno tenha sido descartado.

    Args:
        aluno (tuple): O aluno a ser encontrado.
        individuo (list): O individuo onde o aluno deve ser procurado.

    Returns:
        int or None: O horário onde o aluno foi encontrado ou None se o aluno não foi encontrado.
    """
    index_horario = None
    horario = None
    for x in range(6):
        if (index_horario == None):
            index_horario = encontrar_aluno_horario(aluno, individuo[x])
            if (index_horario != None):
                horario = x
                break
    return horario


def anexar_aluno(index_horario, aluno, individuo, repescagem):
    """
    Adiciona um aluno a um horário caso haja espaço. Se não houver espaço, o aluno é adicionado à lista de repescagem.

    Args:
        index_horario (int or None): O índice do horário onde o aluno deve ser adicionado, None representa que o aluno não foi alocado a um horário no indivíduo pai.
        aluno (tuple): O aluno a ser adicionado.
        individuo (list): O individuo.
        repescagem (list): Lista de alunos para repescagem caso não haja espaço no horário.

    Returns:
        list: O indivíduo atualizado com o aluno adicionado ao horário.
    """
    if (index_horario == None):
        repescagem.append(aluno)
    elif(len(individuo[index_horario]) < 20):
        individuo[index_horario].append(aluno)
    else:
        repescagem.append(aluno)
    return individuo


def repescagem(individuo, repescagem):
    """
    Distribui no indivíduo os alunos de uma lista de repescagem.

    A função tenta realocar alunos da repescagem para horários disponíveis no indivíduo.

    Args:
        individuo (list): O indivíduo.
        repescagem (list): Lista de alunos para repescagem.
    """
    x = 0
    for _ in range(len(repescagem)):
        x = x + 1
        aluno = repescagem.pop(0)
        horarios_possiveis = (aluno[0].copy())
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


def imprimir(individuo):
    """
    Método auxiliar usado para imprimir um indivíduo.

    A função imprime as listas em um indivíduo, mostrando os alunos agendados para cada horário.

    Args:
        individuo (list): O individuo.

    """
    for horario, elem in enumerate(individuo):
        if (type(elem) == list):
            print(f'Alunos agendados às {(horario + 12)}h: ')
            imprimir(elem)
        else:
            print(elem)
    print()
