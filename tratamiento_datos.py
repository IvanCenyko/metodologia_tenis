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
columnas = list(dataframes_archivos["atp_matches_2004"])

# dataframe vacio con partidos nadal
partidos_nadal = pd.DataFrame(columns=columnas)
# dataframe vacio con partidos djokovic
partidos_djokovic = pd.DataFrame(columns=columnas)


# rango de agnos a revisar
years = range(2004, 2023)

# datos de Djokovic

# para cada agno
for year in years:

    # tomo el dataframe de ese agno
    frame = dataframes_archivos[f"atp_matches_{str(year)}"]
    # tomo partidos que gano
    winner = frame[(frame['winner_name'].str.contains("Novak Djokovic"))]
    # tomo partidos que perdio
    loser = frame[(frame['loser_name'].str.contains("Novak Djokovic"))]

    # concateno ambos
    total = pd.concat([winner, loser], ignore_index=True, sort=False)

    # contateno en dataframe de todos los partidos, los que lei de este agno
    partidos_djokovic = pd.concat([total, partidos_djokovic], ignore_index=True, sort=False)


# idem para Nadal

years = range(2004, 2023)


for year in years:

    frame = dataframes_archivos[f"atp_matches_{str(year)}"]
    winner = frame[(frame['winner_name'].str.contains("Rafael Nadal"))]
    loser = frame[(frame['loser_name'].str.contains("Rafael Nadal"))]


    total = pd.concat([winner, loser], ignore_index=True, sort=False)


    partidos_nadal = pd.concat([total, partidos_nadal], ignore_index=True, sort=False)



partidos_djokovic.to_csv("./datos_training/djokovic_training.csv", index=False)
partidos_nadal.to_csv("./datos_training/nadal_training.csv", index=False)