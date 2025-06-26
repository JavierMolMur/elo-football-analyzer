import requests
import math
import json
import calcular_probabilidades

from config import API_KEY
URL = "https://api.football-data.org/v4/competitions/PD/matches"
VENTAJA_LOCAL = 50  
FACTOR_EMPATE = 0.27  # Ajusta este valor según la cantidad histórica de empates
DECIMALES = 4
UMBRAL_RACHA_ANOMALA = 5

# Función para cargar el Elo de los equipos desde el archivo
def cargar_elo():
    elo = {}
    try:
        with open("elo_actualizado.json", "r") as file:
            elo = json.load(file)
            # Convertir los valores a float por si acaso están como strings
            elo = {equipo: float(valor) for equipo, valor in elo.items()}
    except FileNotFoundError:
        print("El archivo 'elo_actualizado.json' no se encuentra.")
        elo = {}

    return elo

# Función para obtener los datos de la API
def obtener_datos_api():
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener los partidos desde la API")
        return None

# Función para obtener las dos siguientes jornadas
def obtener_siguientes_jornadas(data):
    jornadas = sorted(set(partido["matchday"] for partido in data["matches"] if partido["status"] in ["SCHEDULED", "TIMED"]))
    return jornadas[:2] if len(jornadas) > 1 else (jornadas[:1] if jornadas else None)

# Función para obtener los partidos de las siguientes jornadas
def obtener_partidos_siguientes_jornadas(data, jornadas):
    partidos_jornadas = []
    if not jornadas:
        return []
    
    for jornada in jornadas:
        print(f"Jornada {jornada}:")
        partidos_jornada = []
        for partido in data["matches"]:
            if partido["matchday"] == jornada and partido["status"] in ["SCHEDULED", "TIMED"]:
                equipo_local = partido["homeTeam"]["name"]
                equipo_visitante = partido["awayTeam"]["name"]
                partidos_jornada.append({"local": equipo_local, "visitante": equipo_visitante})
        partidos_jornadas.append(partidos_jornada)
    return partidos_jornadas


def run():
    # Cargar Elo y obtener datos de la API
    elo_actualizado = cargar_elo()
    data_api = obtener_datos_api()

    if data_api:
        jornadas = obtener_siguientes_jornadas(data_api)
        partidos_jornadas = obtener_partidos_siguientes_jornadas(data_api, jornadas)

        try:
            with open("rachas_equipos.json", "r", encoding="utf-8") as rachas_file:
                rachas = json.load(rachas_file)
        except FileNotFoundError:
            rachas = {}

        if partidos_jornadas:
            with open("resultados.txt", "w", encoding="utf-8") as file:  # Abrir archivo para escritura
                for i, partidos_jornada in enumerate(partidos_jornadas):
                    jornada_header = f"\nProbabilidades para la jornada {jornadas[i]}:\n"
                    print(jornada_header)
                    file.write(jornada_header)  # Escribir en el archivo

                    for partido in partidos_jornada:
                        equipo_local = partido["local"]
                        equipo_visitante = partido["visitante"]

                        if equipo_local in elo_actualizado and equipo_visitante in elo_actualizado:
                            P_A, P_B, P_empate = calcular_probabilidades.calcular_expectativa(elo_actualizado[equipo_local], elo_actualizado[equipo_visitante])

                            resultado = (
                                f"{equipo_local} vs {equipo_visitante}:\n"
                                f"  Probabilidad de victoria {equipo_local}: {round(P_A,DECIMALES)}\n"
                                f"  Probabilidad de empate: {round(P_empate,DECIMALES)}\n"
                                f"  Probabilidad de victoria {equipo_visitante}: {round(P_B,DECIMALES)}\n"
                            )
                            print(resultado)
                            file.write(resultado)  # Escribir en el archivo

                            # Advertencias por rachas anómalas
                            for equipo in [equipo_local, equipo_visitante]:
                                if equipo in rachas:
                                    tipo = rachas[equipo]["tipo"]
                                    contador = rachas[equipo]["contador"]
                                    if tipo == "victoria" and contador >= UMBRAL_RACHA_ANOMALA:
                                        advertencia = (
                                            f"⚠️  Advertencia: El equipo '{equipo}' lleva una racha anómala de {contador} {tipo}s consecutivas.\n"
                                        )
                                        print(advertencia)
                                        file.write(advertencia)

                        else:
                            mensaje_error = f"Faltan datos de Elo para {equipo_local} o {equipo_visitante}\n"
                            print(mensaje_error)
                            file.write(mensaje_error)  # Escribir en el archivo
        else:
            mensaje_error = "No se pudieron obtener los partidos de las siguientes jornadas.\n"
            print(mensaje_error)
            with open("resultados.txt", "w", encoding="utf-8") as file:
                file.write(mensaje_error)