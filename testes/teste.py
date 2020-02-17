import unittest
from unittest.mock import Mock
import combate


COMBATENTE_1 = {"nome": "Juca",
                "saude": 10, "prontidao": 5,
                "arma": {"estocada": 3, "corte": 4}}

COMBATENTE_2 = {"nome": "Marcio",
                "saude": 8, "prontidao": 7,
                "arma": {"estocada": 4, "corte": 3}}


class TesteDeCombate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.objeto_testado = combate.Partida()
        cls.objeto_testado.combatentes = [COMBATENTE_1, COMBATENTE_2]
        for i in range(-1, 1):
            cls.objeto_testado.combatentes[i].oponente = cls.objeto_testado[i +
                                                                           1]

    def test_partida(self):
        pass


def cria_combatente_falso(configuracoes):

    def completa_atributos(objeto, configs, atributo):
        exec("objeto.{atr} = \
Mock(return_value=configs['{atr}'])".format(atr=atributo))

    combatente = combate.JogadorAleatorio("qualquer")
    for key in configuracoes.keys():
        completa_atributos(combatente, configuracoes, key)
    return combatente


if __name__ == '__main__':
    unittest.main()
