from ..personagem.personagem import Personagem
from ..armas.arma import Arma
from ..lutador.lutador import Lutador

class Partida:
    def __init__(self, lutador_A, lutador_B):
        self.lutadores = {lutador_A.nome: lutador_A,
                          lutador_B.nome: lutador_B}
        self.vantagem = {"quem": None, "tipo": None}
        self.turno = 1

    def efeito_rodada(self, acao_A, acao_B):
        pass

    def inicia_tabela_acoes(self):
        pass
