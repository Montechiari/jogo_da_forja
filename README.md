## jogo_da_forja

# descrição do jogo

Jogo de duelo de espadas baseado em texto. Cada combatente possui uma quantidade de pontos de *saúde* e pontos de *prontidão*. Aquele que tiver os pontos de saúde levados a zero perde o jogo. O combatente que tiver maior número de pontos de prontidão tem *iniciativa*, ou seja, sua ação é levada a cabo primeiro. Os confrontos são feitos em turnos de uma ação por combatente. Caso a prontidão de um combatente seja o dobro da de seu oponente, ele recebe uma ação extra no turno. Cada embate dura no máximo 20 turnos. Existem seis ações possíveis:
- O primeiro par de ações é o dos *movimentos* ofensivo e defensivo. As ações de movimento garantem vantagens nos turnos seguintes. A vantagem defensiva proporciona um incremento nos pontos de prontidão e reduzem o dano recebido. A vantagem ofensiva dobra o dano infligido pelo combatente e não custa pontos de prontidão. Apenas um combatente pode ter a vantagem de movimento ativa, ela se perde assim que seu oponente fizer uma ação de movimento.
- Existem dois tipos de ações de ataque: corte e estocada. O dano produzido por cada tipo de ataque é determinado pelas características da arma do combatente, existindo armas que favorecem o corte e armas que favorecem a estocada, em diferentes proporções. A coincidência de ataque entre os dois combatentes é tratada diferentemente, dependendo da ação. Dois ataques de corte fazem as armas se chocarem, e não há dano a nenhum dos combatentes. Caso haja dois ataques de estocada, os dois combatentes sofrem dano por ordem definida pela iniciativa.
- Para cada tipo de ataque, corte ou estocada, existe uma ação de defesa. Se um combatente escolhe um tipo de defesa distinto do ataque de seu oponente, o ataque causa a metade do dano. Se um combatente escolhe o mesmo tipo de defesa que o ataque de seu adversário, o dano é evitado e o defensor ganha um ponto de prontidão.
Com exceção das ações de movimento e da defesa bem-sucedida, toda ação custa um ponto de prontidão. Ao final do turno, um ponto de prontidão é retornado a cada combatente.
Ao início da partida, são gerados aleatoriamente os dois combatentes, que variam na proporção de pontos de saúde e prontidão. As armas de cada um também são geradas, com características aleatórias de dano. Em nome da isonomia, o total de dano das armas é sempre o mesmo. A soma entre pontos de vida e prontidão também é sempre a mesma.

# sobre implementação do combate

Todas as combinações de ações resultam em alterações em *vantagem*, *saude* ou *prontidão*. Uma variável importante é qual jogador tem iniciativa. Pode ser feita uma só função, opera com variações fornecidas por um dicionário de jogadas. A função dividiria a resolução da jogada com ordem baseada na iniciativa, e a resolução da jogada seria uma função à parte. Preliminarmente, haverá uma função para definição da iniciativa.

# dados para treino de rede neural

- razão entre atributos de arma (corte / estocada) ------------+
- razão entre arma do combatente e do adversário (corte)       |
- razão entre arma do combatente e do adversário (estocada)    | Dados permanentes
- razão entre saude e prontidao do combatente                  |
- razão entre saude do combatente e do adversário              |
- razão entre prontidão do combatente e do adversário ---------+
- número de turno ---------------------------------------------+
- porcentagem atual de saúde                                   |
- porcentagem atual de prontidão                               | Estado atual
- porcentagem saúde adversário                                 |
- porcentagem prontidão adversário                             |
- combatente tem vantagem? (binário)                           |
- qual vantagem? (binário) ------------------------------------+
- quantidade de acoes bonus-------------------------------+ Histórico
- numero de acoes bonus
- última ação
- última ação do adversário                                    |

# sobre o projeto

A primeira etapa é implementar o jogo para browser. No final de cada jogo, dados sobre a partida serão enviados a um servidor, para treino da inteligência artificial. Isso deve estar explícito para os jogadores. Todos os jogadores enfrentarão a mesais vitórias contra a máquina.

A segunda etapa é introduzir traços de RPG ao jogo, com evolução de personagem e relações mais complexas durante o combate. Um exemplo é fazer o sucesso de um ataque ser suscetível à aleatoriedade. Existiria um trade-off, uma estocada teria menos probabilidades de acerto que um corte, mas causaria mais dano.

A terceira etapa é criar uma oficina de armas, e fazer da construção de armas um carro-chefe. Existe a possibilidade de implementar uma economia, com trocas entre jogadores.

# Apontamentos sobre a versão RPG

### Desenvolvimento de personagem

Um ponto importante do jogo básico é o combate em que a sorte se manifesta apenas na coincidência de ações entre oponentes, não está ligada a probabilidades de acerto dadas pelo nível deles. O nível dos combatentes deveria afetar o conhecimento sobre si e sobre o adversário.
Os combatentes têm três níveis de atributos: os permanentes, os de longo prazo, e os de curto prazo. Esses atributos têm ainda duas classes: físicos e psicológicos.
Seria uma boa idéia fazer os atributos terem sinergia com as características da arma que o combatente usa. Dessa forma, a construção da arma assume um papel importante no jogo.

### Treino

O treino será dividido em treino individual e coletivo. O atributo *introvertido/extrovertido* indicará qual desses treinos o combatente vai absorver melhor. No final da semana de treino existem duas chances de combate: sparring (contra colegas de equipe); e feira livre (combates amistosos). No inicio da semana seguinte, uma porcentagem do treino da semana se agrega à habilidade permanente do combatente. Um atributo chamado *plasticidade* define essa porcentagem, e depende de um conjunto de outros fatores como idade, disciplina, condicionamento e inteligência.
