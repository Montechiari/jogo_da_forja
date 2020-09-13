from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from random import shuffle


def escolhe(lista):
    shuffle(lista)
    return lista.pop()


personagem = Personagem()
armas = [Arma() for i in range(10)]

for i, arma in enumerate(armas):
    print(f"Arma {i + 1}:")
    print(str(Lutador(personagem, arma)))
