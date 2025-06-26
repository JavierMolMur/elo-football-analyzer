VENTAJA_LOCAL = 50  
VENTAJA_LOCAL_PENALIZADA = 25
FACTOR_EMPATE = 0.27 


# Función para calcular la expectativa de victoria
# returns (P_A, P_B, probabilidad_empate)
def calcular_expectativa(elo_local, elo_visitante):
    diferencia_elo = abs(elo_local - elo_visitante)
    if diferencia_elo > 200:
        R_A = elo_local + VENTAJA_LOCAL_PENALIZADA
    else:
        R_A = elo_local + VENTAJA_LOCAL

    R_B = elo_visitante

    # Expectativas de victoria
    E_A = 1 / (1 + 10 ** ((R_B - R_A) / 400))
    E_B = 1 - E_A  

    probabilidad_empate = FACTOR_EMPATE * (1 - abs(E_A - E_B))

    # Ajustar para que sumen 1
    P_A = (1 - probabilidad_empate) * E_A
    P_B = (1 - probabilidad_empate) * E_B

    return P_A, P_B, probabilidad_empate

# Función para calcular el multiplicador de expectativas
# reutrns el multiplicador de expectativas
def multiplicador_expectativas(resultado, p_win, p_draw):

    e = p_win + 0.5 * p_draw
    delta = resultado - e
    escala = 2 + 2 * abs(0.5 - p_win)
    return delta * escala

# Función para calcular si la racha es anómala
def es_racha_anomala(prob_victoria, longitud_racha, umbral=0.02):
    return prob_victoria ** longitud_racha < umbral
