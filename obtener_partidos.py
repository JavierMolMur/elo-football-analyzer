import requests
import json

# ejemplo.py
from config import API_KEY

ARCHIVO_JSON = "partidos.json"
LIGA_ID = "PD"  # LaLiga (España)

def cargar_datos():
    """Carga el JSON de partidos o lo crea si no existe."""
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"partidos": {}}

def guardar_datos(datos):
    """Guarda los partidos en un JSON."""
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def obtener_partidos_liga(competicion_id):
    """Descarga los últimos partidos de una liga entera para evitar peticiones por equipo."""
    url = f"https://api.football-data.org/v4/competitions/{competicion_id}/matches"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return []

    partidos = response.json().get("matches", [])
    return [p for p in partidos if p["status"] == "FINISHED"]  # Filtrar solo los finalizados

def actualizar_partidos_liga(competicion_id):
    """Añade partidos de una liga entera sin duplicar."""
    datos = cargar_datos()
    partidos_nuevos = obtener_partidos_liga(competicion_id)

    for partido in partidos_nuevos:
        fecha = partido["utcDate"].split("T")[0]
        equipo_local = partido["homeTeam"]["name"]
        equipo_visitante = partido["awayTeam"]["name"]
        goles_local = partido["score"]["fullTime"]["home"]
        goles_visitante = partido["score"]["fullTime"]["away"]

        id_partido = f"{fecha}_{equipo_local}_{equipo_visitante}"

        if id_partido not in datos["partidos"]:
            datos["partidos"][id_partido] = {
                "fecha": fecha,
                "local": equipo_local,
                "visitante": equipo_visitante,
                "goles_local": goles_local,
                "goles_visitante": goles_visitante
            }
            print(f"Añadido: {id_partido}")
    
    guardar_datos(datos)

# ⚽ Actualizar partidos de LaLiga sin hacer muchas requests
def run():    
    actualizar_partidos_liga(LIGA_ID)
