from copy import copy
import numpy as np

NOMES = ['carlos', 'marco']
SAUDE_PRONTIDAO_MAX = 20
SAUDE_PRONTIDAO_MIN = 8
DANO_ARMA_MAX = 10
DANO_ARMA_MIN = 3


class Combatente():
    def __init__(self, nome):

        self.nome = nome
        self.saude, self.prontidao, self.arma = self.sorteia_atributos()
        self.oponente = None

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
    def decide_acao(self):
        pass


class JogadorRedeNeural(Combatente):
    def decide_acao(self):
        pass


class JogadorAleatorio(Combatente):
    def decide_acao(self):
        pass


class Partida():
    def __init__(self):

        self.vantagem = {'quem': None, 'tipo': None}
        self.combatentes = self.cria_combatentes()
        self.status = None

        self.turno_numero = 1
        while self.todos_vivos():
            self.novo_turno()

        self.registra_partida()

    def cria_combatentes(self):
        combatentes = [Combatente(NOMES[i]) for i in range(2)]
        ordem_invertida = copy(combatentes)
        ordem_invertida.reverse()
        for i in range(2):
            combatentes[i].oponente = ordem_invertida[i]
        return combatentes

    def novo_turno(self):

        acao_extra = self.determina_iniciativa

        for individuo in self.combatentes:
            individuo.decide_acao()

        if self.contabiliza_acoes() == 'segue o jogo':
            for i in range(acao_extra):
                pass

        self.turno_numero += 1
        return 'fim de turno'

    def contabiliza_acoes(self):
        pass

    def todos_vivos(self):
        contagem_de_mortos = ['morto'
                              for i in self.combatentes
                              if i.saude <= 0]
        return True if 'morto' in contagem_de_mortos else False

    def determina_iniciativa(self):
        self.combatentes.sort(key=lambda jogador: jogador.prontidao)
        assert self.combatentes[0].prontidao != 0, 'Prontidao igual a zero!'
        return np.floor(abs(np.log2(self.combatentes[0].prontidao /
                                    self.combatentes[1].prontidao)))

    def registra_partida(self):
        pass


if __name__ == '__main__':
    partida = Partida()
