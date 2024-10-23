import pandas as pd
import os

# Especifica la ruta de la carpeta donde están los CSV
carpeta_csv = r'tennis_atp-master'

# Diccionario para almacenar todos los DataFrames
dataframes = {}

# Recorre todos los archivos de la carpeta
for archivo in os.listdir(carpeta_csv):
    if archivo.endswith('.csv'):
        # Crea la ruta completa del archivo
        archivo_path = os.path.join(carpeta_csv, archivo)
        # Lee el CSV y lo agrega a la lista de DataFrames
        df = pd.read_csv(archivo_path)
        dataframes[archivo.replace(".csv", '')] = df



yearly_matches_djokovic = {}

years = range(2004, 2023)

num_partidos_djokovic = 0


for year in years:

    frame = dataframes[f"atp_matches_{str(year)}"]
    winner = frame[(frame['winner_name'].str.contains("Novak Djokovic"))]
    loser = frame[(frame['loser_name'].str.contains("Novak Djokovic"))]


    total = pd.concat([winner, loser], ignore_index=True, sort=False)

    yearly_matches_djokovic[str(year)] = total

    num_partidos_djokovic += len(total.index)




yearly_matches_nadal = {}

years = range(2004, 2023)

num_partidos_nadal = 0


for year in years:

    frame = dataframes[f"atp_matches_{str(year)}"]
    winner = frame[(frame['winner_name'].str.contains("Rafael Nadal"))]
    loser = frame[(frame['loser_name'].str.contains("Rafael Nadal"))]


    total = pd.concat([winner, loser], ignore_index=True, sort=False)

    yearly_matches_nadal[str(year)] = total

    num_partidos_nadal += len(total.index)

print(num_partidos_nadal)