from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from classes.partida.partida import Partida


lutadores = [Lutador(Personagem(), Arma()), Lutador(Personagem(), Arma())]
partida = Partida(lutadores[0], lutadores[1])
partida.start()
registro = partida.historico

for i in registro:
    print(i)
