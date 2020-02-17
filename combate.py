import numpy as np
import operator
from functools import reduce
import csv

SAUDE_PRONTIDAO_MAX = 25
SAUDE_PRONTIDAO_MIN = 8
DANO_ARMA_MAX = 8
DANO_ARMA_MIN = 3

# Caractere da esquerda eh acao do combatente com iniciativa; direita, do outro
COMBINACOES_DE_ACOES = [["09", "09", "02", "03", "04", "03"],
                        ["19", "19", "12", "13", "14", "13"],
                        ["20", "21", "44", "23", "48", "64"],
                        ["30", "31", "32", "33", "74", "48"],
                        ["40", "41", "84", "47", "44", "44"],
                        ["40", "41", "46", "84", "44", "44"]]

# [tipo de vantagem, quanto inflige dano, tipo de dano, prontidao]
ACOES_CODIFICADAS = {"0": ['ofensiva', 0, '', 0],
                     "1": ['defensiva', 0, '', 0],
                     "2": ['', 1, 'c', -1],
                     "3": ['', 1, 'e', -1],
                     "4": ['', 0, '', -1],
                     "5": ['', 0, '', -1],
                     "6": ['', 0.5, 'c', -1],
                     "7": ['', 0.5, 'e', -1],
                     "8": ['', 0, '', 1],
                     "9": ['', 0, '', 0]}

NOME_DE_ACAO = ['movimento ofensivo', 'movimento defensivo',
                'ataque corte', 'ataque estocada',
                'defesa corte', 'defesa estocada']


class Arma():
    def __init__(self, estocada, corte):
        self.corte = corte
        self.estocada = estocada


class Combatente():
    def __init__(self, nome):

        self.nome = nome
        self.saude, self.prontidao, self.arma = self.sorteia_atributos()
        self.oponente = None
        self.historico_de_acoes = []
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
        arma = Arma(*sorteio(DANO_ARMA_MAX, DANO_ARMA_MIN))
        return saude, prontidao, arma

    def altera_saude(self, montante):
        self.saude += montante

    def altera_prontidao(self, montante):
        if (self.prontidao + montante) > 0:
            self.prontidao += montante
        else:
            self.prontidao = 1

    def inflige_dano(self, tipo):
        dano = self.arma[tipo]
        self.oponente.altera_saude(dano * -1)

    def resumo_de_atributos(self):
        return "{nome}, {saude}s, {prontidao}p, ({estocada}e/{corte}c)".format(
                nome=self.nome, saude=self.saude, prontidao=self.prontidao,
                estocada=self.arma.estocada, corte=self.arma.corte
                                                                              )

    def mensagem_acao(self):
        return "{nome} realiza {acao}".format(nome=self.nome,
                                              acao=NOME_DE_ACAO[self.acao - 1])

    def mensagem_iniciativa(self):
        return "{nome} tem a iniciativa.".format(nome=self.nome)

    def mensagem_atributos(self):
        return "{nome} tem {saude} pontos de vida \
e {prontidao} pontos de prontidao.".format(nome=self.nome,
                                           saude=self.saude,
                                           prontidao=self.prontidao)

    def mensagem_arma(self):
        return "A espada de {} causa {} de dano de estocada e {} \
de dano de corte.".format(self.nome, self.arma["estocada"], self.arma["corte"])

    def mensagem_vantagem(self, tipo):
        return "{nome} assume vantagem {vantagem}.".format(nome=self.nome,
                                                           vantagem=tipo)

    def mensagem_dano(self, dano):
        return "{nome} recebe {dano} pontos de dano!".format(
            nome=self.oponente.nome,
            dano=dano)


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
    def __init__(self, nome):
        Combatente.__init__(self, nome)

    def decide_acao(self):
        self.acao = np.random.randint(1, 7)
        return self.acao


class RegistroDeTurno():
    def __init__(self):
        pass

    def coleta_dados_iniciais(self, combatentes):
        self.dados_iniciais = {}
        for combatente in combatentes:
            self.dados_iniciais[combatente.nome] = [combatente.saude,
                                                    combatente.prontidao]


class Vantagem():
    def __init__(self, quem=None, tipo=None):
        self.quem = quem
        self.tipo = tipo


class Partida():
    def __init__(self):
        pass

    def inicia(self):
        self.vantagem = Vantagem()
        self.registro = RegistroDeTurno()
        self.combatentes = self.cria_combatentes()
        self.registro.coleta_dados_iniciais(self.combatentes)

        self.turno_numero = 1
        while self.todos_vivos() and self.turno_numero < 20:
            self.novo_turno()

    def cria_combatentes(self):
        combatentes = [JogadorAleatorio("Carlos"), JogadorAleatorio("Hicham")]
        for i in range(-1, len(combatentes) - 1):
            combatentes[i].oponente = combatentes[i + 1]
        return combatentes

    def novo_turno(self):

        numero_de_acoes_extras = self.determina_iniciativa()

        self.imprime_cabecalho()

        for combatente in self.combatentes:
            combatente.decide_acao()
        print(self.mensagem_sobre_acao())

        self.traduz_acoes(*self.combatentes)

        # pontuacao = [' e ', "."]
        dicionario_de_efeitos = {self.combatentes[0].nome: [],
                                 self.combatentes[1].nome: []}
        frases = [self.aplica_efeitos_de_acao(combatente)
                  for combatente in self.combatentes]
        conjunto = []
        for frase in frases:
            conjunto.extend(frase)
        for frase in conjunto:
            dicionario_de_efeitos[frase[0]].append(frase[1])
        self.imprime_consequencias(dicionario_de_efeitos)

        while numero_de_acoes_extras > 0:
            mensagem = ["Ação extra: –", self.combatentes[0].nome,
                        "realizou",
                        NOME_DE_ACAO[self.combatentes[0].decide_acao() - 1]]
            print(" ".join(mensagem))
            self.combatentes[0].decide_acao()
            self.traduz_acoes(*self.combatentes, acao_extra=True)
            self.aplica_efeitos_de_acao(self.combatentes[0])
            numero_de_acoes_extras -= 1

        self.turno_numero += 1
        return 'fim de turno'

    def traduz_acoes(self, ativo, passivo, acao_extra=False):
        if acao_extra:
            ativo.acao = ACOES_CODIFICADAS[str(ativo.acao - 1)]
        else:
            indice_de_acao = COMBINACOES_DE_ACOES[ativo.acao - 1
                                                  ][passivo.acao - 1]
            for i, combatente in enumerate([ativo, passivo]):
                combatente.acao = ACOES_CODIFICADAS[indice_de_acao[i]]

    def aplica_efeitos_de_acao(self, combatente):
        relatorio = []
        self.resolve_prontidao(combatente)
        relatorio.append(self.resolve_dano(combatente))
        if combatente.acao[0] != '':
            relatorio.append(self.resolve_vantagem(combatente))
        return relatorio

    def resolve_vantagem(self, combatente):
        self.vantagem = Vantagem(combatente, combatente.acao[0])
        combatente.oponente.tem_vantagem = False
        combatente.tem_vantagem = True
        saida = [combatente.nome,
                 "assume vantagem {tipo}".format(tipo=self.vantagem.tipo)]
        return saida

    def resolve_dano(self, combatente):
        dano = 0
        if combatente.acao[2] == 'c':
            dano = combatente.arma.corte
        elif combatente.acao[2] == 'e':
            dano = combatente.arma.estocada
        if (combatente.tem_vantagem and self.vantagem.tipo == 'ofensiva'):
            dano *= 2
        elif (combatente.oponente.tem_vantagem and self.vantagem.tipo ==
              'defensiva'):
            dano *= 0.5
        if dano > 0:
            combatente.oponente.altera_saude(-dano)
            return [combatente.oponente.nome,
                    "recebe {dano} pontos de dano".format(dano=dano)]
        else:
            return [combatente.oponente.nome, ""]

    def resolve_prontidao(self, combatente):
        prontidao_nova = combatente.acao[3]
        if combatente.tem_vantagem and self.vantagem.tipo == 'defensiva':
            prontidao_nova += 1
        combatente.altera_prontidao(prontidao_nova)

    def todos_vivos(self):
        contagem_de_mortos = ['morto'
                              for i in self.combatentes
                              if i.saude <= 0]
        return False if 'morto' in contagem_de_mortos else True

    def determina_iniciativa(self):
        self.combatentes.sort(key=lambda jogador: jogador.prontidao,
                              reverse=True)
        assert self.combatentes[0].prontidao != 0, 'Prontidao igual a zero!'
        return np.floor(abs(np.log2(self.combatentes[0].prontidao /
                                    self.combatentes[1].prontidao)))

    def reporta_estatisticas(self):
        for combatente in sorted(self.combatentes, key=lambda x: x.nome):
            print(combatente.mensagem_atributos())

    def imprime_cabecalho(self):
        superior = "\nTurno {t}. {resumo_A} | {resumo_B}".format(
                    t=self.turno_numero,
                    resumo_A=self.combatentes[0].resumo_de_atributos(),
                    resumo_B=self.combatentes[1].resumo_de_atributos())
        iniciativa = "{nome} tem iniciativa.".format(
                      nome=self.combatentes[0].nome)
        vantagem = "{nome} tem vantagem {tipo}.".format(
                    nome=self.vantagem.quem.nome, tipo=self.vantagem.tipo
                    ) if self.vantagem.quem is not None else "Ninguém tem \
vantagem."
        print(superior, "\n" + iniciativa, vantagem)

    def mensagem_sobre_acao(self):
        pontuacao = [" e ", "."]
        acoes_por_extenso = ["{nome} realizou {acao}{ponto}".format(
            nome=combatente.nome,
            acao=NOME_DE_ACAO[combatente.acao - 1],
            ponto=pontuacao[i]
                                                                    )
                             for i, combatente in enumerate(self.combatentes)]
        return "".join(acoes_por_extenso)

    def imprime_consequencias(self, dicionario):
        pontuacao = [" e ", "."]
        for key in dicionario.keys():
            if '' in dicionario[key]:
                dicionario[key].remove('')
            if dicionario[key] != []:
                mensagem = []
                for i, frase in enumerate(dicionario[key]):
                    mensagem.append(frase + pontuacao[i - 1])
                print("–", key, "".join(reversed(mensagem)))
            else:
                print("– Não houve consequência para {nome}.".format(nome=key))


if __name__ == '__main__':
    # partida = Partida()
    with open("./testes/resultados_combate.csv") as arquivocsv:
        leitor = csv.reader(arquivocsv)
        for row in leitor:
            print(row)
