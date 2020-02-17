import unittest
# import combate
import csv
import json
import numpy as np


COMBATENTE_1 = {"nome": "Juca",
                "saude": 8.0, "prontidao": 7.0,
                "arma": {"estocada": 3.0, "corte": 4.0}}
COMBATENTE_2 = {"nome": "Marcio",
                "saude": 10.0, "prontidao": 5.0,
                "arma": {"estocada": 4.0, "corte": 3.0}}
DUMMIES = [COMBATENTE_1, COMBATENTE_2]

MENSAGEM_DE_ENTRADA = {"mensagem": "entrada",
                       "turno": 1,
                       "iniciativa": DUMMIES[0]["nome"],
                       "vantagem": {"quem": None, "tipo": None},
                       "combatentes": DUMMIES,
                       "jogadas": []
                       }

NOME_DE_ACAO = ['movimento ofensivo', 'movimento defensivo',
                'ataque corte', 'ataque estocada',
                'defesa corte', 'defesa estocada']


class TabelaResultadoCombate():
    def __init__(self, dict_turno):
        self.assimila_dicionario(dict_turno)
        self.tabela = self.tabela_resultados_padrao(self.leitor_csv())

    def leitor_csv(self):
        with open("resultados_combate.csv") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            return np.array([linha for linha in leitor])

    def tabela_resultados_padrao(self, array_csv):
        tabela = np.reshape(array_csv, (6, 6, 6))
        return tabela

    def valor(self, acao_primeiro, acao_segundo):
        return self.tabela[acao_primeiro][acao_segundo]

    def assimila_dicionario(self, dicionario):
        for chave in dicionario:
            exec(f"self.{chave} = dicionario['{chave}']")

    def atualiza_atributos_combatente(self, combatente, saude_prontidao):
        combatente['saude'], combatente['prontidao'] = saude_prontidao

    def mensagem_resultante(self, acao_primeiro, acao_segundo):
        MENSAGEM_DE_ENTRADA["jogadas"] = [acao_primeiro, acao_segundo]
        primeira_mensagem = json.dumps(MENSAGEM_DE_ENTRADA, indent=2)
        saida = self.valor(acao_primeiro, acao_segundo)
        self.vantagem = {"quem": saida[0], "tipo": saida[1]}
        for i in range(2, 4, 2):
            self.atualiza_atributos_combatente(self.combatentes[int((i / 2) -
                                                                    1)],
                                               (float(saida[i]),
                                                float(saida[i + 1])))
        segunda_mensagem = f'''
            "mensagem": "saida",
            "turno": {self.turno + 1},
            "iniciativa": '{"Juca" if saida[3] > saida[5] else "Marcio"}',
            "vantagem": {self.vantagem},
            "combatentes": {self.combatentes},
            "jogadas": []'''
        segunda_mensagem = eval("".join(["{", segunda_mensagem, "}"]))
        segunda_mensagem = json.dumps(segunda_mensagem, indent=2)
        return "[" + primeira_mensagem + ",\n" + segunda_mensagem + "]"


class TesteDeCombate(unittest.TestCase):

    def setUp(self):
        self.partida_falsa = combate.Partida()
        self.partida_falsa.combatentes = self.partida_falsa.cria_combatentes()
        self.combatentes_falsos = self.partida_falsa.combatentes
        for i in range(2):
            padroniza_combatentes(self.combatentes_falsos[i],
                                  DUMMIES[i])
        self.partida_falsa.determina_iniciativa()

    def test_combatentes_falsos(self):
        for i, dummy in enumerate(DUMMIES):
            for key in dummy:
                self.assertEqual(
                    eval("self.combatentes_falsos[{}].{}".format(i, key)),
                    dummy[key])

    def test_choque_entre_armas(self):
        # Quando os dois combatentes realizam ataque corte.
        for combatente in self.combatentes_falsos:
            combatente.acao = 3
        self.partida_falsa.traduz_acoes(*self.combatentes_falsos)
        for combatente in self.combatentes_falsos:
            self.partida_falsa.aplica_efeitos_de_acao(combatente)
        for i in range(2):
            self.assertEqual(self.combatentes_falsos[i].saude,
                             DUMMIES[i]["saude"])
            self.assertEqual(self.combatentes_falsos[i].prontidao,
                             DUMMIES[i]["prontidao"] - 1)

    def test_duas_defesas(self):
        # Quando os dois defendem: apenas diminui a prontidao deles.
        for i in range(5, 7):
            for j in range(5, 7):
                prontidoes_esperadas = []
                for k, combatente in enumerate(self.combatentes_falsos):
                    acoes = [i, j]
                    prontidoes_esperadas.append(combatente.prontidao - 1)
                    combatente.acao = acoes[k]
                self.partida_falsa.traduz_acoes(*self.combatentes_falsos)
                for k, combatente in enumerate(self.combatentes_falsos):
                    self.partida_falsa.aplica_efeitos_de_acao(combatente)
                    self.assertEqual(combatente.prontidao,
                                     prontidoes_esperadas[k])


def padroniza_combatentes(combatente, configuracoes):
    for key in configuracoes.keys():
        exec("combatente.{atr} = configuracoes['{atr}']".format(atr=key))


if __name__ == '__main__':
    # unittest.main()
    tabela = TabelaResultadoCombate(MENSAGEM_DE_ENTRADA)

    with open("testejson.json", "w") as arquivo_json:
        # json.load(arquivo_json)
        arquivo_json.write("{ dados:\n")
        for i in range(6):
            for j in range(6):
                mensagem = tabela.mensagem_resultante(i, j)
                arquivo_json.write(mensagem + ",\n")
            # json.dump(mensagem, arquivo_json)
