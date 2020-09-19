from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from classes.partida.partida import Partida
import csv
from tqdm import tqdm

VEZES = 1000000


dados_partida = []
for i in tqdm(range(VEZES)):
    lutadores = [Lutador(Personagem(), Arma()), Lutador(Personagem(), Arma())]
    partida = Partida(lutadores[0], lutadores[1])
    partida.start()
    dados_partida.append(partida.dados_treino_aposta())

with open("./dados/aposta.csv", "a") as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    for linha in tqdm(dados_partida):
        escritor.writerow(linha)
