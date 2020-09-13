from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from random import shuffle


def escolhe(lista):
    shuffle(lista)
    return lista.pop()


personagens = [Personagem() for i in range(10)]
armas = [Arma() for i in range(5)]

lutador1 = Lutador(escolhe(personagens), escolhe(armas))
lutador2 = Lutador(escolhe(personagens), escolhe(armas))

print(str(lutador1))
print(str(lutador2))
