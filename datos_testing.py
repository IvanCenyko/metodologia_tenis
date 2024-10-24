# este archivo se corre una única vez para generar los archivos .csv en "datos_testing/"

import pandas as pd
import os

# Especifica la ruta de la carpeta donde están los CSV
carpeta_csv = r'tennis_atp-master'

# Diccionario para almacenar todos los DataFrames
dataframes_archivos = {}

# Recorre todos los archivos de la carpeta
for archivo in os.listdir(carpeta_csv):
    if archivo.endswith('.csv'):
        # Crea la ruta completa del archivo
        archivo_path = os.path.join(carpeta_csv, archivo)
        # Lee el CSV y lo agrega a la lista de DataFrames
        df = pd.read_csv(archivo_path)
        dataframes_archivos[archivo.replace(".csv", '')] = df


# tomo columnas de algun dataframe (todos son iguales en formato)
columnas = list(dataframes_archivos["atp_matches_2023"])

# dataframe vacio con partidos nadal
partidos_nadal_ganados = pd.DataFrame(columns=columnas)
partidos_nadal_perdidos = pd.DataFrame(columns=columnas)

# dataframe vacio con partidos djokovic
partidos_djokovic_ganados = pd.DataFrame(columns=columnas)
partidos_djokovic_perdidos = pd.DataFrame(columns=columnas)




# rango de agnos a revisar
years = [2023, 2024]


# datos de Djokovic

# para cada agno
for year in years:

    # tomo el dataframe de ese agno
    frame = dataframes_archivos[f"atp_matches_{str(year)}"]

    # tomo partidos que gano djokovic contra cualquiera menos djokovic (eso se reserva para testing)
    winner = frame[(frame['winner_name'].str.contains("Novak Djokovic")) & ~frame["loser_name"].str.contains("Rafael Nadal")]
    # tomo partidos que perdio djokovic contra cualquiera menos nadal (eso se reserva para testing)
    loser = frame[(frame['loser_name'].str.contains("Novak Djokovic")) & ~frame["winner_name"].str.contains("Rafael Nadal")]


    # contateno en dataframe de todos los partidos, los que lei de este agno
    partidos_djokovic_ganados = pd.concat([partidos_djokovic_ganados, winner], ignore_index=True, sort=False)
    partidos_djokovic_perdidos = pd.concat([partidos_djokovic_perdidos, loser], ignore_index=True, sort=False)


# idem para Nadal

for year in years:

    frame = dataframes_archivos[f"atp_matches_{str(year)}"]

    winner = frame[(frame['winner_name'].str.contains("Rafael Nadal")) & ~frame["loser_name"].str.contains("Novak Djokovic")]
    loser = frame[(frame['loser_name'].str.contains("Rafael Nadal")) & ~frame["winner_name"].str.contains("Novak Djokovic")]


    partidos_nadal_ganados = pd.concat([partidos_nadal_ganados, winner], ignore_index=True, sort=False)
    partidos_nadal_perdidos = pd.concat([partidos_nadal_perdidos, loser], ignore_index=True, sort=False)



# exporto a csv
partidos_djokovic_ganados.to_csv("./datos_testing/djokovic_ganados_testing.csv", index=False)
partidos_djokovic_perdidos.to_csv("./datos_testing/djokovic_perdidos_testing.csv", index=False)

partidos_nadal_ganados.to_csv("./datos_testing/nadal_ganados_testing.csv", index=False)
partidos_nadal_perdidos.to_csv("./datos_testing/nadal_perdidos_testing.csv", index=False)
