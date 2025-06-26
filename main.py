# main.py
import obtener_partidos as script1
import calcular_elo_grafico as script2
import calcular_resultados as script3

def main():

    print("Ejecutando script 1")
    script1.run()
    print("Ejecutando script 2")
    script2.run()
    print("Ejecutando script 3")
    script3.run()

if __name__ == "__main__":
    main()
