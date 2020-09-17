from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from classes.partida.partida import Partida
from tqdm import tqdm

vezes = 60000
codigo_estilos = {
    "Aikido": 0,
    "Torniquete": 1,
    "Jô-jitsu": 2}

matriz_vitorias = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]

for i in tqdm(range(vezes)):
    lutadores = [Lutador(Personagem(), Arma()), Lutador(Personagem(), Arma())]
    partida = Partida(lutadores[0], lutadores[1])
    partida.start()
    ganhou = partida.quem_ganhou()
    if (ganhou is not None):
        lutadores.remove(ganhou)
        perdeu = lutadores[0]
        matriz_vitorias[codigo_estilos[ganhou.estilo]][codigo_estilos[perdeu.estilo]] += 1

for i in range(3):
    print(matriz_vitorias[i], f"- somatoria: {sum(matriz_vitorias[i]) / (vezes * 0.01)}% ")
