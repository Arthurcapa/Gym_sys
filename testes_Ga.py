from Gymsys_manager import *
import matplotlib.pyplot as plt
from Gymsys_Ga import *
import unittest
import numpy as np

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

if __name__ == '__main__':
    unittest.main()
