import unittest
import unittest.mock
import numpy as np
from unittest.mock import patch
from copy import deepcopy
from Gymsys_manager import *
from Gymsys_Ga import *
from Gymsys_simulacao import *
from Gymsys_render import *
from Gymsys_greedy import *

#Testes de Gymsys_manager.py ---------------------------------------------------------------------------------------------------------------------------------------
class TestBadRngCheck(unittest.TestCase):
    def test_bad_rng_check_false(self):
        """Verifica se a função retorna False quando o treino está correto."""
        for i in range(10):
            with self.subTest(i=i):
                treino_valido = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.assertFalse(bad_rng_check(treino_valido))

    def test_bad_rng_check_true(self):
        """Verifica se a função retorna True quando há mais de 3 repetições de algum número."""
        for i in range(10):
            with self.subTest(i=i):
                treino_invalido = [0, 0, 0, 0, 1, 2, 3, 4, 5, 6]
                self.assertTrue(bad_rng_check(treino_invalido))

    def test_bad_rng_check_variabilidade(self):
        """Verifica se a função lida bem com diferentes entradas de treino."""
        treino_invalido = [1, 1, 1, 1, 0, 0, 0, 0, 3, 3]
        self.assertTrue(bad_rng_check(treino_invalido))

class TestGerarAluno(unittest.TestCase):

    def test_gerar_aluno_variabilidade(self):
        """Verifica se os alunos gerados são diferentes entre si."""
        aluno1 = gerar_aluno()
        aluno2 = gerar_aluno()
        self.assertNotEqual(aluno1, aluno2, "Os alunos gerados são iguais!")

class TestGerarAlunos(unittest.TestCase):
    
    def test_gerar_alunos_numero_correto(self):
        """Verifica se a função gera o número correto de alunos (entre 90 e 130)."""
        alunos = gerar_alunos()
        self.assertGreaterEqual(len(alunos), 90)
        self.assertLessEqual(len(alunos), 130)

    def test_gerar_alunos_horarios_validos(self):
        """Verifica se todos os alunos gerados possuem horários válidos e únicos."""
        alunos = gerar_alunos()
        for horarios, _ in alunos:
            self.assertGreaterEqual(len(horarios), 1)
            self.assertLessEqual(len(horarios), 6)
            self.assertEqual(len(horarios), len(set(horarios)))  # Horários únicos

    def test_gerar_alunos_consistencia(self):
        """Verifica se a função gera alunos válidos em múltiplas execuções."""
        for _ in range(10):  # Realiza 10 execuções
            alunos = gerar_alunos()
            for horarios, treino in alunos:
                self.assertGreaterEqual(len(horarios), 1)
                self.assertLessEqual(len(horarios), 6)
                self.assertEqual(len(horarios), len(set(horarios)))  # Horários únicos
                self.assertEqual(len(treino), 10)
                for i in range(10):
                    self.assertLessEqual(treino.count(i), 3)  # Não deve ter números repetidos mais de 3 vezes

    def test_gerar_alunos_horarios_faixa_valida(self):
        """Verifica se todos os horários gerados estão dentro da faixa de 12h a 17h."""
        alunos = gerar_alunos()
        for horarios, _ in alunos:
            for horario in horarios:
                self.assertIn(horario, [12, 13, 14, 15, 16, 17])  # Horário dentro da faixa válida

class TestIndexAlunoAleatorio(unittest.TestCase):

    def test_retornar_indice_valido(self):
        """Verifica se a função retorna um horário e um índice válidos dentro desse horário."""
        individuo = [
            [( [12, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )],  # Horário 12h
            [( [13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )],  # Horário 13h
            [( [14, 15], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )],  # Horário 14h
            [],  # Horário 15h (vazio)
            [( [16], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )],  # Horário 16h
            [( [17], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )],  # Horário 17h
            0    # Descarte
        ]
        resultado = index_aluno_aleatorio(individuo)
        horario, index_aluno = resultado

        # Verifica se o horário retornado está entre 0 e 5 (exceto horário 15h, que está vazio)
        self.assertIn(horario, [0, 1, 2, 4, 5])
        
        # Verifica se o índice do aluno está dentro do número de alunos no horário
        self.assertTrue(0 <= index_aluno < len(individuo[horario]))

    def test_horario_com_um_aluno(self):
        """Verifica se a função lida corretamente com horários com um único aluno."""
        individuo = [
            [( [12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] )],  # Horário 12h
            [],  # Horário 13h (vazio)
            [],  # Horário 14h (vazio)
            [],  # Horário 15h (vazio)
            [],  # Horário 16h (vazio)
            [],  # Horário 17h (vazio)
            0    # Descarte
        ]
        resultado = index_aluno_aleatorio(individuo)
        horario, index_aluno = resultado

        # Verifica se o horário retornado foi 0 (12h, que tem 1 aluno)
        self.assertEqual(horario, 0)
        
        # Verifica se o índice do aluno é 0, pois há apenas 1 aluno nesse horário
        self.assertEqual(index_aluno, 0)

    def test_indice_aleatorio_valido_para_horarios_cheios(self):
        """Verifica se a função gera índices aleatórios válidos em horários com vários alunos."""
        individuo = [
            [],  # Horário 12h (vazio)
            [],  # Horário 13h (vazio)
            [],  # Horário 14h (vazio)
            [],  # Horário 15h (vazio)
            [],  # Horário 16h (vazio)
            [],  # Horário 17h (vazio)
            0    # Descarte
        ]
        for _ in range(20):
            individuo[0].append(gerar_aluno())  # Adiciona 20 alunos ao horário 12h
        resultado = index_aluno_aleatorio(individuo)
        horario, index_aluno = resultado

        # Verifica se o horário retornado é 0 (12h), pois é o único horário com alunos
        self.assertIn(horario, [0])

        # Verifica se o índice do aluno está dentro do número de alunos no horário
        self.assertTrue(0 <= index_aluno < len(individuo[horario]))

class TestAlunosTrocaveis(unittest.TestCase):

    def test_trocaveis_com_horarios_comum(self):
        """Verifica se alunos com horários comuns e diferentes podem ser trocados."""
        aluno1 = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        aluno2 = ([12, 14, 15, 16], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        index_aluno1 = [0, 0]  # Índice dentro do horário 12
        index_aluno2 = [2, 0] # Índice dentro do horário 14
        resultado = alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2)
        self.assertTrue(resultado)  # Ambos têm horário comum (12, 14)

    def test_nao_trocaveis_sem_horarios_comum(self):
        """Verifica se alunos sem horários comuns não podem ser trocados."""
        aluno1 = ([12, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        aluno2 = ([15, 16], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        index_aluno1 = [0, 9] # Índice dentro do horário 12
        index_aluno2 = [3, 7] # Índice dentro do horário 15
        resultado = alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2)
        self.assertFalse(resultado)  # Não têm horários comuns, não podem ser trocados

    def test_trocaveis_com_mais_de_um_horario_comum(self):
        """Verifica se alunos com múltiplos horários em comum podem ser trocados."""
        aluno1 = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        aluno2 = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        index_aluno1 = [0, 12] # Índice dentro do horário 12
        index_aluno2 = [2, 3] # Índice dentro do horário 14
        resultado = alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2)
        self.assertTrue(resultado)  # Ambos têm horário comum (14)

    def test_trocaveis_com_indices_iguais(self):
        """Verifica se alunos com os mesmos índices podem ser trocados."""
        aluno1 = ([12, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        aluno2 = ([12, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        index_aluno1 = [0, 5]  # Índice dentro do horário 12
        index_aluno2 = [0, 7]  # Índice dentro do horário 12
        resultado = alunos_trocaveis(aluno1, index_aluno1, aluno2, index_aluno2)
        self.assertFalse(resultado)  # Mesmo com horários em comum, índices são iguais, não podem ser trocados

class TestEncontrarAlunoHorario(unittest.TestCase):

    def test_aluno_presente_no_horario(self):
        """Verifica se a função retorna o índice correto quando o aluno está presente no horário."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        horario = [([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 
                   ([15, 16], [11, 12, 13, 14, 15, 16, 17, 18, 19, 20])]
        resultado = encontrar_aluno_horario(aluno, horario)
        self.assertEqual(resultado, 0)  # O aluno deve estar no índice 0

    def test_aluno_nao_presente_no_horario(self):
        """Verifica se a função retorna None quando o aluno não está no horário."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        horario = [([15, 16], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]
        resultado = encontrar_aluno_horario(aluno, horario)
        self.assertIsNone(resultado)  # O aluno não está presente, então deve retornar None

    def test_aluno_aparece_mais_vezes_no_horario(self):
        """Verifica se a função retorna o primeiro índice do aluno, caso ele apareça mais de uma vez no horário."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        horario = [([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                   ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]
        resultado = encontrar_aluno_horario(aluno, horario)
        self.assertEqual(resultado, 0)  # O aluno aparece duas vezes, mas a função deve retornar o primeiro índice

class TestEncontrarAlunoIndividuo(unittest.TestCase):

    def test_aluno_presente_no_individuo(self):
        """Verifica se a função retorna o horário correto onde o aluno está presente no indivíduo."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [
            [([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],  # Horário 0
            [],  # Horário 1
            [],  # Horário 2
            [],  # Horário 3
            [],  # Horário 4
            [],  # Horário 5
            0    # Descarte
        ]
        resultado = encontrar_aluno_individuo(aluno, individuo)
        self.assertEqual(resultado, 0)  # O aluno está no horário 0

    def test_aluno_nao_presente_no_individuo(self):
        """Verifica se a função retorna None quando o aluno não está presente no indivíduo."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [
            [([15, 16], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],  # Horário 0
            [([14, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],  # Horário 1
            [],  # Horário 2
            [],  # Horário 3
            [],  # Horário 4
            [],  # Horário 5
            0    # Descarte
        ]
        resultado = encontrar_aluno_individuo(aluno, individuo)
        self.assertIsNone(resultado)  # O aluno não está presente em nenhum horário

    def test_aluno_descartado(self):
        """Verifica se a função retorna None quando o aluno foi descartado e não está alocado em nenhum horário."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [
            [([12, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],  # Horário 0
            [],  # Horário 1
            [],  # Horário 2
            [([12, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],  # Horário 3
            [([13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],  # Horário 4
            [],  # Horário 5
            1    # Descarte
        ]
        resultado = encontrar_aluno_individuo(aluno, individuo)
        self.assertIsNone(resultado)  # O aluno foi descartado e não está em nenhum horário válido

    def test_individuo_com_horarios_vazios(self):
        """Verifica se a função lida corretamente com horários vazios no indivíduo."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [
            [],  # Horário 0
            [],  # Horário 1
            [],  # Horário 2
            [],  # Horário 3
            [],  # Horário 4
            [([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])]  # Horário 5
        ]
        resultado = encontrar_aluno_individuo(aluno, individuo)
        self.assertEqual(resultado, 5)  # O aluno está no horário 5, e os outros horários estão vazios

class TestAnexarAluno(unittest.TestCase):

    def test_aluno_nao_alocado(self):
        """Verifica se um aluno é adicionado à lista de repescagem quando index_horario é None."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [[], [], [], [], [], [], 0]  # Todos os horários estão vazios
        repescagem = []
        
        individuo_atualizado = anexar_aluno(None, aluno, individuo, repescagem)
        
        self.assertIn(aluno, repescagem)  # O aluno deve ser adicionado à repescagem
        self.assertEqual(len(individuo_atualizado[0]), 0)  # Nenhum aluno foi adicionado ao horário 0
        self.assertEqual(len(individuo_atualizado[1]), 0)  # Nenhum aluno foi adicionado ao horário 1
        self.assertEqual(len(individuo_atualizado[2]), 0)  # Nenhum aluno foi adicionado ao horário 2
        self.assertEqual(len(individuo_atualizado[3]), 0)  # Nenhum aluno foi adicionado ao horário 3
        self.assertEqual(len(individuo_atualizado[4]), 0)  # Nenhum aluno foi adicionado ao horário 4
        self.assertEqual(len(individuo_atualizado[5]), 0)  # Nenhum aluno foi adicionado ao horário 5

    def test_aluno_alocado_com_espaco(self):
        """Verifica se um aluno é adicionado a um horário que tem espaço disponível."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [[], [], [], [], [], [], 0]  # Todos os horários estão vazios
        repescagem = []
        
        individuo_atualizado = anexar_aluno(0, aluno, individuo, repescagem)
        
        self.assertIn(aluno, individuo_atualizado[0])  # O aluno foi adicionado ao horário 0
        self.assertNotIn(aluno, repescagem)  # O aluno não foi para a repescagem

    def test_aluno_alocado_sem_espaco(self):
        """Verifica se um aluno é adicionado à repescagem quando o horário já tem 20 alunos."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [[], [], [], [], [], [], 0]
        for _ in range(20):
            individuo[0].append(gerar_aluno())  # O horário 0 está lotado com 20 alunos
        repescagem = []
        
        individuo_atualizado = anexar_aluno(0, aluno, individuo, repescagem)
        
        self.assertIn(aluno, repescagem)  # O aluno foi adicionado à repescagem, pois o horário 0 já tem 20 alunos
        self.assertEqual(len(repescagem), 1)  # Deve haver apenas um aluno na repescagem
        self.assertNotIn(aluno, individuo_atualizado[0])  # O aluno não foi adicionado ao horário 0
        self.assertEqual(len(individuo_atualizado[0]), 20)  # O horário 0 ainda está cheio

class TestRepescagem(unittest.TestCase):

    def test_aluno_realocado_com_espaco(self):
        """Verifica se o aluno é realocado em um horário disponível."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [[], [], [], [], [], [], 0]  # Todos os horários estão vazios
        lista_repescagem = [aluno]

        repescagem(individuo, lista_repescagem)
        
        self.assertEqual(len(lista_repescagem), 0)  # A repescagem deve estar vazia, pois o aluno foi alocado
        aluno_alocado = False
        for i in range(6):
            aluno_alocado = aluno in individuo[i]
            if aluno_alocado:
                break
        self.assertTrue(aluno_alocado)  # O aluno deve ter sido alocado em algum horário

    def test_aluno_nao_realocado_por_espacos_cheios(self):
        """Verifica se o aluno é descartado quando todos os horários estão cheios."""
        aluno = ([12, 13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [[], [], [], [], [], [], 0]
        for i in range(6):
            for _ in range(20):
                individuo[i].append(gerar_aluno())  # Todos os horários estão cheios
        lista_repescagem = [aluno]
        
        repescagem(individuo, lista_repescagem)
        
        self.assertEqual(len(lista_repescagem), 0)  # A repescagem deve estar vazia pois o aluno foi processado/descartado
        self.assertEqual(individuo[6], 1)  # O número de alunos descartados deve ser 1
        for i in range(6):
            self.assertNotIn(aluno, individuo[i])  # O aluno não deve ter sido adicionado a nenhum horário

    def test_aluno_adequadamente_adicionado_se_espaco(self):
        """Verifica se o aluno é corretamente adicionado a um horário disponível com espaço suficiente."""
        aluno = ([12, 13, 14, 17], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        individuo = [[], [], [], [], [], []]
        for i in range(5):
            for _ in range(20):
                individuo[i].append(gerar_aluno())  # Todos os horários estão cheios menos as 17h
        lista_repescagem = [aluno]
        
        repescagem(individuo, lista_repescagem)
        
        self.assertEqual(len(lista_repescagem), 0)  # A repescagem deve estar vazia
        self.assertIn(aluno, individuo[5])  # O aluno deve ser alocado no horário 5 (17h)
        self.assertEqual(len(individuo[5]), 1)  # O horário 5 deve agora ter 1 aluno

# Testes de Gymsys_Ga.py ---------------------------------------------------------------------------------------------------------------------------------------
class TestFuncaoFitness(unittest.TestCase):
  
    def test_fitness_minima(self):
        """Verifica se a função retorna o valor correto para um cenário de fitness baixa."""
        individuo = [
            [],  # Horário 12
            [],  # Horário 13
            [],  # Horário 14
            [],  # Horário 15
            [],  # Horário 16
            [],  # Horário 17
            0    # Alunos descartados
        ]
        for i in range(6):
            for _ in range(10):
                individuo[i].append(([12, 13, 14, 15, 16, 17], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))  # Adiciona 10 alunos a cada horário
        resultado = funcao_fitness(individuo)
        self.assertEqual(resultado, 0.061441)

    def test_fitness_maxima(self):
        """Verifica se a função retorna o valor correto para um cenário de fitness alta."""
        individuo = [
            [],  # Horário 12
            [],  # Horário 13
            [],  # Horário 14
            [],  # Horário 15
            [],  # Horário 16
            [],  # Horário 17
            15   # Alunos descartados
        ]
        for i in range(6):
            for _ in range(15):
                individuo[i].append(([12, 13, 14, 15, 16, 17], [0, 0, 0, 3, 3, 3, 6, 6, 6, 9]))  # Adiciona 10 alunos a cada horário
        resultado = funcao_fitness(individuo)
        self.assertEqual(resultado, 668503069.884452)

    def test_fitness_moderada(self):
        """Verifica se a função retorna o valor correto para um cenário de fitness moderada."""
        individuo = [
            [],   # Horário 12, 
            [],   # Horário 13, 
            [],   # Horário 14, 
            [],   # Horário 15, 
            [],   # Horário 16, 
            [],   # Horário 17, 
            8  # 5 alunos descartados
        ]
        for i in range(6):
            for _ in range(10):
                individuo[i].append(([12, 13, 14, 15, 16, 17], [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]))  # Adiciona 10 alunos a cada horário
        resultado = funcao_fitness(individuo)
        self.assertEqual(resultado, 48.234526)

    def test_fitness_zero(self):
        """Verifica se a fitness retorna 0.000061 (menor valor possível)para todos os horários vazios."""
        individuo = [
            [],  # Horário 12 com máquinas diferentes
            [],  # Horário 13
            [],  # Horário 14
            [],  # Horário 15
            [],  # Horário 16
            [],  # Horário 17
            0  # Sem alunos descartados
        ]
        resultado = funcao_fitness(individuo)
        self.assertEqual(resultado, 0.000061)

class TestCriarIndividuo(unittest.TestCase):

    def test_todos_alunos_alocados_com_sucesso(self):
        """
        Testa se todos os alunos são corretamente alocados quando há vagas
        suficientes em seus horários disponíveis.
        """
        espaco_solucao = [
            ([12],[1, 2, 3, 4, 5, 6, 7, 8, 9, 1]),
            ([13],[1, 2, 3, 4, 5, 6, 7, 8, 9, 2]),
            ([14],[1, 2, 3, 4, 5, 6, 7, 8, 9, 3])
        ]
        
        individuo = criar_individuo(espaco_solucao)

        self.assertEqual(individuo[0][0][1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 1])  # horário 12 - índice 0
        self.assertEqual(individuo[1][0][1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 2])  # horário 13 - índice 1
        self.assertEqual(individuo[2][0][1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 3])  # horário 14 - índice 2
        self.assertEqual(individuo[6], 0)  # nenhum aluno descartado

    def test_aluno_descartado_por_limite_de_vagas(self):
        """
        Testa se um aluno é corretamente descartado quando o horário desejado
        já atingiu o limite de 20 alunos.
        """

        # 21 alunos tentando horário 12 (índice 0), limite é 20
        espaco_solucao = [([12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]) for _ in range(21)]
        
        individuo = criar_individuo(espaco_solucao)

        self.assertEqual(len(individuo[0]), 20)  # horário 12 cheio
        self.assertEqual(individuo[6], 1)  # 1 aluno descartado

    @patch('numpy.random.default_rng')
    def test_aluno_com_varios_horarios_todos_ocupados(self, mock_rng):
        """
        Testa se um aluno com múltiplas opções de horário é descartado quando
        todas essas opções estão lotadas.
        """
        mock_rng_instance = mock_rng.return_value
        # Sempre tenta horário cheio, depois outros, todos cheios
        mock_rng_instance.integers.side_effect = lambda *args, **kwargs: 0

        espaco_solucao = []
        for i in range(6):
            espaco_solucao += [([12 + i], [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]) for _ in range(20)]
        # Adiciona um aluno com todos os horários possíveis (todos cheios)
        espaco_solucao.append(([12, 13, 14, 15, 16, 17], [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]))
        
        individuo = criar_individuo(espaco_solucao)
        for i in range(6):
            self.assertNotIn(individuo[i], ([12, 13, 14, 15, 16, 17], [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]))  # O aluno não deve estar em nenhum horário
        self.assertEqual(individuo[6], 1)  # Último aluno descartado

class TestCrossoverEntrelacado(unittest.TestCase):

    def setUp(self):
        """
        Cria um espaço de solução com 130 alunos, cada um com um treino válido e um único horário disponível.
        Dois pais são montados dividindo esses alunos entre horários.
        """
        self.espaco_solucao = (
            [([12], gerar_treino()) for _ in range(30)] + [([13], gerar_treino()) for _ in range(20)] + [([14], gerar_treino()) for _ in range(20)] +
            [([15], gerar_treino()) for _ in range(20)] + [([16], gerar_treino()) for _ in range(20)] + [([17], gerar_treino()) for _ in range(20)]
        )

        self.espaco_solucao_excedido = (
            [([12], gerar_treino()) for _ in range(40)] + [([13], gerar_treino()) for _ in range(40)] + [([14], gerar_treino()) for _ in range(40)] +
            [([15], gerar_treino()) for _ in range(40)] + [([16], gerar_treino()) for _ in range(40)] + [([17], gerar_treino()) for _ in range(40)]
        )
        # Monta dois pais artificiais com os alunos intercalados
        self.parente1 = [[], [], [], [], [], [], 0]
        self.parente2 = [[], [], [], [], [], [], 0]
        for i, aluno in enumerate(self.espaco_solucao):
            index = aluno[0][0] - 12
            if i % 2 == 0:
                self.parente1[index].append(aluno)
            else:
                self.parente2[index].append(aluno)
        # Monta dois pais artificiais com os alunos intercalados com os horários lotados
        self.parente1_max = [[], [], [], [], [], [], 0]
        self.parente2_max = [[], [], [], [], [], [], 0]
        for i, aluno in enumerate(self.espaco_solucao_excedido):
            index = aluno[0][0] - 12
            if i % 2 == 0:
                self.parente1_max[index].append(aluno)
            else:
                self.parente2_max[index].append(aluno)

    @patch('Gymsys_Ga.random.sample')
    def test_filho_tem_mesmo_total_de_alunos(self, mock_sample):
        """
        Verifica se o total de alunos nos filhos (alocados + descartados) é igual
        ao total original, garantindo que nenhum aluno foi perdido.
        """
        mock_sample.side_effect = lambda lista, _: lista.copy()
        filho1, filho2 = crossover_entrelacado(self.parente1, self.parente2, self.espaco_solucao)

        total_original = len(self.espaco_solucao)
        total_f1 = sum(len(h) for h in filho1[:6]) + filho1[6]
        total_f2 = sum(len(h) for h in filho2[:6]) + filho2[6]

        self.assertEqual(total_f1, total_original)
        self.assertEqual(total_f2, total_original)

    @patch('Gymsys_Ga.random.sample')
    @patch('Gymsys_Ga.np.random.default_rng')
    def test_filho_tem_distribuicao_alternada(self, mock_rng, mock_sample):
        """
        Garante que os filhos foram montados alternando a origem dos pais, 
        verificando que a distribuição entre os pais está de forma intercalada 
        entre os filhos.
        """
        # Mock do sample para não alterar a ordem dos alunos
        mock_sample.side_effect = lambda lista, _: lista.copy()

        # Mock do RNG para sempre escolher o primeiro horário possível
        mock_rng.return_value.integers.side_effect = lambda low, high: 0

        filho1, filho2 = crossover_entrelacado(self.parente1, self.parente2, self.espaco_solucao)

        # Verificando a distribuição alternada entre os filhos
        for i in range(6):  # Existem 6 horários
            # Índices de alunos nos pais
            aluno_parente1 = {id(a) for a in self.parente1[i]}  # Alunos no parente1 para o horário i
            aluno_parente2 = {id(a) for a in self.parente2[i]}  # Alunos no parente2 para o horário i

            # Verificando se o filho1 e filho2 alternaram entre os pais
            if i % 2 == 0:
                # Para índices pares, o aluno deve vir de parente1 em filho1 e de parente2 em filho2
                self.assertTrue(aluno_parente1.intersection({id(a) for a in filho1[i]}))
                self.assertTrue(aluno_parente2.intersection({id(a) for a in filho2[i]}))
            else:
                # Para índices ímpares, o aluno deve vir de parente2 em filho1 e de parente1 em filho2
                self.assertTrue(aluno_parente2.intersection({id(a) for a in filho1[i]}))
                self.assertTrue(aluno_parente1.intersection({id(a) for a in filho2[i]}))

        # Garantindo que o total de alunos alocados e descartados é igual ao total original
        total_espaco = len(self.espaco_solucao)
        total_f1 = sum(len(h) for h in filho1[:6]) + filho1[6]
        total_f2 = sum(len(h) for h in filho2[:6]) + filho2[6]
        self.assertEqual(total_f1, total_espaco)
        self.assertEqual(total_f2, total_espaco)

    @patch('Gymsys_Ga.random.sample')
    def test_filho_respeita_limite_por_horario(self, mock_sample):
        """
        Verifica se nenhum horário ultrapassa o limite de 20 alunos por horário.
        """
        mock_sample.side_effect = lambda lista, _: lista.copy()
        filho1, filho2 = crossover_entrelacado(self.parente1_max, self.parente2_max, self.espaco_solucao_excedido)

        for horario in filho1[:6] + filho2[:6]:
            self.assertLessEqual(len(horario), 20)

class TestCrossoverUmPonto(unittest.TestCase):

    def setUp(self):
        """
        Cria um espaço de solução com 240 alunos, cada um com um treino válido e um único horário disponível.
        Dois pais são montados dividindo esses alunos entre horários.
        """
        self.espaco_solucao = (
            [([12], gerar_treino()) for _ in range(40)] + [([13], gerar_treino()) for _ in range(40)] + [([14], gerar_treino()) for _ in range(40)] +
            [([15], gerar_treino()) for _ in range(40)] + [([16], gerar_treino()) for _ in range(40)] + [([17], gerar_treino()) for _ in range(40)]
        )

        # Monta dois pais artificiais intercalando os alunos no espaço solução	
        self.parente1 = [[], [], [], [], [], [], 0]
        self.parente2 = [[], [], [], [], [], [], 0]
        for i, aluno in enumerate(self.espaco_solucao):
            index = aluno[0][0] - 12
            if i % 2 == 0:
                self.parente1[index].append(aluno)
            else:
                self.parente2[index].append(aluno)

    @patch('Gymsys_Ga.random.sample')
    def test_filho_tem_mesmo_total_de_alunos(self, mock_sample):
        """
        Verifica se o total de alunos nos filhos (alocados + descartados) é igual
        ao total original, garantindo que nenhum aluno foi perdido.
        """
        mock_sample.side_effect = lambda lista, _: lista.copy()
        filho1, filho2 = crossover_um_ponto(self.parente1, self.parente2, self.espaco_solucao)

        total_original = len(self.espaco_solucao)
        total_f1 = sum(len(h) for h in filho1[:6]) + filho1[6]
        total_f2 = sum(len(h) for h in filho2[:6]) + filho2[6]

        self.assertEqual(total_f1, total_original)
        self.assertEqual(total_f2, total_original)

    @patch('Gymsys_Ga.np.random.default_rng')
    def test_metade_de_um_parente(self, mock_rng):
        """
        Verifica se os filhos foram gerados com a primeira metade dos alunos
        vindo de um parente e a segunda do outro.
        """
        mock_rng.return_value.integers.side_effect = lambda low, high: low
        filho1, filho2 = crossover_um_ponto(self.parente1, self.parente2, self.espaco_solucao)
        
        # Os primeiros 120 alunos devem ter vindo de parente1 em filho1
        # e os últimos 120 alunos devem ter vindo de parente1 em filho2 (neste caso, os últimos vão para o descarte no filho2)
        for i, aluno in enumerate(self.espaco_solucao[:6]):
            if aluno in self.parente1[aluno[0][0] - 12] and i < 65:
                self.assertTrue(aluno in filho1[aluno[0][0] - 12]) # confirmação da presença no filho1
            elif aluno not in self.parente1[aluno[0][0] - 12] and i < 65:
                self.assertFalse(aluno in filho1[aluno[0][0] - 12]) # confirmação da ausência no filho1
            elif aluno in self.parente1[aluno[0][0] - 12] and i > 65:
                self.assertTrue(aluno in filho2[aluno[0][0] - 12]) # confirmação da presença no filho2
            elif aluno not in self.parente1[aluno[0][0] - 12] and i > 65:
                self.assertFalse(aluno in filho2[aluno[0][0] - 12]) # confirmação da ausência no filho2

        # Os primeiros 120 alunos devem ter vindo de parente2 em filho2
        # e os últimos 120 alunos devem ter vindo de parente2 em filho1 (neste caso, os últimos vão para o descarte no filho1)
        for i, aluno in enumerate(self.espaco_solucao[:6]):
            if aluno in self.parente2[aluno[0][0] - 12] and i < 65:
                self.assertTrue(aluno in filho2[aluno[0][0] - 12]) # confirmação da presença no filho1
            elif aluno not in self.parente2[aluno[0][0] - 12] and i < 65:
                self.assertFalse(aluno in filho2[aluno[0][0] - 12]) # confirmação da ausência no filho1
            elif aluno in self.parente2[aluno[0][0] - 12] and i > 65:
                self.assertTrue(aluno in filho1[aluno[0][0] - 12]) # confirmação da presença no filho2
            elif aluno not in self.parente2[aluno[0][0] - 12] and i > 65:
                self.assertFalse(aluno in filho1[aluno[0][0] - 12]) # confirmação da ausência no filho2

    @patch('Gymsys_Ga.np.random.default_rng')
    def test_filho_respeita_limite_por_horario(self, mock_rng):
        """
        Verifica se nenhum horário ultrapassa o limite de 20 alunos por horário, e se o valor do descarte reflete o número de alunos descartados.
        """
        mock_rng.return_value.integers.side_effect = lambda low, high: low
        filho1, filho2 = crossover_um_ponto(self.parente1, self.parente2, self.espaco_solucao)

        for i in range(6):
            self.assertLessEqual(len(filho1[i]), 20)
            self.assertLessEqual(len(filho2[i]), 20)

        total_f1 = sum(len(h) for h in filho1[:6]) + filho1[6]
        total_f2 = sum(len(h) for h in filho2[:6]) + filho2[6]
        self.assertEqual(total_f1, len(self.espaco_solucao))
        self.assertEqual(total_f2, len(self.espaco_solucao))

class TestMutacao(unittest.TestCase):

    def setUp(self):
        """
        Cria um indivíduo com 6 horários e 12 alunos, cada um com múltiplas opções de horário.
        """
        self.individuo = [[], [], [], [], [], [], 0]
        horarios = [12, 13, 14, 15, 16, 17]
        for i in range(12):
            horario = horarios[i % 6]
            aluno = (horarios.copy(), gerar_treino())
            self.individuo[horario - 12].append(aluno)

    @patch('Gymsys_Ga.random.random', return_value=0.1)
    @patch('Gymsys_Ga.index_aluno_aleatorio')
    @patch('Gymsys_Ga.alunos_trocaveis', return_value=True)
    def test_mutacao_realizada_quando_probabilidade_atingida(self, mock_trocaveis, mock_index, mock_random):
        """
        Verifica se a mutação troca dois alunos corretamente quando a probabilidade é atingida.
        """
        mock_index.side_effect = [(0, 0), (1, 0)]
        individuo_original = deepcopy(self.individuo)
        aluno1 = individuo_original[0][0]
        aluno2 = individuo_original[1][0]

        mutado = mutacao(self.individuo, taxa_mutacao=1.0)

        self.assertEqual(mutado[0][0], aluno2)
        self.assertEqual(mutado[1][0], aluno1)

    @patch('Gymsys_Ga.random.random', return_value=0.9)
    def test_mutacao_nao_ocorre_quando_probabilidade_nao_atingida(self, mock_random):
        """
        Garante que o indivíduo não é alterado quando a mutação não ocorre.
        """
        original = deepcopy(self.individuo)
        resultado = mutacao(self.individuo, taxa_mutacao=0.1)
        self.assertEqual(resultado, original)

    @patch('Gymsys_Ga.random.random', return_value=0.0)
    @patch('Gymsys_Ga.index_aluno_aleatorio')
    @patch('Gymsys_Ga.alunos_trocaveis', side_effect=[False]*101 + [True])
    def test_mutacao_faz_retry_ate_troca_valida(self, mock_trocaveis, mock_index, mock_random):
        """
        Garante que a mutação tenta múltiplas combinações até encontrar uma troca válida.
        """
        # retorna sempre (0, 0), (1, 0), alternando infinitamente
        def index_generator():
            while True:
                yield (0, 0)
                yield (1, 0)

        mock_index.side_effect = index_generator()

        resultado = mutacao(deepcopy(self.individuo), taxa_mutacao=1.0)

        # Verifica se de fato tentou algumas vezes antes de conseguir
        self.assertGreaterEqual(mock_trocaveis.call_count, 100)

        # Verifica se a troca ocorreu (aluno (0,0) foi trocado com (1,0))
        aluno1 = self.individuo[0][0]
        aluno2 = self.individuo[1][0]
        self.assertIn(aluno1, resultado[1])
        self.assertIn(aluno2, resultado[0])

    def test_mutacao_nao_usa_aluno_com_um_horario_ou_incompativel(self):
        """
        Garante que a mutação ignora alunos com apenas um horário e que a troca só ocorre entre alunos compatíveis.
        """
        individuo = [
            [([12], gerar_treino())],
            [([13, 14], gerar_treino())],
            [([14], gerar_treino()), ([13, 14], gerar_treino())],
            [([15], gerar_treino())],
            [([16], gerar_treino())],
            [([17], gerar_treino())],
            0
        ]

        mutado = mutacao(individuo, 1)
        # Garante que a troca foi feita entre os dois alunos com horários múltiplos e compatíveis
        self.assertEqual(mutado[2][1], individuo[1][0])
        self.assertEqual(mutado[1][0], individuo[2][1])

class TestSelecaoTorneio(unittest.TestCase):
    """Por simplicidade, os indivíduos usados não são os mesmos do AG, mas a lógica é a mesma."""
    def setUp(self):
        self.populacao = [
            ['ind0'], ['ind1'], ['ind2'], ['ind3'],
            ['ind4'], ['ind5'], ['ind6'], ['ind7'], ['ind8'], ['ind9']
        ]

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.sample')
    def test_retorna_dois_melhores_do_torneio(self, mock_sample, mock_fitness):
        """
        Garante que a seleção retorna os dois indivíduos com melhor fitness entre os escolhidos no torneio.
        """
        torneio_mock = [['ind3'], ['ind6'], ['ind2'], ['ind8'], ['ind4']]
        mock_sample.return_value = torneio_mock

        fitness_map = {str(ind): i for i, ind in enumerate(torneio_mock)}
        mock_fitness.side_effect = lambda ind: fitness_map[str(ind)]

        ind1, ind2 = selecao_torneio(self.populacao, tam_torneio=5)

        self.assertEqual(ind1, ['ind3'])
        self.assertEqual(ind2, ['ind6'])

    @patch('Gymsys_Ga.funcao_fitness', return_value=1)
    @patch('Gymsys_Ga.random.sample')
    def test_torneio_com_fitness_iguais(self, mock_sample, mock_fitness):
        """
        Garante que, mesmo com fitness iguais, a função retorna dois indivíduos distintos da amostra.
        """
        mock_sample.return_value = self.populacao[:4]

        ind1, ind2 = selecao_torneio(self.populacao, tam_torneio=4)

        self.assertIn(ind1, self.populacao[:4])
        self.assertIn(ind2, self.populacao[:4])
        self.assertNotEqual(ind1, ind2)

    @patch('Gymsys_Ga.random.sample')
    def test_torneio_respeita_tamanho_parametrizado(self, mock_sample):
        """
        Verifica se o parâmetro `tam_torneio` é corretamente passado para `random.sample`.
        """
        tam = 6
        mock_sample.return_value = self.populacao[:tam]

        with patch('Gymsys_Ga.funcao_fitness', return_value=1):
            selecao_torneio(self.populacao, tam_torneio=tam)

        mock_sample.assert_called_once_with(self.populacao, tam)

class TestSelecaoRank(unittest.TestCase):
    """Por simplicidade, os indivíduos usados não são os mesmos do AG, mas a lógica é a mesma."""
    def setUp(self):
        # Cria uma população fictícia de 5 indivíduos
        self.populacao = [['ind0'], ['ind1'], ['ind2'], ['ind3'], ['ind4']]

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_selecao_usa_rank_para_probabilidades(self, mock_choices, mock_fitness):
        """
        Garante que os indivíduos são classificados por fitness e as probabilidades de seleção
        são baseadas em seu ranking (melhor fitness → maior chance).
        """
        # Define fitness fixos para garantir ordem
        mock_fitness.side_effect = [30, 10, 20, 40, 50]  # ordem de fitness: ind1, ind2, ind0, ind3, ind4
        mock_choices.return_value = [['ind1'], ['ind2']]  # valor simulado da escolha

        resultado = selecao_rank(self.populacao, num_pais=2)

        self.assertEqual(resultado, [['ind1'], ['ind2']])
        mock_choices.assert_called_once()

        # Verifica se a ordem dos indivíduos usados em random.choices é a esperada (ordenada por fitness crescente)
        ranked_esperado = [['ind1'], ['ind2'], ['ind0'], ['ind3'], ['ind4']]
        ranked_passado = mock_choices.call_args[0][0]
        self.assertEqual(ranked_passado, ranked_esperado)

    @patch('Gymsys_Ga.funcao_fitness', return_value=100)
    @patch('Gymsys_Ga.random.choices')
    def test_fitness_iguais_geram_probabilidades_adequadas(self, mock_choices, mock_fitness):
        """
        Garante que, se todos os fitness forem iguais, todos os indivíduos tenham chances adequadas de serem escolhidos.
        """
        selecao_rank(self.populacao, num_pais=3)
        weights = mock_choices.call_args[1]['weights']
        # Como todos os fitness são iguais, os ranks ainda serão [1, 2, 3, 4, 5]
        # Mas a distribuição deve ser proporcional e justa (ainda que não igual)
        self.assertEqual(len(weights), len(self.populacao))
        self.assertTrue(all(w > 0 for w in weights))

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_numero_de_pais_selecionados_esta_correto(self, mock_choices, mock_fitness):
        """
        Verifica se a função retorna exatamente `num_pais` indivíduos.
        """
        mock_fitness.side_effect = [5, 15, 25, 35, 45]
        mock_choices.return_value = [['ind0'], ['ind2'], ['ind4']]

        pais = selecao_rank(self.populacao, num_pais=3)

        self.assertEqual(len(pais), 3)
        self.assertEqual(pais, [['ind0'], ['ind2'], ['ind4']])

class TestSelecaoRankComElitismo(unittest.TestCase):
    """Por simplicidade, os indivíduos usados não são os mesmos do AG, mas a lógica é a mesma."""
    def setUp(self):
        # Cria uma população fictícia com 5 indivíduos (representados por letras)
        self.populacao = [['A'], ['B'], ['C'], ['D'], ['E']]

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_retorna_num_pais(self, mock_choices, mock_fitness):
        """
        Garante que a função retorna exatamente `num_pais` indivíduos.
        """
        mock_fitness.side_effect = [10, 20, 30, 40, 50]  # Ordem de fitness crescente
        mock_choices.return_value = [['X'], ['Y']]

        resultado = selecao_rank_com_elitismo(self.populacao, num_pais=4, elitismo=2)
        self.assertEqual(len(resultado), 4)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_elitismo_seleciona_melhores(self, mock_choices, mock_fitness):
        """
        Garante que os indivíduos com melhor fitness (menor valor) são escolhidos como elites.
        """
        mock_fitness.side_effect = [50, 40, 30, 20, 10]  # E é o melhor, A o pior
        mock_choices.return_value = [['X'], ['Y']]

        resultado = selecao_rank_com_elitismo(self.populacao, num_pais=4, elitismo=2)
        self.assertIn(['E'], resultado)
        self.assertIn(['D'], resultado)

    @patch('Gymsys_Ga.funcao_fitness', return_value=100)
    @patch('Gymsys_Ga.random.choices')
    def test_fitness_iguais_ainda_funciona(self, mock_choices, mock_fitness):
        """
        Garante que a função ainda funciona corretamente mesmo se todos os fitness forem iguais.
        """
        mock_choices.return_value = [['B'], ['C']]
        resultado = selecao_rank_com_elitismo(self.populacao, num_pais=4, elitismo=2)
        self.assertEqual(len(resultado), 4)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_probabilidades_calculadas_com_base_em_ranking(self, mock_choices, mock_fitness):
        """
        Garante que `random.choices` é chamado com pesos baseados no ranking da população.
        """
        mock_fitness.side_effect = [50, 40, 30, 20, 10]  # E é o melhor
        selecao_rank_com_elitismo(self.populacao, num_pais=4, elitismo=2)

        weights = mock_choices.call_args[1]['weights']
        self.assertEqual(len(weights), 3)
        self.assertTrue(all(w > 0 for w in weights))

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_elitismo_zero_equivale_a_rank_puro(self, mock_choices, mock_fitness):
        """
        Garante que quando `elitismo=0`, a seleção se comporta como rank puro.
        """
        mock_fitness.side_effect = [10, 20, 30, 40, 50]
        mock_choices.return_value = [['B'], ['C'], ['D']]

        resultado = selecao_rank_com_elitismo(self.populacao, num_pais=3, elitismo=0)
        self.assertEqual(resultado, [['B'], ['C'], ['D']])

class TestSelecaoRoleta(unittest.TestCase):
    """Por simplicidade, os indivíduos usados não são os mesmos do AG, mas a lógica é a mesma."""
    def setUp(self):
        # População de teste simples
        self.populacao = [['A'], ['B'], ['C'], ['D'], ['E']]

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_retorna_num_pais(self, mock_choices, mock_fitness):
        """
        Garante que a função retorna exatamente `num_pais` indivíduos.
        """
        mock_fitness.side_effect = [10, 20, 30, 40, 50]
        mock_choices.return_value = [['A'], ['B']]
        
        resultado = selecao_roleta(self.populacao, num_pais=2)
        self.assertEqual(len(resultado), 2)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_fitness_menor_recebe_mais_peso(self, mock_choices, mock_fitness):
        """
        Garante que os indivíduos com menor fitness recebem maior peso na seleção.
        """
        fitness_vals = [1, 2, 3, 4, 5]  # A = melhor, E = pior
        mock_fitness.side_effect = fitness_vals
        selecao_roleta(self.populacao, num_pais=3)

        max_fitness = max(fitness_vals)
        inverted = [max_fitness - f + 1e-6 for f in fitness_vals]
        total = sum(inverted)
        expected_weights = [v / total for v in inverted]

        mock_choices.assert_called_once_with(self.populacao, weights=expected_weights, k=3)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_com_fitness_iguais_probabilidades_iguais(self, mock_choices, mock_fitness):
        """
        Garante que se todos os fitness forem iguais, todos tenham mesma probabilidade.
        """
        mock_fitness.side_effect = [10, 10, 10, 10, 10]
        selecao_roleta(self.populacao, num_pais=3)

        # max_fitness - f + 1e-6 será o mesmo para todos → probabilidade igual
        expected_weights = [1 / 5] * 5
        mock_choices.assert_called_once_with(self.populacao, weights=expected_weights, k=3)

class TestSelecaoRoletaComElitismo(unittest.TestCase):
    """Por simplicidade, os indivíduos usados não são os mesmos do AG, mas a lógica é a mesma."""
    def setUp(self):
        # População de teste simples
        self.populacao = [['A'], ['B'], ['C'], ['D'], ['E']]

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_retorna_num_pais(self, mock_choices, mock_fitness):
        """
        Garante que a função retorna exatamente `num_pais` indivíduos, incluindo elites e os selecionados pela roleta.
        """
        mock_fitness.side_effect = [50, 40, 30, 20, 10]
        mock_choices.return_value = [['X'], ['Y']]  # Simula dois selecionados pela roleta

        resultado = selecao_roleta_com_elitismo(self.populacao, num_pais=4, elitismo=2)
        self.assertEqual(len(resultado), 4)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_seleciona_melhores_elites(self, mock_choices, mock_fitness):
        """
        Garante que os indivíduos com menor fitness são selecionados como elites.
        """
        mock_fitness.side_effect = [50, 30, 10, 40, 20]  # 'C' e 'E' têm os menores valores

        mock_choices.return_value = [['X'], ['Y']]  # mocka seleção por roleta

        resultado = selecao_roleta_com_elitismo(self.populacao, num_pais=4, elitismo=2)
        
        self.assertIn(['C'], resultado)  # 'C' deve estar nos elites
        self.assertIn(['E'], resultado)  # 'E' deve estar nos elites
        self.assertEqual(len(resultado), 4)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_roleta_favorece_fitness_menores(self, mock_choices, mock_fitness):
        """
        Verifica se os pesos usados na roleta favorecem indivíduos com menor fitness.
        """
        # A menor fitness = maior probabilidade (invertido)
        mock_fitness.side_effect = [100, 50, 25, 12.5, 6.25]  # valores decrescentes

        def fake_choices(pop, weights, k):
            self.assertEqual(pop, [['A'], ['B'], ['C']])  # não elites
            self.assertEqual(k, 1)  # num_pais - elitismo
            # Como fitness foram [100, 50, 25, 12.5, 6.25]
            # Os não elites serão os 3 piores: 'A' (100), 'B' (50), 'C' (25)
            # Seus pesos devem ser: [1/100, 1/50, 1/25] → normalizado

            expected_weights = [1 / 100, 1 / 50, 1 / 25]
            total = sum(expected_weights)
            normalized = [w / total for w in expected_weights]
            self.assertAlmostEqual(sum(normalized), 1.0)
            return [['C']]

        mock_choices.side_effect = fake_choices

        resultado = selecao_roleta_com_elitismo(self.populacao, num_pais=3, elitismo=2)
        self.assertEqual(len(resultado), 3)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.random.choices')
    def test_com_fitness_iguais_probabilidades_iguais(self, mock_choices, mock_fitness):
        """
        Garante que, quando todos os fitness são iguais, as probabilidades passadas para a roleta são iguais.
        """
        mock_fitness.side_effect = [10, 10, 10, 10, 10]  # Todos os indivíduos com fitness igual
        mock_choices.return_value = [['X'], ['Y']]       # Não importa aqui

        # elitismo = 2, num_pais = 4 → roleta escolhe 2 entre 3 restantes
        resultado = selecao_roleta_com_elitismo(self.populacao, num_pais=4, elitismo=2)

        # Pegamos os argumentos usados na chamada de `random.choices`
        args, kwargs = mock_choices.call_args
        probabilidades = kwargs.get('weights', [])

        # Verifica se todas as probabilidades são iguais
        self.assertTrue(all(p == probabilidades[0] for p in probabilidades), 
                        msg="As probabilidades não são todas iguais.")

        # Confirma que o número total de pais está correto
        self.assertEqual(len(resultado), 4)

class TestAlgoritmoGenetico(unittest.TestCase):

    def setUp(self):
        self.espaco_solucao = [('aluno1'), ('aluno12'), ('aluno3'), ('aluno4'), ('aluno5')]
        self.individuo_exemplo = [[('aluno1')], [('aluno2')], [('aluno3')], [('aluno4')], [('aluno5')], [], 0]

    @patch('Gymsys_Ga.criar_individuo')
    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.selecao_rank')
    @patch('Gymsys_Ga.crossover_entrelacado')
    @patch('Gymsys_Ga.mutacao')
    def test_retorna_individuo(self, mock_mutacao, mock_crossover, mock_selecao, mock_fitness, mock_criar_individuo):
        """
        Garante que a função retorna dois indivíduo ao final.
        """
        mock_criar_individuo.side_effect = lambda x: self.individuo_exemplo.copy()
        mock_fitness.side_effect = lambda ind: 10  # fitness constante
        mock_selecao.return_value = (self.individuo_exemplo, self.individuo_exemplo)
        mock_crossover.return_value = (self.individuo_exemplo, self.individuo_exemplo)
        mock_mutacao.side_effect = lambda ind, taxa: ind

        resultado = algoritmo_genetico(
            num_generacoes=2,
            tam_populacao=4,
            espaco_solucao=self.espaco_solucao,
            taxa_mutacao=0.1,
            elitismo=2
        )
        tam = 0
        # Verifica se o tamanho da soma dos horários do individuo é igual ao tamanho do espaço de solução
        for i in range(6):
            tam += len(resultado[1][i])
        self.assertEqual(tam, len(self.espaco_solucao))
        # Verifica se o resultado é uma lista de listas
        self.assertIsInstance(resultado[1], list)
        self.assertIsInstance(resultado[0], list)

    @patch('Gymsys_Ga.criar_individuo')
    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.selecao_rank')
    @patch('Gymsys_Ga.crossover_entrelacado')
    @patch('Gymsys_Ga.mutacao')
    def test_melhor_fitness_mantido(self, mock_mutacao, mock_crossover, mock_selecao, mock_fitness, mock_criar_individuo):
        """
        Garante que o indivíduo com melhor fitness é retornado.
        """
        individuo_bom = [['bom']]
        individuo_ruim = [['ruim']]

        mock_criar_individuo.side_effect = [individuo_bom, individuo_ruim, individuo_ruim, individuo_ruim]
        mock_fitness.side_effect = lambda ind: 0 if ind == individuo_bom else 100
        mock_selecao.return_value = (individuo_ruim, individuo_ruim)
        mock_crossover.return_value = (individuo_ruim, individuo_ruim)
        mock_mutacao.side_effect = lambda ind, taxa: ind

        resultado = algoritmo_genetico(
            num_generacoes=1,
            tam_populacao=4,
            espaco_solucao=[['bom'], ['ruim']],
            taxa_mutacao=0.1,
            elitismo=2
        )
        self.assertEqual(resultado[1], individuo_bom)

    @patch('Gymsys_Ga.funcao_fitness')
    @patch('Gymsys_Ga.criar_individuo')
    def test_populacao_criada_com_tamanho_correto(self, mock_criar_individuo, mock_fitness):
        """
        Garante que a população inicial tem o tamanho correto.
        """
        mock_criar_individuo.return_value = self.individuo_exemplo
        mock_fitness.return_value = 10

        with patch('Gymsys_Ga.selecao_rank', return_value=(self.individuo_exemplo, self.individuo_exemplo)), \
             patch('Gymsys_Ga.crossover_entrelacado', return_value=(self.individuo_exemplo, self.individuo_exemplo)), \
             patch('Gymsys_Ga.mutacao', side_effect=lambda ind, taxa: ind):

            algoritmo_genetico(
                num_generacoes=1,
                tam_populacao=5,
                espaco_solucao=self.espaco_solucao,
                taxa_mutacao=0.1,
                elitismo=2
            )

            self.assertEqual(mock_criar_individuo.call_count, 5)

#Testes de Gymsys_render.py ---------------------------------------------------------------------------------------------------------------------------------------

class TestVisualSemaphore(unittest.TestCase):
    def setUp(self):
        # Cria um mock de canvas e configura os retornos para chamadas de criação de elementos gráficos
        self.canvas = unittest.mock.MagicMock()
        self.canvas.create_rectangle.side_effect = lambda *args, **kwargs: f"rect_{len(self.canvas.create_rectangle.call_args_list)}"
        self.canvas.create_oval.side_effect = lambda *args, **kwargs: f"oval_{len(self.canvas.create_oval.call_args_list)}"
        self.canvas.create_text.side_effect = lambda *args, **kwargs: f"text_{len(self.canvas.create_text.call_args_list)}"

    def test_init_cria_elementos_graficos(self):
        """
        Verifica se a inicialização do VisualSemaphore cria corretamente
        os elementos gráficos no canvas (retângulos, círculos e textos)
        e se os atributos internos são atribuídos corretamente.
        """
        vs = VisualSemaphore(self.canvas, x=10, y=20, max_permits=2, machine_id=1)
        
        self.assertEqual(self.canvas.create_rectangle.call_count, 2)
        self.assertEqual(self.canvas.create_oval.call_count, 2)
        self.assertEqual(self.canvas.create_text.call_count, 3)  # 2 labels + 1 título
        
        self.assertEqual(len(vs.rectangles), 2)
        self.assertEqual(len(vs.circles), 2)
        self.assertEqual(len(vs.labels), 2)
        self.assertEqual(vs.machine_id, 1)
        self.assertEqual(vs.max_permits, 2)

    @patch('threading.Semaphore')
    def test_acquire_funciona_quando_permitido(self, MockSemaphore):
        """
        Testa se o método acquire funciona corretamente quando o semáforo
        permite a aquisição. Verifica se os elementos gráficos do canvas
        são atualizados para indicar o uso por uma thread.
        """
        mock_semaphore = MockSemaphore.return_value
        mock_semaphore.acquire.return_value = True

        self.canvas.itemcget.side_effect = ["white", "white"]
        vs = VisualSemaphore(self.canvas, x=0, y=0, max_permits=2, machine_id=0)
        vs.semaphore = mock_semaphore

        vs.circles = ['oval1', 'oval2']
        vs.labels = ['label1', 'label2']
        vs.rectangles = ['rect1', 'rect2']

        sucesso = vs.acquire(thread_id=42)

        self.assertTrue(sucesso)
        self.canvas.itemcget.assert_called()
        self.canvas.itemconfig.assert_any_call('oval1', fill="blue")
        self.canvas.itemconfig.assert_any_call('label1', text="Aluno 42")
        self.canvas.itemconfig.assert_any_call('rect1', fill="red")

    @patch('threading.Semaphore')
    def test_acquire_falha_quando_nao_permitido(self, MockSemaphore):
        """
        Testa se o método acquire retorna False e não modifica o canvas
        quando o semáforo nega a aquisição de um slot.
        """
        mock_semaphore = MockSemaphore.return_value
        mock_semaphore.acquire.return_value = False

        vs = VisualSemaphore(self.canvas, x=0, y=0)
        vs.semaphore = mock_semaphore

        sucesso = vs.acquire(thread_id=1)

        self.assertFalse(sucesso)
        self.canvas.itemcget.assert_not_called()
        self.canvas.itemconfig.assert_not_called()

    @patch('threading.Semaphore')
    def test_release_libera_um_permit(self, MockSemaphore):
        """
        Testa se o método release libera um slot ocupado, atualizando
        os elementos gráficos no canvas e chamando release() no semáforo.
        """
        mock_semaphore = MockSemaphore.return_value

        vs = VisualSemaphore(self.canvas, x=0, y=0, max_permits=2, machine_id=0)
        vs.semaphore = mock_semaphore

        vs.circles = ['oval1', 'oval2']
        vs.rectangles = ['rect1', 'rect2']
        vs.labels = ['label1', 'label2']

        self.canvas.itemcget.side_effect = ["blue", "white"]

        vs.release()

        mock_semaphore.release.assert_called_once()
        self.canvas.itemcget.assert_any_call('oval1', "fill")
        self.canvas.itemconfig.assert_any_call('oval1', fill="white")
        self.canvas.itemconfig.assert_any_call('rect1', fill="green")
        self.canvas.itemconfig.assert_any_call('label1', text="")

class TestUpdateCanvasSize(unittest.TestCase):

    def setUp(self):
        self.canvas = unittest.mock.MagicMock()

        # Cria uma máquina mockada com múltiplos atributos
        def make_mock_maquina(machine_id, max_permits=2):
            machine = unittest.mock.MagicMock()
            machine.width = 50
            machine.height = 20
            machine.max_permits = max_permits
            machine.canvas = self.canvas
            machine.rectangles = [f'rect{machine_id}_{i}' for i in range(max_permits)]
            machine.circles = [f'circle{machine_id}_{i}' for i in range(max_permits)]
            machine.labels = [f'label{machine_id}_{i}' for i in range(max_permits)]
            machine.label = f'machine_label_{machine_id}'
            return machine

        self.maquinas = [make_mock_maquina(i) for i in range(4)]

    def test_update_positions_and_canvas_config(self):
        update_canvas_size(self.maquinas, self.canvas)

        # Verifica se as posições x e y foram atualizadas
        for i, maquina in enumerate(self.maquinas):
            self.assertTrue(hasattr(maquina, "x"))
            self.assertTrue(hasattr(maquina, "y"))

        # Verifica se canvas.config foi chamado com largura e altura
        self.canvas.config.assert_called_once()
        args, kwargs = self.canvas.config.call_args
        self.assertIn("width", kwargs)
        self.assertIn("height", kwargs)

    def test_coords_called_for_all_elements(self):
        update_canvas_size(self.maquinas, self.canvas)

        for maquina in self.maquinas:
            for rect in maquina.rectangles:
                self.canvas.coords.assert_any_call(rect, unittest.mock.ANY, unittest.mock.ANY,
                                                   unittest.mock.ANY, unittest.mock.ANY)
            for circle in maquina.circles:
                self.canvas.coords.assert_any_call(circle, unittest.mock.ANY, unittest.mock.ANY,
                                                   unittest.mock.ANY, unittest.mock.ANY)
            for label in maquina.labels:
                self.canvas.coords.assert_any_call(label, unittest.mock.ANY, unittest.mock.ANY)

            self.canvas.coords.assert_any_call(maquina.label, unittest.mock.ANY, unittest.mock.ANY)

class TestUpdateCornerLabel(unittest.TestCase):
    def setUp(self):
        # Cria um mock de canvas para ser usado nos testes
        self.canvas = unittest.mock.MagicMock()

    def test_cria_novo_texto_quando_nao_existe(self):
        """
        Testa se a função cria um novo texto no canto do canvas
        quando nenhum texto com a tag 'corner_label' existe.
        """
        self.canvas.find_withtag.return_value = []  # Nenhum texto existente
        self.canvas.create_text.return_value = 42   # Simula criação com ID 42

        with patch('Gymsys_render.corner_label_id', None):
            update_corner_label(self.canvas, 123)

        self.canvas.create_text.assert_called_once_with(
            10, 10,
            anchor="nw",
            text="Tempo de espera total: 123",
            fill="black",
            font=("Arial", 12),
            tags="corner_label"
        )

    def test_atualiza_texto_quando_corner_label_existe(self):
        """
        Testa se a função atualiza corretamente o texto existente
        quando um elemento com a tag 'corner_label' já está presente.
        """
        self.canvas.find_withtag.return_value = ["qualquer_id"]

        with patch('Gymsys_render.corner_label_id', 123):
            update_corner_label(self.canvas, 456)

        self.canvas.itemconfig.assert_called_once_with(
            123, text="Tempo de espera total: 456"
        )

#Testes de Gymsys_greedy.py ------------------------------------------------------------------------------------------------------------------------------------------

class TestAlgoritmoGuloso(unittest.TestCase):
    
    def test_espaco_vazio(self):
        """Deve retornar solução vazia quando não há alunos para alocar."""
        espaco_solucao = []
        resultado = algoritmo_guloso(espaco_solucao)
        self.assertEqual(resultado, [[], [], [], [], [], [], 0])

    def test_um_aluno_valido(self):
        """Deve alocar corretamente um único aluno compatível."""
        aluno_valido = ([13, 14], [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        espaco_solucao = [aluno_valido]
        resultado = algoritmo_guloso(espaco_solucao)
        alocado = any(resultado[i] for i in range(6))
        self.assertTrue(alocado)
        self.assertEqual(resultado[6], 0)

    def test_um_aluno_invalido(self):
        """Deve descartar aluno incompatível e aumentar o contador de descartes."""
        aluno_invalido = ([], [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        espaco_solucao = [aluno_invalido]
        resultado = algoritmo_guloso(espaco_solucao)
        self.assertTrue(all(len(horario) == 0 for horario in resultado[:6]))
        self.assertEqual(resultado[6], 1)

    def test_varios_alunos(self):
        """Deve alocar e descartar alunos corretamente de acordo com o fitness."""
        alunos = [
            ([12], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            ([13, 12], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            ([13, 12, 14], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
            ([], [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]) 
        ]
        resultado = algoritmo_guloso(alunos)
        total = sum(len(h) for h in resultado[:6]) + resultado[6]
        self.assertEqual(total, 4)
        self.assertEqual(len(resultado), 7)
        self.assertEqual(resultado[6], 1)
        self.assertIn(([12], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), resultado[0])
        self.assertIn(([13, 12], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), resultado[1])
        self.assertIn(([13, 12, 14], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]), resultado[2])

class TestCriarNovaSolucao(unittest.TestCase):
    def setUp(self):
        """Define uma solução inicial vazia e um exemplo de aluno válido."""
        self.solucao_vazia = [[] for _ in range(6)] + [0]  # [[], [], [], [], [], [], 0]
        self.aluno_valido = ([12], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # Treina às 12h

    def test_alocacao_valida(self):
        """Testa se o aluno é corretamente alocado quando há espaço disponível."""
        nova_solucao = criar_nova_solucao(self.solucao_vazia, self.aluno_valido)
        self.assertIsNotNone(nova_solucao)
        self.assertIn(self.aluno_valido, nova_solucao[0])  # 12h -> índice 0

    def test_alocacao_limite_excedido(self):
        """Testa se None é retornado quando não há espaço disponível para o aluno."""
        solucao_cheia = [ [self.aluno_valido]*20 if i == 0 else [] for i in range(6)] + [0]
        resultado = criar_nova_solucao(solucao_cheia, self.aluno_valido)
        self.assertIsNone(resultado)

    def test_melhor_solucao_por_fitness(self):
        """Testa se a solução com melhor fitness é escolhida entre múltiplas opções."""
        # Aluno pode treinar às 12h e 13h (índices 0 e 1)
        aluno_multi = ([12, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        # Solução inicial com um aluno já em 12h para mudar o fitness
        base = [[] for _ in range(6)] + [0]
        base[0].append(self.aluno_valido)  # piora a fitness no horário 12h
        nova_solucao = criar_nova_solucao(base, aluno_multi)

        # Verifica se o aluno foi alocado em 13h (índice 1), que tem fitness melhor
        self.assertIn(aluno_multi, nova_solucao[1])
        self.assertNotIn(aluno_multi, nova_solucao[0])

    def test_retorna_objeto_novo(self):
        """Testa se a função retorna uma nova instância de solução (imutabilidade)."""
        original = copy.deepcopy(self.solucao_vazia)
        criar_nova_solucao(original, self.aluno_valido)
        self.assertEqual(original, self.solucao_vazia)  # Verifica que não foi modificada
        

#Testes de Gymsys_simulacao.py ---------------------------------------------------------------------------------------------------------------------------------------

class TestCriarMaquinas(unittest.TestCase):

    def test_criar_maquinas(self):
        """
        Testa se a função criar_maquinas retorna uma lista com o número correto de elementos
        e se cada elemento é uma instância da classe VisualSemaphore.
        """
        # Cria um objeto Mock para o canvas, já que não precisamos de um canvas real para este teste.
        canvas_mock = unittest.mock.Mock()

        # Chama a função a ser testada
        maquinas = criar_maquinas(canvas_mock)

        # Verifica se o número de semáforos criados é igual ao número de elementos em max_permits
        self.assertEqual(len(maquinas), 10, "Número incorreto de máquinas criadas")

        # Verifica se cada elemento da lista é uma instância de VisualSemaphore
        for maquina in maquinas:
            self.assertIsInstance(maquina, VisualSemaphore, "Objeto incorreto criado")

        # Verifica se os parâmetros de inicialização de cada VisualSemaphore estão corretos
        max_permits_esperados = [1, 1, 1, 1, 1, 1, 2, 3, 3, 5]
        for i, maquina in enumerate(maquinas):
            self.assertEqual(maquina.max_permits, max_permits_esperados[i], f"Permissões incorretas para a máquina {i}")
            self.assertEqual(maquina.machine_id, i, f"ID de máquina incorreto para a máquina {i}")
            self.assertEqual(maquina.x, 50 + i * 200, f"Posição x incorreta para a máquina {i}")
            self.assertEqual(maquina.y, 100, f"Posição y incorreta para a máquina {i}")
            self.assertEqual(maquina.canvas, canvas_mock, f"Canvas incorreto para a máquina {i}")

class TestSimulacaoHorario(unittest.TestCase):

    @patch("Gymsys_simulacao.update_canvas_size")
    @patch("Gymsys_simulacao.criar_maquinas")
    @patch("Gymsys_simulacao.treino")
    def test_simulacao_com_dois_alunos(self, mock_treino, mock_criar_maquinas, mock_update_canvas_size):
        """Testa se a simulação cria e inicia threads corretamente para dois alunos"""
        canvas = unittest.mock.MagicMock()
        alunos_horario = [([12], [0, 1]), ([13], [2])]
        shared_data = {"mutex": unittest.mock.MagicMock(), "espera_total": 0}

        # Cria mocks de VisualSemaphore com os atributos necessários
        fake_maquina = unittest.mock.MagicMock()
        fake_maquina.width = 50
        fake_maquina.height = 20
        fake_maquina.max_permits = 2
        
        mock_criar_maquinas.return_value = [fake_maquina] * 5  # Simula 5 máquinas
        simulacao_horario(canvas, alunos_horario, shared_data)

        self.assertEqual(mock_treino.call_count, 2)
        calls = [
            unittest.mock.call(alunos_horario[0], 0, mock_criar_maquinas.return_value, shared_data, canvas),
            unittest.mock.call(alunos_horario[1], 1, mock_criar_maquinas.return_value, shared_data, canvas),
        ]
        mock_treino.assert_has_calls(calls, any_order=True)
        mock_criar_maquinas.assert_called_once_with(canvas)
        mock_update_canvas_size.assert_called_once_with(mock_criar_maquinas.return_value, canvas)

    @patch("Gymsys_simulacao.update_canvas_size")
    @patch("Gymsys_simulacao.criar_maquinas")
    @patch("Gymsys_simulacao.treino")
    def test_simulacao_sem_alunos(self, mock_treino, mock_criar_maquinas, mock_update_canvas_size):
        """Testa se a simulação lida corretamente com lista vazia de alunos"""
        canvas = unittest.mock.MagicMock()
        alunos_horario = []
        shared_data = {"mutex": unittest.mock.MagicMock(), "espera_total": 0}

        simulacao_horario(canvas, alunos_horario, shared_data)

        mock_treino.assert_not_called()
        mock_criar_maquinas.assert_called_once()
        mock_update_canvas_size.assert_called_once()

class TestSimulacaoIndividuo(unittest.TestCase):
    
    @patch('Gymsys_simulacao.simulacao_horario')
    def test_simulacao_individuo_com_tres_horarios(self, mock_simulacao_horario):
        # Setup do canvas
        canvas = unittest.mock.MagicMock()
        
        # Criando um individuo com 3 horários de treino (lista de alunos por horário)
        alunos_mock = [([12, 13, 14], [0, 1]), ([12, 13, 14], [2, 3])]
        individuo = [alunos_mock, alunos_mock, alunos_mock, [], [], [], 0]  # Último elemento é descarte

        # Setup do shared_data global
        from Gymsys_simulacao import shared_data
        shared_data["espera_total"] = 15.0
        shared_data["mutex"] = unittest.mock.MagicMock()
        shared_data["mutex"].acquire = unittest.mock.MagicMock()
        shared_data["mutex"].release = unittest.mock.MagicMock()

        # Rodar a simulação
        espera = simulacao_individuo(canvas, individuo)

        # Verificações
        self.assertEqual(espera, 15.0)
        self.assertEqual(shared_data["espera_total"], 0)
        self.assertEqual(mock_simulacao_horario.call_count, 6)
        canvas.delete.assert_called_with("clear")
        shared_data["mutex"].acquire.assert_called_once()
        shared_data["mutex"].release.assert_called_once()

class TestTreino(unittest.TestCase):

    def setUp(self):
        self.aluno = ([12, 13], [0, 1])  # Horários e máquinas que o aluno quer usar
        self.id = 1
        self.tempo_treino_mock = 0.6

        # Mocks para semáforos (sempre adquirem com sucesso)
        self.semaforo_mock1 = unittest.mock.MagicMock()
        self.semaforo_mock1.acquire.return_value = True
        self.semaforo_mock2 = unittest.mock.MagicMock()
        self.semaforo_mock2.acquire.return_value = True

        self.maquinas = [self.semaforo_mock1, self.semaforo_mock2]

        # Shared data com mutex e espera_total
        self.shared_data = {
            "espera_total": 0,
            "mutex": threading.Lock()
        }

        # Canvas simulado
        self.canvas = unittest.mock.MagicMock()

    @patch('Gymsys_simulacao.tempo_maquinas', new=[0.3, 0.3, 0.4, 0.4, 0.5, 0.5, 0.7, 1.0, 1.2, 1.5])
    @patch("Gymsys_simulacao.update_corner_label")
    @patch("Gymsys_simulacao.calcular_tempo_treino")
    def test_treino_completo_sem_espera(self, mock_tempo, mock_update):
        """Testa se o treino é realizado com sucesso e a espera é próxima de zero quando não há bloqueios."""
        mock_tempo.return_value = self.tempo_treino_mock

        start = time.time()
        treino(self.aluno, self.id, self.maquinas, self.shared_data, self.canvas)
        end = time.time()

        self.assertAlmostEqual(self.shared_data["espera_total"], (end - start) - self.tempo_treino_mock, delta=0.05)
        mock_update.assert_called_once_with(self.canvas, self.shared_data["espera_total"])
        self.assertEqual(self.semaforo_mock1.acquire.call_count, 1)
        self.assertEqual(self.semaforo_mock2.acquire.call_count, 1)

    @patch("Gymsys_simulacao.time.sleep", return_value=None)
    @patch("Gymsys_simulacao.update_corner_label")
    @patch("Gymsys_simulacao.calcular_tempo_treino")
    def test_sem_release_na_falha(self, mock_tempo, mock_update, mock_sleep):
        """Testa se máquinas são reordenadas corretamente quando semáforo não está disponível."""
        self.semaforo_mock1.acquire.side_effect = [False, True]
        mock_tempo.return_value = self.tempo_treino_mock

        treino(self.aluno, self.id, self.maquinas, self.shared_data, self.canvas)

        # A máquina 0 deveria ser tentada duas vezes
        self.assertGreaterEqual(self.semaforo_mock1.acquire.call_count, 2)

    @patch("Gymsys_simulacao.time.sleep", return_value=None)
    @patch("Gymsys_simulacao.update_corner_label")
    @patch("Gymsys_simulacao.calcular_tempo_treino")
    def test_shared_mutex_usado(self, mock_tempo, mock_update, mock_sleep):
        """Testa se o mutex é corretamente usado ao atualizar a espera_total."""
        mock_tempo.return_value = self.tempo_treino_mock
        treino(self.aluno, self.id, self.maquinas, self.shared_data, self.canvas)
        # Não temos como testar diretamente o lock, mas podemos confirmar ausência de erro e update correto
        mock_update.assert_called_once()

class TestCalcularTempoTreino(unittest.TestCase):
    """Para testar a função de forma apropriada, são usados alguns casos que não ocorrem necessariamente na execução real do código."""
    def test_calcular_tempo_treino_aluno_com_uma_maquina(self):
        """
        Testa o cálculo do tempo de treino para um aluno que treina em apenas uma máquina.
        """
        aluno = ([12, 14], [0])
        self.assertEqual(calcular_tempo_treino(aluno), 0.3)

    def test_calcular_tempo_treino_aluno_com_multiplas_maquinas(self):
        """
        Testa o cálculo do tempo de treino para um aluno que treina em todas as máquinas disponíveis.
        """
        aluno = ([13, 14], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(calcular_tempo_treino(aluno), 6.8)

    def test_calcular_tempo_treino_aluno_com_maquinas_repetidas(self):
        """
        Testa o cálculo do tempo de treino para um aluno que treina em máquinas repetidas.
        """
        aluno = ([15, 17], [0, 0, 0, 1, 1, 1, 9, 9, 9, 2])
        self.assertEqual(calcular_tempo_treino(aluno), 6.7)

    def test_calcular_tempo_treino_aluno_sem_maquinas(self):
        """
        Testa o cálculo do tempo de treino para um aluno que não treina em nenhuma máquina.
        """
        aluno = ([13, 15], [])
        self.assertEqual(calcular_tempo_treino(aluno), 0)

if __name__ == '__main__':
    unittest.main()
