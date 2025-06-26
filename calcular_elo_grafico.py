import math
import obtener_partidos as data
import calcular_probabilidades
from datetime import datetime
import json
import matplotlib.pyplot as plt  # 📊 Para generar el gráfico

ELO_INICIAL = {
    "Real Madrid CF": 1400,
    "FC Barcelona": 1400,
    "Club Atlético de Madrid": 1400,
    "Girona FC": 1400,
    "Athletic Club": 1400,
    "Real Sociedad de Fútbol": 1400,
    "Villarreal CF": 1400,
    "Real Betis Balompié": 1400,
    "Sevilla FC": 1400,
    "Valencia CF": 1400,
    "RC Celta de Vigo": 1400,
    "RCD Mallorca": 1400,
    "CA Osasuna": 1400,
    "Getafe CF": 1400,
    "Rayo Vallecano de Madrid": 1400,
    "UD Las Palmas": 1400,
    "Deportivo Alavés": 1400,
    "RCD Espanyol de Barcelona": 1400,
    "Real Valladolid CF": 1400,
    "CD Leganés": 1400,
}

K_BASE = 30  
VENTAJA_LOCAL = 50  
VENTAJA_LOCAL_PENALIZADA = 30
FECHA_INICIO_LIGA = datetime(2024, 8, 15)  # Fecha de inicio de la liga

def calcular_elo():
    datos = data.cargar_datos()
    elo = ELO_INICIAL.copy()
    rachas = {equipo: {"tipo": None, "contador": 0} for equipo in elo}
    historial_elo = {equipo: [elo[equipo]] for equipo in elo}  # 📈 Inicializar historial

    for jornada, partido in datos["partidos"].items():
        equipo_local = partido["local"]
        equipo_visitante = partido["visitante"]
        goles_local = partido["goles_local"]
        goles_visitante = partido["goles_visitante"]
        fecha_partido = datetime.strptime(partido["fecha"], "%Y-%m-%d")

        dias_transcurridos = (fecha_partido - FECHA_INICIO_LIGA).days
        peso_jornada = 1 + 1.0 * (1 - math.exp(-0.01 * dias_transcurridos)) 

        for equipo in [equipo_local, equipo_visitante]:
            if equipo not in elo:
                elo[equipo] = 1500
                rachas[equipo] = {"tipo": None, "contador": 0}
                historial_elo[equipo] = [elo[equipo]]

        E_A, E_B, E_D = calcular_probabilidades.calcular_expectativa(elo[equipo_local], elo[equipo_visitante])

        if goles_local > goles_visitante:
            S_A, S_B = 1, 0  
            tipo_partido = "victoria"
        elif goles_local < goles_visitante:
            S_A, S_B = 0, 1  
            tipo_partido = "derrota"
        else:
            S_A, S_B = 0.5, 0.5  
            tipo_partido = "empate"

        for equipo, S, E in [(equipo_local, S_A, E_A), (equipo_visitante, S_B, E_B)]:
            if rachas[equipo]["tipo"] == tipo_partido:
                rachas[equipo]["contador"] += 1
            else:
                rachas[equipo]["contador"] = 1
            rachas[equipo]["tipo"] = tipo_partido

            if tipo_partido != "empate":    
                if rachas[equipo]["tipo"] == tipo_partido:
                    rachas[equipo]["contador"] += 1
                else:
                    rachas[equipo]["contador"] = 1
            else:
                rachas[equipo]["contador"] = 0
            rachas[equipo]["tipo"] = tipo_partido

            multiplicador_racha = 1 + 1.0 * (1 - math.exp(-0.5 * rachas[equipo]["contador"]))
            diferencia_goles = abs(goles_local - goles_visitante)
            factor_diferencia_goles = max(2 * diferencia_goles, 10)

            elo[equipo] += (K_BASE * factor_diferencia_goles) * (S - E)


        # 📊 Guardar Elo tras el partido
        for equipo in historial_elo:
            historial_elo[equipo].append(elo.get(equipo, historial_elo[equipo][-1]))

    return elo, rachas, historial_elo

def guardar_resultados(elo_actualizado, rachas):
    with open("elo_actualizado.txt", "w") as file:
        file.write("Elo actual de los equipos:\n")
        for equipo, rating in sorted(elo_actualizado.items(), key=lambda x: x[1], reverse=True):
            file.write(f"{equipo}: {round(rating, 2)}\n")
    with open("elo_actualizado.json", "w") as json_file:
        json.dump(elo_actualizado, json_file, indent=4)

    with open("rachas_equipos.json", "w") as rachas_file:
        json.dump(rachas, rachas_file, indent=4)

def graficar_historial_elo(historial_elo):
    plt.figure(figsize=(14, 8))
    for equipo, elos in historial_elo.items():
        if len(elos) > 1:  # Evitar equipos sin partidos
            plt.plot(elos, label=equipo)
    plt.xlabel("Jornadas")
    plt.ylabel("Elo")
    plt.title("Evolución del Elo por jornada")
    plt.legend(loc="upper left", fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("evolucion_elo.png")  # 💾 Guardar gráfico como imagen
    plt.show()

# ⚽ Calcular y mostrar el Elo de los equipos
def run():
    elo_actualizado, rachas, historial_elo = calcular_elo()
    guardar_resultados(elo_actualizado, rachas)
    graficar_historial_elo(historial_elo)
    print("Los resultados se han guardado en 'elo_actualizado.txt', 'rachas_equipos.json' y el gráfico en 'evolucion_elo.png'")
