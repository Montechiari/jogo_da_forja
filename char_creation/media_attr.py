from classes.personagem.personagem import Personagem
from classes.armas.arma import Arma
from classes.lutador.lutador import Lutador
from numpy import average


def reporta(dados, atributo):
    min_dd = min(dados)
    med_dd = average(dados)
    max_dd = max(dados)
    print(f"\n{atributo} min: {min_dd}\n{atributo} max: {max_dd}\n"
          f"{atributo} med: {med_dd}")


saudes = []
alcances = []
agilidades = []
velocidades = []
impactos = []
danos_crt = []
danos_stq = []
bonus_ofs = []
bonus_def = []
custos = []

for i in range(100000):
    persona = Personagem()
    arma = Arma()
    lutador = Lutador(persona, arma)
    print(f"{lutador.personagem.nome}, lutador de {lutador.personagem.estilo},"
          f" tem:\n{lutador.alcance} metros de alcance;\n"
          f"{lutador.saude} pontos de saude;\n"
          f"{lutador.agilidade} pontos de agilidade;\n"
          f"{lutador.velocidade} pontos de velocidade;\n"
          f"{lutador.impacto} pontos de impacto;\n"
          f"{lutador.dano_corte} dano de corte;\n"
          f"{lutador.dano_estocada} dano de estocada;\n"
          f"{lutador.bonus_ofensivo} bonus ofensivo;\n"
          f"{lutador.bonus_defensivo} bonus defensivo;\n"
          f"{lutador.custo_acao} de custo de ação.\n")

    alcances.append(lutador.alcance)
    saudes.append(lutador.saude)
    agilidades.append(lutador.agilidade)
    velocidades.append(lutador.velocidade)
    impactos.append(lutador.impacto)
    danos_crt.append(lutador.dano_corte)
    danos_stq.append(lutador.dano_estocada)
    bonus_ofs.append(lutador.bonus_ofensivo)
    bonus_def.append(lutador.bonus_defensivo)
    custos.append(lutador.custo_acao)

reporta(saudes, "saude")
reporta(alcances, "alcance")
reporta(agilidades, "agilidade")
reporta(velocidades, "velocidade")
reporta(impactos, "impacto")
reporta(danos_crt, "dano corte")
reporta(danos_stq, "dano estocada")
reporta(bonus_ofs, "bonus ofensivo")
reporta(bonus_def, "bonus defensivo")
reporta(custos, "custo de ação")
