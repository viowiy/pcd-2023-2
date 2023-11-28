state = [0, 0, 0, 0, 0, 0, 1, 0, 1] # Ni es necesario definir esta variable acá... solo para tener en cuenta lo que es...

def cell_char(x):
    if x == 1:
        return "x"
    if x == 2:
        return "o"
    return " "

def init_state():
    return [0, 0, 0, 0, 0, 0, 0, 0, 0]

def  is_final_state(s): # Como hacer esto en una sola línea???
    for i in range(len(s)):
        if s[i-1] == 0:
            return False
    return True

def print_state(s):
    c = [cell_char(x) for x in s]
    print("    A   B   C  ")
    print("  ┏━━━┯━━━┯━━━┓")
    print("1 ┃ {} │ {} │ {} ┃".format(c[0], c[1], c[2]))
    print("  ┠───┼───┼───┨")
    print("2 ┃ {} │ {} │ {} ┃".format(c[3], c[4], c[5]))
    print("  ┠───┼───┼───┨")
    print("3 ┃ {} │ {} │ {} ┃".format(c[6], c[7], c[8]))
    print("  ┗━━━┷━━━┷━━━┛")

def next_player(p):
    return 1 if p == 2 else 2

#is_final_state([0, 1, 1, 1, 1, 1, 1, 1, 1])

def ask_action(s):
    for _ in range(10):
        move = int(input("Haga su jugada: "))
        if s[move] == 0:
            return move
        print("Jugada inválida...")
    print("10 intentos y nada... Adios...")
    return -123

# Acá voy a programar la juagada del player PC.

def options(s):
    optiones = [i for i in range(len(s)) if s[i]== 0]
    return optiones

"""
Matriz de vecinos por líneas...
Ve valores:
Horizontal, Vertical, Diagonal1 y  Diagonal2 (en caso del 4).
Lo que traté de crear fue una guía para que el juego sepa que casillas jugadas por el player 1 le resultan más peligrosas...
En otra fase, se pudiera usar para analizar que casillas del player 2 se deben jugar para ganar...
"""
line_matrix={"0" : [[1,2] , [3,6], [4,8]],
             "1" : [[0,2] , [4,7]],
             "2" : [[0,1] , [5,8], [4,6]],
             "3" : [[4,5] , [0,6]],
             "4" : [[3,5] , [1,7], [0,8], [2,6]],
             "5" : [[3,4] , [2,8]],
             "6" : [[7,8] , [0,3], [2,4]],
             "7" : [[6,8] , [1,4]],
             "8" : [[6,7] , [2,5], [0,4]]}

def risk_calc(ops): # Calculará el tamaño del riesgo de no jugar en determinada casilla...
    risk_list = []
    for op in ops:
        # risk = 0
        memory_risk = 0
        for line in line_matrix[str(op)]:
            risk = 0
            for neigbor in line:
                risk += 1 if state[neigbor] == 1 else 0
                memory_risk = risk if risk > memory_risk else memory_risk
                # print("Opción: {}, Línea: {}, Vecino: {}, Caracter: {} Riesgo: {}, Memoria: {}".format(op, line, neigbor, cell_char(state[neigbor]), risk, memory_risk))
        risk_list.append(memory_risk)
    return risk_list


def actual_winner(s):
    winner = 0
    for item in s:
        memory1 = 0
        memory2 = 0
        for line in line_matrix[str(item)]:
            score1 = 0
            score2 = 0
            for neigbor in line:
                score1 += 1 if s[neigbor] == 1 else 0
                score2 += 1 if s[neigbor] == 1 else 0
                memory1 = score1 if score1 > memory1 else memory1
                memory2 = score2 if score2 > memory2 else memory2
                # print("Opción: {}, Línea: {}, Vecino: {}, Caracter: {} Riesgo: {}, Memoria: {}".format(op, line, neigbor, cell_char(state[neigbor]), risk, memory_risk))
                # Correr esta línea PRINT luego para comprender por qué está seleccionando mal la opción a jugar...
        #risk_list.append(memory_risk)
        if memory1 == 3:
            for item in state:
                if item == 0:
                    item = 3
            return 1
        elif memory2 == 3:
            for item in state:
                if item == 0:
                    item = 3
            return 2
    return 0

def report_winner(s):
    print("El Ganador es: ", actual_winner(s))


def choose_action(s):
    op_list = options(s)
    rsk_list = risk_calc(op_list)
    
    cumul_risk = 0
    big_risk_op = 0
    
    for ch_op in range(len(op_list)):
        if rsk_list[ch_op] >= cumul_risk:
            big_risk_op = op_list[ch_op]
            cumul_risk = rsk_list[ch_op]
    return big_risk_op # Arreglar este defecto luego... esto devuelve el mayor riesgo que se analizó de último...
    # Crear en vez de un solo valor una lista de todos los valores mayores y hacer un Ramdon Choice???
    # Esto agregaría algo de azar... pero basado en la prioridad... que por ahora es no perder...

def next_state(s, m, player):
    s[m] = player
    print_state(s)
    return s

#choose_action(state)
#state = [0, 1, 1, 1, 2, 2, 0, 2, 1]
#print("Opciones: ", options(state))
#print("Riesgos: ", risk_calc(options(state)))
#choose_action(state)

def tic_tac_toe():
    state = init_state()
    print("EL GATO™")
    player = 1
    while not is_final_state(state):
        print_state(state)
        m = ask_action(state) if player == 1 else choose_action(state)
        s = next_state(state, m, player)
        # actual_winner(state) # Acá trabajar después... ya que report_winner solo dará el ganador cuando haya final state...
        player = next_player(player)
    report_winner(state)

tic_tac_toe()