import copy

NOMES = ['carlos', 'marco']
SAUDE_MAX = 10
INICIATIVA_MAX = 10


class Jogador():
    def __init__(self, nome):
        self.nome = nome
        self.saude = SAUDE_MAX
        self.iniciativa = INICIATIVA_MAX


class Arena():
    def __init__(self):

        self.vantagem = {'quem': None, 'tipo': None}
        self.jogadores = [Jogador(NOMES[i]) for i in range(2)]

    def luta(self):
        def os_dois_vivos():
            vivos = True
            for jogador in self.jogadores:
                if jogador.saude <= 0:
                    vivos = False
            return vivos

        registro_de_acoes = []
        while os_dois_vivos():
            registro_de_acoes.append(self.novo_turno())
        return registro_de_acoes

    def novo_turno(self):
        fila_de_jogadores = sorted(copy(self.jogadores),
                                   key=lambda jogador: jogador.iniciativa)
        self.resolve_acao(*fila_de_jogadores)
        return [jogador.estado_atual for jogador in fila_de_jogadores]

    def resolve_acao(self, A_jogador, B_jogador):
        pass
