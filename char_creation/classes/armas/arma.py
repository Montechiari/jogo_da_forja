from numpy.random import randint, normal, choice


class Arma:
    def __init__(self, peso=None, pnt_equilibrio=None,
                 pnt_percussao=None, curvatura=None, ponta=None,
                 tamanho=None, rigidez=None, fio=None):

        if (peso is None):
            self.peso = self.gera_peso()
        else:
            self.peso = peso

        if (pnt_equilibrio is None):
            self.pnt_equilibrio = self.gera_pnt_equilibrio()
        else:
            self.pnt_equilibrio = pnt_equilibrio

        if (tamanho is None):
            self.tamanho = self.gera_tamanho()
        else:
            self.tamanho = tamanho

        if (pnt_percussao is None):
            self.pnt_percussao = self.gera_pnt_percussao()
        else:
            self.pnt_percussao = pnt_percussao

        if (curvatura is None):
            self.curvatura = self.gera_curvatura()
        else:
            self.curvatura = curvatura

        if (ponta is None):
            self.ponta = self.gera_ponta()
        else:
            self.ponta = ponta

        if (rigidez is None):
            self.rigidez = self.gera_rigidez()
        else:
            self.rigidez = rigidez

        self.fio = 1
        self.durabilidade = 1


    def gera_peso(self):
        return normal(1, 0.1)

    def gera_pnt_equilibrio(self):
        return abs(normal(0, 0.08))

    def gera_pnt_percussao(self):
        try:
            percussao = 2 * (self.tamanho / 3)
        except Exception as e:
            percussao = None
        return percussao

    def gera_curvatura(self):
        if (randint(2) == 1):
            curva = 1
        else:
            curva = 1 + abs(normal(0, 0.1))
        return curva

    def gera_ponta(self):
        pontas = [{"nome": "punhal", "estocada": 1, "corte": 0.5},
                  {"nome": "gancho", "estocada": 0.3, "corte": 1},
                  {"nome": "clip", "estocada": 0.7, "corte": 0.7},
                  {"nome": "tanto", "estocada": 0.5, "corte": 0.9}]
        return choice(pontas)

    def gera_tamanho(self):
        return normal(0.6, 0.06)

    def gera_rigidez(self):
        return normal(1, 0.1)

    def __str__(self):
        return f'''tamanho: {self.tamanho}
peso: {self.peso}
ponto de equilibrio: {self.pnt_equilibrio}
ponto de percussao: {self.pnt_percussao}
curvatura: {self.curvatura}
ponta: {self.ponta["nome"]}, {self.ponta["corte"]}, {self.ponta["estocada"]}
rigidez: {self.rigidez}'''



if __name__ == "__main__":
    arma = Arma()
    print(str(arma))
