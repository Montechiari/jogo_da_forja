import numpy as np
from keras.models import load_model
import tensorflow as tf
from tqdm import tqdm
import os

# marcador de vantagem: (jogador, tipo de vantagem); ex: (marcos, ofensivo)
# ofensivo = 0; defensivo = 1
VANTAGEM = (None, 0)


def acao_ataque(ofensor, defensor):
    # Ataque com conexao (efetivo)
    dano = ofensor['arma'][ofensor['acao'][1]]
    if VANTAGEM == (defensor, 1):
        dano *= 0.5
    elif VANTAGEM == (ofensor, 0):
        dano *= 2
    defensor['saude'] -= dano
    ofensor['iniciativa'] -= 1
    return dano


def acao_defesa(defensor):
    defensor['iniciativa'] -= 1


def acao_combate(ofensor, defensor):
    # Defesa certa ou defesa errada com vantagem defensiva
    if ((ofensor['acao'][1] == defensor['acao'][1]) != (VANTAGEM == (defensor,
                                                                     1))):
        defensor['iniciativa'] += 1
        ofensor['iniciativa'] -= 1
        dano = 0

    # Defesa errada sem vantagem defensiva
    elif ofensor['acao'][1] != defensor['acao'][1]:
        if VANTAGEM != (ofensor, 0):
            defensor['iniciativa'] -= 1
            ofensor['iniciativa'] -= 1
            dano = ofensor['arma'][ofensor['acao'][1]] * 0.5
            defensor['saude'] -= dano
        else:
            defensor['iniciativa'] -= 1
            ofensor['iniciativa'] -= 1
            dano = ofensor['arma'][ofensor['acao'][1]]
            defensor['saude'] -= dano

    # Defesa certa e vantagem defensiva
    elif ((ofensor['acao'][1] == defensor['acao'][1]) and (VANTAGEM ==
                                                           (defensor, 1))):
        defensor['iniciativa'] += 2
        ofensor['iniciativa'] -= 2
        dano = 0

    # retorna dano
    return dano


def acao_empate(ofensor, defensor):
    ofensor['iniciativa'] -= 1
    defensor['iniciativa'] -= 1


def acao_movimento(jogador):
    global VANTAGEM
    VANTAGEM = (jogador, jogador['acao'][1])


def cria_lutador(nome):
    jogador = {'nome': nome}
    jogador['saude'] = round(np.random.triangular(3, 5, 7))
    jogador['energia'] = 10 - jogador['saude']
    arma = np.random.randint(1, 4) * 0.5
    # Danos de e estocada e corte
    jogador['arma'] = (2.5 - arma, arma + 1)
    # print(jogador)
    jogador['iniciativa'] = jogador['energia'] // 2
    # Tabela de transicao de acoes do jogador
    jogador['markov'] = [0 for i in range(36)]
    # Lista de acoes realizadas
    jogador['lista_de_acoes'] = []
    jogador['acao'] = None
    jogador['acao_anterior'] = None
    # registro de jogadas
    jogador['in'], jogador['out'] = [], []
    return jogador


def registra_jogada(n_turno, n_acao, jogadores):

    for i, jogador in enumerate(jogadores):

        if VANTAGEM[0] is None:
            quem_tem_vantagem = 0
        elif VANTAGEM[0] is jogador:
            quem_tem_vantagem = 1
        else:
            quem_tem_vantagem = 2

        dados = '{} {} {} {} {} {} {} {} {} {} {} {}'.format(n_turno, n_acao,
                                                             jogador['saude'],
                                                             jogadores[i - 1]['saude'],
                                                             jogador['iniciativa'],
                                                             jogadores[i - 1]['iniciativa'],
                                                             jogador['arma'][0],
                                                             jogador['arma'][1],
                                                             jogadores[i - 1]['arma'][0],
                                                             jogadores[i - 1]['arma'][1],
                                                             quem_tem_vantagem,
                                                             VANTAGEM[1])
        try:
            acao = (jogador['acao_anterior'][0] *
                    2) + jogador['acao_anterior'][1] + 1
        except TypeError:
            acao = 0

        try:
            acao_inimigo = (jogadores[i - 1]['acao_anterior'][0] *
                            2) + jogadores[i - 1]['acao_anterior'][1] + 1
        except TypeError:
            acao_inimigo = 0

        dados = ''.join([dados, ' ', str(acao), ' ', str(acao_inimigo), ' ',
                         ' '.join([str(i) for i in markov_normalizada(jogadores[i - 1])])])

        jogador['in'].append(dados)
        # print(jogador['in'][-1])


def cria_jogada(jogador, modelo):
    jogador['acao_anterior'] = jogador['acao']
    if modelo is None:
        jogador['acao'] = (np.random.randint(3), np.random.randint(2))
    else:
        vetor_entrada = [float(i) for i in jogador['in'][-1].split(' ')]
        output_vector = modelo.predict(np.array([vetor_entrada]))[0]
        output_max = np.argmax(output_vector)
        jogador['acao'] = inverso_chave_jogada(output_max)

        # print('acao:', jogador['acao'], output_vector)
    jogador['lista_de_acoes'].append(jogador['acao'])
    if jogador['acao_anterior'] is not None:
        jogador['markov'][chave_jogada(jogador)] += 1
    jogador['out'].append(' '.join(['1' if i == ((jogador['acao'][0] * 2) +
                                                 jogador['acao'][1]) else '0'
                                    for i in range(6)]))
    # print(jogador['out'][-1])


def chave_jogada(jogador):
    a, b = jogador['acao'], jogador['acao_anterior']
    return ((a[0] * 2) + a[1]) + (6 * ((b[0] * 2) + b[1]))


def inverso_chave_jogada(numero):
    b = numero % 2
    a = numero // 2
    return a, b


def markov_normalizada(jogador):
    qtd_horizontal = [sum(jogador['markov'][i * 6: (i * 6) + 6])
                      for i in range(6)]
    qtd_horizontal = [i if i > 0 else 1 for i in qtd_horizontal]
    return [item / qtd_horizontal[i // 6]
            for i, item in enumerate(jogador['markov'])]


def traduz_jogada(jogada):
    if jogada[0] == 0:
        if jogada[1] == 0:
            texto = 'movimento ofensivo.'
        else:
            texto = 'movimento defensivo.'
    elif jogada[0] == 1:
        if jogada[1] == 0:
            texto = 'ataque estocada.'
        else:
            texto = 'ataque corte.'
    else:
        if jogada[1] == 0:
            texto = 'defesa estocada.'
        else:
            texto = 'defesa corte.'
    return texto


def resolve_jogada(jogadores):
    ativo, passivo = jogadores[0], jogadores[1]

    # print(ativo['nome'], '({} hp)'.format(ativo['saude']), 'performa',
          # traduz_jogada(ativo['acao']))
    # print(passivo['nome'], '({} hp)'.format(passivo['saude']), 'performa',
          # traduz_jogada(passivo['acao']))

    # Caso sejam dois movimento, quem tem iniciativa tem vantagem
    if ativo['acao'][0] + passivo['acao'][0] == 0:
        acao_movimento(ativo)
        # print(ativo['nome'], 'assume posicao de vantagem.\n')

    # Resolve ataque, checa fim, resolve vantagem
    elif ativo['acao'][0] == 1 and passivo['acao'][0] == 0:
        dano = acao_ataque(ativo, passivo)
        # checa fim
        if passivo['saude'] <= 0:
            # print(passivo['nome'], 'recebe', dano, 'de dano e morre.\n')
            return 'fim de jogo'
        acao_movimento(passivo)
        # print(passivo['nome'], 'recebe', dano, 'de dano',
              # 'e assume posicao de vantagem.\n')

    # Resolve defesa, resolve vantagem
    elif ((ativo['acao'][0] == 2 and passivo['acao'][0] == 0) or
          (passivo['acao'][0] == 2 and ativo['acao'][0] == 0)):
        if ativo['acao'][0] == 2 and passivo['acao'][0] == 0:
            defensor, movente = ativo, passivo
        else:
            defensor, movente = passivo, ativo
        acao_defesa(defensor)
        acao_movimento(movente)
        # print(movente['nome'], 'assume posicao de vantagem.\n')

    # Resolve vantagem, Resolve ataque, checa fim
    elif ativo['acao'][0] == 0 and passivo['acao'][0] == 1:
        acao_movimento(ativo)
        dano = acao_ataque(passivo, ativo)
        # checa fim
        if ativo['saude'] <= 0:
            # print(ativo['nome'], 'recebe', dano, 'de dano e morre.\n')
            return 'fim de jogo'
        # print(ativo['nome'], 'recebe', dano, 'de dano',
              # 'e assume posicao de vantagem.\n')

    # Resolve combate, checa fim
    elif ((ativo['acao'][0] == 1 or passivo['acao'][0] == 1) and
          (ativo['acao'][0] == 2 or passivo['acao'][0] == 2)):
        if ativo['acao'][0] == 1:
            atacante, defensor = ativo, passivo
        else:
            atacante, defensor = passivo, ativo
        dano = acao_combate(atacante, defensor)
        # checa fim
        if defensor['saude'] <= 0:
            # print(defensor['nome'], 'recebe', dano, 'de dano e morre.\n')
            return 'fim de jogo'
        # print(defensor['nome'], 'recebe', dano, 'de dano.\n')

    # Resolve defesa, resolve defesa
    elif ativo['acao'][0] == 2 and passivo['acao'][0] == 2:
        acao_defesa(ativo)
        acao_defesa(passivo)
        # print('Ninguém se feriu.\n')

    # Resolve ataque, checa fim, resolve ataque, checa fim
    elif ((ativo['acao'] == (1, 0) and passivo['acao'] == (1, 1)) or
          (ativo['acao'] == (1, 1) and passivo['acao'] == (1, 0))):
        dano_1 = acao_ataque(ativo, passivo)
        # checa fim
        if passivo['saude'] <= 0:
            # print(passivo['nome'], 'recebe', dano_1, 'de dano e morre.\n')
            return 'fim de jogo'
        dano_2 = acao_ataque(passivo, ativo)
        if ativo['saude'] <= 0:
            # print(ativo['nome'], 'recebe', dano_2, 'de dano e morre.\n')
            return 'fim de jogo'
        # print(passivo['nome'], 'recebe', dano_1, 'de dano,',
              # ativo['nome'], 'recebe', dano_2, 'de dano.\n')

    # Resolve ataque, resolve ataque, checa fim
    elif ativo['acao'] == (1, 0) and passivo['acao'] == (1, 0):
        dano_1 = acao_ataque(ativo, passivo)
        dano_2 = acao_ataque(passivo, ativo)
        # print(passivo['nome'], 'recebe', dano_1, 'de dano,',
              # ativo['nome'], 'recebe', dano_2, 'de dano.\n')
        if ativo['saude'] <= 0 or passivo['saude'] <= 0:
            return 'fim de jogo'

    # Resolve empate
    elif ativo['acao'] == (1, 1) and passivo['acao'] == (1, 1):
        acao_empate(ativo, passivo)
        # print('As armas colidem, ninguém se feriu.\n')

    return 'turno concluido'


def turno(jogadores):

    # print(jogadores[0]['nome'], 'tem', jogadores[0]['iniciativa'],
          # 'de iniciativa,', jogadores[1]['nome'], 'tem',
          # jogadores[1]['iniciativa'], 'de iniciativa.\n')

    # calcula quantas acoes cada um tem
    jogadores = sorted(jogadores, key=lambda jogador: jogador['iniciativa'],
                       reverse=True)
    jogadores[1]['qtd_acoes'] = 2
    if jogadores[0]['iniciativa'] != 0:
        try:
            razao = jogadores[0]['iniciativa'] / jogadores[1]['iniciativa']
        except ZeroDivisionError:
            razao = jogadores[0]['iniciativa']

        if razao < 2:
            jogadores[0]['qtd_acoes'] = 2
        elif razao >= 2 and razao < 4:
            jogadores[0]['qtd_acoes'] = 3
        else:
            jogadores[0]['qtd_acoes'] = 4

    n_acao = 1
    status_de_jogo = 'inicio'
    for i in range(2):
        if status_de_jogo != 'fim de jogo':
            registra_jogada(n_turno, n_acao, jogadores)
            cria_jogada(jogadores[0], jogadores[0]['modelo'])
            cria_jogada(jogadores[1], jogadores[1]['modelo'])
            # registra_jogada(n_turno, n_acao, jogadores)
            status_de_jogo = resolve_jogada(jogadores)
            n_acao += 1

    # demais acoes
    if jogadores[0]['qtd_acoes'] > 2 and status_de_jogo != 'fim de jogo':
        # print(jogadores[0]['nome'], 'tem uma ação a mais!')
        for i in range(jogadores[0]['qtd_acoes'] - 2):
            registra_jogada(n_turno, n_acao, jogadores)
            cria_jogada(jogadores[0], jogadores[0]['modelo'])
            jogadores[1]['in'].pop()
            # registra_jogada(n_turno, n_acao, jogadores)
            if jogadores[0]['acao'][0] == 0:
                acao_movimento(jogadores[0])
                # print(jogadores[0]['nome'], 'assume posicao de vantagem.\n')
            elif jogadores[0]['acao'][0] == 1:
                dano = acao_ataque(jogadores[0], jogadores[1])
                if jogadores[1]['saude'] <= 0:
                    # print(jogadores[1]['nome'], 'recebe',
                          # dano, 'de dano e morre.\n')
                    status_de_jogo = 'fim de jogo'
                else:
                    pass
                    # print(jogadores[1]['nome'], 'recebe',
                          # dano, 'de dano.\n')
            else:
                pass
                # print(jogadores[0]['nome'], 'defende, ninguém se feriu.\n')
            n_acao += 1

    for jogador in jogadores:
        jogador['iniciativa'] += 2

    return status_de_jogo


if __name__ == '__main__':

    registro_in, registro_out = [], []
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '99'
    tf.logging.set_verbosity(tf.logging.ERROR)
    # modelinho = load_model('model_checkpoint_30_batch_9_epochs.h5')
    modelinho = load_model('carlos.h5')
    # modelo_carlos = load_model('model_checkpoint_30_batch_9_epochs.h5')

    vencedor = {'alberto': 0, 'carlos': 0}

    for i in tqdm(range(1)):
        # print('jogo', i + 1)
        VANTAGEM = (None, 0)
        jogadores = [cria_lutador('alberto'), cria_lutador('carlos')]
        jogadores[0]['modelo'] = modelinho
        jogadores[1]['modelo'] = None

        n_turno = 1

        # print('\nTurno', n_turno)
        status = turno(jogadores)
        while status != 'fim de jogo':
            n_turno += 1
            # print('\nTurno', n_turno)

            # Impede que a luta dure demais
            status = turno(jogadores)
            if n_turno >= 20:
                break

        # for jogador in jogadores:
        #     if jogador['saude'] > 0:
        #         print(jogador['nome'], 'vence!\n')
        # for jogador in jogadores:
        #     if jogador['saude'] > 0:
        #         vencedor[jogador['nome']] += 1

        # for item in vencedor:
        #     print(item, vencedor[item] / (i + 1))

        # Vencedor passa a ser quem tem mais saude
        if jogadores[0]['saude'] > jogadores[1]['saude']:
            vencedor = jogadores[0]
        else:
            vencedor = jogadores[1]

        for i in range(len(vencedor['in'])):
            registro_in.append(vencedor['in'][i])
            registro_out.append(vencedor['out'][i])

    with open('treino.in', mode='a') as f:
        for linha in registro_in:
            f.write(linha)
            f.write('\n')

    with open('treino.out', mode='a') as f:
        for linha in registro_out:
            f.write(linha)
            f.write('\n')
