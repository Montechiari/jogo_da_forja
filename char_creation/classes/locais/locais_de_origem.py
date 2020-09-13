import json
from numpy.random import choice, normal

class Provincia:
    def __init__(self, nome):
        self.nome = nome
        self.config()

    def config(self):
        try:
            with open(f"classes/locais/configs/{self.nome}.json") as f:
                configuracao = json.load(f)
            self.estilo = configuracao["estilo"]
            self.char_nomes = configuracao["char_nomes"]
            self.char_sobrenomes = configuracao["char_sobrenomes"]
            self.gen_params = configuracao["gen_params"]
        except Exception as e:
            print(e)

    def char_gen(self):
        char_dict = {}
        char_dict["provincia"] = self.nome
        char_dict["estilo"] = self.estilo

        nome = choice(self.char_nomes)
        sobrenome = choice(self.char_sobrenomes)
        char_dict["nome"] = f"{nome} {sobrenome}"

        char_dict["atributos"] = self.gen_atributos()
        return char_dict

    def gen_atributos(self):
        return {chv: normal(val[0], val[1])
                for (chv, val) in self.gen_params.items()}



if __name__ == "__main__":
    provincia = Provincia(choice(["Siracusa", "Damasco", "Dudinka"]))
    char = provincia.char_gen()
    print("Teste da classe Provincia. Gerador de personagem:")
    print(f'''nome = {char["nome"]}
provincia = {char["provincia"]}
estilo = {char["estilo"]}
força = {char["atributos"]["forca"]}
destreza = {char["atributos"]["destreza"]}
movimentação = {char["atributos"]["movimentacao"]}
envergadura = {char["atributos"]["envergadura"]}''')

