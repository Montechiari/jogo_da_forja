import unittest
import combate


COMBATENTE_1 = {"nome": "Juca",
                "saude": 8, "prontidao": 7,
                "arma": {"estocada": 3, "corte": 4}}
COMBATENTE_2 = {"nome": "Marcio",
                "saude": 10, "prontidao": 5,
                "arma": {"estocada": 4, "corte": 3}}
DUMMIES = [COMBATENTE_1, COMBATENTE_2]


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
    unittest.main()
