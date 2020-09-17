from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from classes.partida.partida import Partida
from tqdm import tqdm


lutadores = [Lutador(Personagem(), Arma()), Lutador(Personagem(), Arma())]

print("\n")
for lutador in lutadores:
    print(lutador)

aposta = "---"
while (aposta != lutadores[0].nome) and (aposta != lutadores[1].nome):
    aposta = input("Digite o nome do lutador que voce espera que vença:")

partida = Partida(lutadores[0], lutadores[1])
partida.start()
ganhou = partida.quem_ganhou()
print(f"{ganhou.nome} venceu a partida.")

if (ganhou.nome == aposta):
    print("Voce venceu a aposta!")
else:
    print("Voce perdeu a aposta...")
