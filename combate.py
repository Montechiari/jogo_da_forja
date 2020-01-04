from copy import copy
import numpy as np

SAUDE_PRONTIDAO_MAX = 20
SAUDE_PRONTIDAO_MIN = 8
DANO_ARMA_MAX = 10
DANO_ARMA_MIN = 3

# Caractere da esquerda eh acao de combatente com iniciativa; direita, do outro
COMBINACOES_DE_ACOES = [["19", "19", "13", "16", "14", "16"],
                        ["29", "29", "23", "26", "24", "26"],
                        ["31", "32", "44", "36", "48", "54"],
                        ["61", "62", "63", "66", "74", "48"],
                        ["41", "42", "84", "47", "44", "44"],
                        ["41", "42", "45", "84", "44", "44"]]

# [tipo de vantagem, quanto inflige dano, tipo de dano, prontidao]
ACOES_CODIFICADAS = {"1": ['ofensiva', 0, '', 0],
                     "2": ['defensiva', 0, '', 0],
                     "3": ['', 1, 'c', -1],
                     "4": ['', 0, '', -1],
                     "5": ['', 0.5, 'c', -1],
                     "6": ['', 1, 'e', -1],
                     "7": ['', 0.5, 'e', -1],
                     "8": ['', 0, '', 1],
                     "9": ['', 0, '', 0]}

INDICE_DE_ACAO_EXTRA = ['1', '2', '3', '6', '4', '4']


class Combatente():
    def __init__(self, nome):

        self.nome = nome
        self.saude, self.prontidao, self.arma = self.sorteia_atributos()
        self.oponente = None
        self.acao = None
        self.tem_vantagem = False

    def sorteia_atributos(self):
        def sorteio(maximo, minimo):
            pontos_livres = maximo - (2 * minimo)
            primeiro_atributo = minimo + np.random.randint(0,
                                                           pontos_livres + 1
                                                           )
            segundo_atributo = maximo - primeiro_atributo
            return (primeiro_atributo, segundo_atributo)

        saude, prontidao = sorteio(SAUDE_PRONTIDAO_MAX, SAUDE_PRONTIDAO_MIN)
        arma = {}
        arma['estocada'], arma['corte'] = sorteio(DANO_ARMA_MAX, DANO_ARMA_MIN)
        return saude, prontidao, arma

    def altera_saude(self, montante):
        self.saude += montante

    def altera_prontidao(self, montante):
        self.prontidao += montante

    def inflige_dano(self, tipo):
        dano = self.arma[tipo]
        self.oponente.altera_saude(dano * -1)

    def registro_da_partida(self):
        pass

    def registra_turno(self):
        pass


class JogadorHumano(Combatente):
    def __init__(self):
        Combatente.__init__(self, 'Carlos')

    def decide_acao(self):
        pass


class JogadorRedeNeural(Combatente):
    def __init__(self):
        Combatente.__init__(self, 'Caio')

    def decide_acao(self):
        pass


class JogadorAleatorio(Combatente):
    def __init__(self):
        Combatente.__init__(self, 'Hicham')

    def decide_acao(self):
        self.acao = np.random.randint(1, 7)


class Partida():
    def __init__(self):

        self.vantagem = {'quem': None, 'tipo': None}
        self.combatentes = self.cria_combatentes()
        self.status = None
        self.turno_numero = 1
        while self.todos_vivos():
            self.novo_turno()
        print('fim da partida!')

    def cria_combatentes(self):
        combatentes = [JogadorAleatorio(), JogadorAleatorio()]
        ordem_invertida = copy(combatentes)
        ordem_invertida.reverse()
        for i in range(2):
            combatentes[i].oponente = ordem_invertida[i]
        return combatentes

    def novo_turno(self):
        print("turno", self.turno_numero)
        print(self.combatentes[0].saude, self.combatentes[1].saude)
        acao_extra = self.determina_iniciativa()
        for individuo in self.combatentes:
            individuo.decide_acao()

        self.traduz_acoes()

        for combatente in self.combatentes:
            self.aplica_efeitos_de_acao(combatente)

        while acao_extra > 0 or self.turno_numero > 20:
            self.combatentes[0].decide_acao()
            self.aplica_efeitos_de_acao(self.combatentes[0])
            acao_extra -= 1

        self.turno_numero += 1
        return 'fim de turno'

    def traduz_acoes(self):
        indice_de_acao = COMBINACOES_DE_ACOES[self.combatentes[0].acao - 1
                                              ][self.combatentes[1].acao - 1]
        for i, combatente in enumerate(self.combatentes):
            combatente.acao = ACOES_CODIFICADAS[indice_de_acao[i]]

    def traduz_acao_extra(self):
        indice = INDICE_DE_ACAO_EXTRA[self.combatentes[0].acao - 1]
        acao_traduzida = ACOES_CODIFICADAS[indice]
        self.combatentes[0].acao = acao_traduzida

    def aplica_efeitos_de_acao(self, combatente):
        if combatente.acao[0] != '':
            self.resolve_vantagem(combatente)
        self.resolve_dano(combatente)
        self.resolve_prontidao(combatente)

    def resolve_vantagem(self, combatente):
        self.vantagem['quem'] = combatente
        self.vantagem['tipo'] = combatente.acao[0]
        combatente.oponente.tem_vantagem = False
        combatente.tem_vantagem = True

    def resolve_dano(self, combatente):
        dano = 0
        if combatente.acao[2] is 'c':
            dano = combatente.arma['corte']
        elif combatente.acao[2] is 'e':
            dano = combatente.arma['estocada']
        if (combatente.tem_vantagem and self.vantagem['tipo'] is 'ofensiva'):
            dano *= 2
        elif (combatente.oponente.tem_vantagem and self.vantagem['tipo'] is 'defensiva'):
            dano *= 0.5
        combatente.oponente.altera_saude(-dano)

    def resolve_prontidao(self, combatente):
        prontidao_nova = combatente.acao[3]
        if combatente.tem_vantagem and self.vantagem['tipo'] is 'defensiva':
            prontidao_nova += 1
        combatente.altera_prontidao(prontidao_nova)

    def todos_vivos(self):
        contagem_de_mortos = ['morto'
                              for i in self.combatentes
                              if i.saude <= 0]
        return False if 'morto' in contagem_de_mortos else True

    def determina_iniciativa(self):
        self.combatentes.sort(key=lambda jogador: jogador.prontidao)
        assert self.combatentes[0].prontidao != 0, 'Prontidao igual a zero!'
        return np.floor(abs(np.log2(self.combatentes[0].prontidao /
                                    self.combatentes[1].prontidao)))

    def registra_partida(self):
        pass


if __name__ == '__main__':
    partida = Partida()
