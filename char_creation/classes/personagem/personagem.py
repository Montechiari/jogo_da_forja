from numpy.random import choice
from ..locais.locais_de_origem import Provincia


class Personagem:
    def __init__(self, provincia=None):
        if (provincia is None):
            provincia = choice(["Siracusa", "Damasco", "Dudinka"])
        self.provincia = provincia
        self.gerar_personagem()

    def gerar_personagem(self):
        prv = Provincia(self.provincia)
        atributos = prv.char_gen()

        self.nome = atributos["nome"]
        self.estilo = atributos["estilo"]
        self.forca = atributos["atributos"]["forca"]
        self.destreza = atributos["atributos"]["destreza"]
        self.movimentacao = atributos["atributos"]["movimentacao"]
        self.envergadura = atributos["atributos"]["envergadura"]

    def __str__(self):
        return f'''nome: {self.nome}
provincia: {self.provincia}
estilo: {self.estilo}
força: {self.forca}
destreza: {self.destreza}
movimentação: {self.movimentacao}
envergadura: {self.envergadura}'''

if __name__ == "__main__":
    personagem = Personagem()
    print(str(personagem))
