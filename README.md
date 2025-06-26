# ⚽ Elo Football Analyzer

Herramienta de análisis y simulación de puntuaciones Elo para equipos de fútbol. Este proyecto permite calcular la evolución del ranking Elo a lo largo de una temporada utilizando resultados reales, e incluye un sistema de predicción para partidos futuros basado en estos datos.

## 🚀 Características

- Cálculo de Elo por jornada con múltiples factores:
  - Localía
  - Diferencia de goles
  - Rachas de victorias o derrotas
  - Peso temporal por jornada
- Predicción de resultados con cálculo de probabilidades (victoria, empate, derrota)
- Generación automática de gráficas de evolución del Elo por equipo
- Exportación a formatos `.json` y `.txt` de resultados y rankings
- Detección de rachas anómalas


## 🧠 Lógica de cálculo

- Se asigna un Elo inicial a cada equipo (personalizable).
- Cada partido modifica el Elo de ambos equipos en función del resultado real, su expectativa previa, y factores como racha y diferencia de goles.
- Se registra la evolución para generar un historial completo por jornada.

## 📊 Visualización

Puedes ejecutar `calcular_elo_grafico.py` para generar un gráfico estático con la evolución del Elo de los equipos por jornada. Esto te permite detectar tendencias o cambios bruscos en rendimiento.

## 📦 Requisitos

- Python 3.9+
- Bibliotecas:
  - `matplotlib`
  - `json`
  - `datetime`
  - `math`

Instalación de dependencias:

```bash
pip install matplotlib
