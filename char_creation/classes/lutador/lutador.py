from ..armas.arma import Arma
from ..personagem.personagem import Personagem
from math import sqrt, log10, log2

class Lutador():
    def __init__(self, personagem, arma):
        self.personagem = personagem
        self.nome = self.personagem.nome
        self.estilo = self.personagem.estilo
        self.arma = arma

    @property
    def alcance(self):
        return round(self.personagem.envergadura + self.arma.tamanho, 3)

    @property
    def saude(self):
        return round(( 15 + (self.personagem.forca * self.personagem.envergadura) -
                     self.personagem.movimentacao ) / 2, 2)

    @property
    def agilidade(self):
        return round((self.personagem.destreza + (2 *
                     self.personagem.movimentacao) + self.alcance) / 2, 2)

    @property
    def velocidade(self):
        return round((((0.5 * ((2 * self.personagem.forca) *
                             self.personagem.destreza)) - (self.arma.peso +
                                                           1)**2) * 0.1) + 5, 2)

    @property
    def impacto(self):
        return round(self.personagem.forca * self.arma.peso, 2)

    @property
    def dano_corte(self):
        energia = sqrt(self.velocidade * self.impacto)
        fio = self.arma.ponta["corte"] + self.arma.rigidez
        return round((energia * fio) * self.arma.curvatura * 0.3, 2)

    @property
    def dano_estocada(self):
        perfuracao = sqrt(self.velocidade * self.impacto) * self.arma.ponta["estocada"]
        return round((perfuracao * self.personagem.movimentacao * 0.105) + 1, 2)

    @property
    def bonus_ofensivo(self):
        return round(((self.personagem.movimentacao * self.alcance) * 0.033) + 1.03, 2)

    @property
    def bonus_defensivo(self):
        return round((abs(self.personagem.movimentacao * self.velocidade
                     * self.arma.pnt_equilibrio)**0.55 * 0.05) + 0.2, 2)

    @property
    def custo_acao(self):
        return round(log10((abs(self.personagem.movimentacao *
                         self.personagem.destreza) + 1)**-1.2 * 10**3) *
                           (self.arma.peso), 2)

    def gera_placar(self):
        return {
                "nome": {self.nome},
                "estilo": {self.estilo},
                "saude": {self.saude},
                "iniciativa": {self.agilidade},
                "dano corte": {self.dano_corte},
                "dano estocada": {self.dano_estocada},
                "bonus ofensivo": {self.bonus_ofensivo},
                "bonus defensivo": {self.bonus_defensivo},
                "custo de ação": {self.custo_acao}}

    def __str__(self):
        return f'''{self.personagem.nome}, lutador de {self.personagem.estilo}.
saude: {self.saude}
agilidade: {self.agilidade}
alcance: {self.alcance}
dano de corte: {self.dano_corte}
dano de estocada: {self.dano_estocada}
bonus ofensivo: {self.bonus_ofensivo}
bonus defensivo: {self.bonus_defensivo}
custo de ação: {self.custo_acao}
'''
