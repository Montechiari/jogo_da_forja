from ..personagem.personagem import Personagem
from ..armas.arma import Arma
from ..lutador.lutador import Lutador
from math import log2, floor
from numpy.random import randint


TAXA_VANTAGEM_DE_ESTILO = 0.15
ESTILOS_DE_LUTA = ["Aikido", "Torniquete", "Jô-jitsu"]
NOMES_ACOES = ["movimento ofensivo", "movimento defensivo",
               "ataque corte", "ataque estocada",
               "defesa corte", "defesa estocada", "nenhuma ação"]


class Placar:
    def __init__(self, lutador):
        self.lutador = lutador
        self.saude = lutador.saude
        self.iniciativa = lutador.agilidade
        self.ultima_acao = 0


class Partida:
    def __init__(self, lutador_A, lutador_B, verbose=False):
        self.verbose = verbose
        self.lutadores = {lutador_A.nome: lutador_A,
                          lutador_B.nome: lutador_B}
        # define quem tem vantagem pelo estilo de luta
        self.bonus_estilo = self.vantagem_de_estilo(lutador_A, lutador_B)
        # variavel para vantagem de movimentacao
        self.vantagem = {"quem": None, "tipo": None}
        # número do turno
        self.turno = 0
        # lutadores em ordem
        self.fila_lutadores = [Placar(lutador) for lutador in [lutador_A,
                                                               lutador_B]]
        self.fim_de_partida = False
        self.historico = []

    def ordena_por_iniciativa(self):
        if self.fila_lutadores[0].iniciativa != \
                self.fila_lutadores[1].iniciativa:
            self.fila_lutadores.sort(key=lambda ltdr: ltdr.iniciativa,
                                     reverse=True)
        else:
            self.fila_lutadores.sort(key=lambda ltdr: ltdr.lutador.personagem.movimentacao,
                                     reverse=True)
        # retorna quantidade de acoes extras
        return int(floor(abs(log2(self.fila_lutadores[0].iniciativa /
                                  self.fila_lutadores[1].iniciativa))))

    def efeitos_rodada(self, acao_A, acao_B):
        DE_ACOES_PARA_ALTERACOES = [["09", "09", "02", "03", "04", "04", "09"],
                                    ["19", "19", "12", "13", "14", "14", "19"],
                                    ["20", "21", "44", "23", "45", "64", "29"],
                                    ["30", "31", "32", "33", "74", "48", "39"],
                                    ["40", "41", "85", "47", "44", "44", "49"],
                                    ["40", "41", "46", "84", "44", "44", "49"]]

        # ---------------[tipo vant, mult. dano, tipo dano,mod. iniciativa]
        ALTERACOES = {"0": ['ofensiva', 0, None, 0],
                      "1": ['defensiva', 0, None, 0],
                      "2": [None, 1, "corte", -1],
                      "3": [None, 1, "estocada", -1],
                      "4": [None, 0, None, -1],
                      "5": ['defensiva', 1, "corte", 1],
                      "6": [None, 0.5, "corte", -1],
                      "7": [None, 0.5, "estocada", -1],
                      "8": ['defensiva', 1, "estocada", 1],
                      "9": [None, 0, None, 0]}

        alteracoes_codificadas = DE_ACOES_PARA_ALTERACOES[acao_A - 1][acao_B - 1]
        for i, lutador in enumerate(self.fila_lutadores):
            if lutador.iniciativa <= 0:
                alteracoes_codificadas = list(alteracoes_codificadas)
                alteracoes_codificadas[i] = "9"
                alteracoes_codificadas = "".join(alteracoes_codificadas)

        return (ALTERACOES[str(alteracoes_codificadas[0])],
                ALTERACOES[str(alteracoes_codificadas[1])])

    def consequencia(self, alteracoes):
        def aplicar():

            for i in range(2):
                # checa se alguem tem vantagem de movimentacao
                if (alteracoes[i][0] is not None):
                    self.vantagem['quem'] = self.fila_lutadores[i].lutador
                    self.vantagem['tipo'] = alteracoes[i][0]
                # checa se tem bonus de estilo de luta
                mod_dano = alteracoes[i][1]
                custo_acao = self.fila_lutadores[i].lutador.custo_acao
                if (self.fila_lutadores[i].lutador is self.bonus_estilo):
                    mod_dano += mod_dano * TAXA_VANTAGEM_DE_ESTILO
                    custo_acao -= custo_acao * TAXA_VANTAGEM_DE_ESTILO
                # calcula bonus ofensivo
                i_tem_vantagem = (self.vantagem['quem'] is
                                  self.fila_lutadores[i].lutador)
                i_desvantagem = (self.vantagem['quem'] is
                                 self.fila_lutadores[i - 1].lutador)
                vant_ofs = self.vantagem['tipo'] == "ofensiva"
                vant_def = self.vantagem['tipo'] == "defensiva"
                if (i_tem_vantagem and vant_ofs):
                    mod_dano *= self.fila_lutadores[i].lutador.bonus_ofensivo
                elif (i_desvantagem and vant_def):
                    mod_dano *= self.fila_lutadores[i - 1].lutador.bonus_defensivo
                # aplica dano
                corte = self.fila_lutadores[i].lutador.dano_corte * mod_dano
                estocada = self.fila_lutadores[i].lutador.dano_estocada * mod_dano
                if (alteracoes[i][2] == "corte"):
                    self.fila_lutadores[i - 1].saude -= corte
                elif (alteracoes[i][2] == "estocada"):
                    self.fila_lutadores[i - 1].saude -= estocada
                # deduz custo da acao
                self.fila_lutadores[i].iniciativa += custo_acao * alteracoes[i][3]
                if self.fila_lutadores[i].iniciativa < custo_acao:
                    self.fila_lutadores[i].iniciativa = custo_acao
                # limita saude minima a zero
                if self.fila_lutadores[i - 1].saude < 0:
                    self.fila_lutadores[i - 1].saude = 0
                    self.fim_de_partida = True
                    return "fim"
            return "continua"

        return aplicar

    def novo_turno(self):
        acao_extra = self.ordena_por_iniciativa()
        for i in range(acao_extra + 1):
            acao1 = self.pede_acao()
            if i == 0:
                acao2 = self.pede_acao()
            else:
                acao2 = 0
            self.fila_lutadores[0].ultima_acao = acao1
            self.fila_lutadores[1].ultima_acao = acao2
            aplicar = self.consequencia(self.efeitos_rodada(acao1, acao2))
            if(aplicar() == "fim"):
                self.print_placar(i)
                return
            self.print_placar(i)
            self.registrar()
        self.turno += 1
        return

    def print_placar(self, acao_n):
        if (self.verbose is True):
            if (self.vantagem['quem'] is None):
                vantage = "ninguem"
            else:
                vantage = self.vantagem['quem'].nome
            print(f"\nTurno {self.turno + 1}, Ação {acao_n + 1}. {vantage} tem vantagem {self.vantagem['tipo']}")
            for item in self.fila_lutadores:
                if item.ultima_acao is not None:
                    print(f'''{item.lutador.nome}:\nultima acao: {NOMES_ACOES[item.ultima_acao - 1]}\nsaude {item.saude} | iniciativa {item.iniciativa}\n''')
                else:
                    print(f'''{item.lutador.nome}:\nultima acao: nenhuma\nsaude {item.saude} | iniciativa {item.iniciativa}\n''')

    def start(self):
        self.print_placar(0)
        self.registrar()
        while (not self.fim_de_partida and (self.turno < 20)):
            self.novo_turno()
        self.registrar()

    def pede_acao(self):
        return randint(1, 7)

    def vantagem_de_estilo(self, lutadorA, lutadorB):
        # -- mod_dano de estilos!
        tem_vantagem = None
        estilo_A = lutadorA.estilo
        estilo_B = lutadorB.estilo
        idx_A = ESTILOS_DE_LUTA.index(estilo_A)
        idx_B = ESTILOS_DE_LUTA.index(estilo_B)
        if ((idx_A < idx_B) or (idx_A == 2 and idx_B == 0)):
            tem_vantagem = lutadorA
        elif (idx_A > idx_B):
            tem_vantagem = lutadorB
        return tem_vantagem

    def quem_ganhou(self):
        ganhou = None
        for i in range(2):
            if self.fila_lutadores[i].saude == 0:
                ganhou = self.fila_lutadores[i - 1].lutador
        return ganhou

    def registrar(self):
        vantagem, placares, ultimas_acoes = [], [], []
        for i, placar in enumerate(self.fila_lutadores):
            if self.vantagem['quem'] is placar.lutador:
                vantagem.append(i)
            elif self.vantagem['quem'] is None:
                vantagem.append(-1)
            if self.vantagem['tipo'] == "ofensiva":
                vantagem.append(0)
            else:
                vantagem.append(1)
            placares.extend(eval(repr(placar.lutador)))
            ultimas_acoes.append(placar.ultima_acao)
        registro = [self.turno] + vantagem + placares + ultimas_acoes
        self.historico.append(registro)

    def dados_treino_aposta(self):
        quem_ganha = []
        placares = []
        for i, placar in enumerate(self.fila_lutadores):
            placares.extend(eval(repr(placar.lutador)))
            placares.append(ESTILOS_DE_LUTA.index(placar.lutador.estilo))
            if self.quem_ganhou() is placar.lutador:
                quem_ganha.append(i)
        return placares + quem_ganha
