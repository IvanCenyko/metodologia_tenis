import pandas as pd
import os

# Especifica la ruta de la carpeta donde están los CSV
carpeta_csv = r'tennis_atp-master'

# Lista para almacenar todos los DataFrames
dataframes = {}

# Recorre todos los archivos de la carpeta
for archivo in os.listdir(carpeta_csv):
    if archivo.endswith('.csv'):
        # Crea la ruta completa del archivo
        archivo_path = os.path.join(carpeta_csv, archivo)
        # Lee el CSV y lo agrega a la lista de DataFrames
        df = pd.read_csv(archivo_path)
        dataframes[archivo.replace(".csv", '')] = df



'''
frame = dataframes["atp_matches_2004"]
frame["winner_name"].str.contains("Novak Djokovic")
'''