# este archivo se corre una única vez para generar los archivos .csv en "datos_training/"

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




def dataframe_generator(years:range,dataframes:dict, tenista1:str, tenista2:str, ):

    # tomo columnas de algun dataframe (todos son iguales en formato)
    columnas = list(dataframes[f"atp_matches_{years[-2]}"])

    # dataframe vacio con partidos tenista2
    partidos_tenista2_ganados = pd.DataFrame(columns=columnas)
    partidos_tenista2_perdidos = pd.DataFrame(columns=columnas)

    # dataframe vacio con partidos tenista1
    partidos_tenista1_ganados = pd.DataFrame(columns=columnas)
    partidos_tenista1_perdidos = pd.DataFrame(columns=columnas)

    tenista1_vs_tenista2 = pd.DataFrame(columns=columnas)


    # datos de tenista1

    # para cada agno
    for year in years:

        # tomo el dataframe de ese agno
        frame = dataframes_archivos[f"atp_matches_{str(year)}"]

        # tomo partidos que gano tenista1 contra cualquiera menos tenista1 (eso se reserva para testing)
        winner = frame[(frame['winner_name'].str.contains(tenista1)) & ~frame["loser_name"].str.contains(tenista2)]
        # tomo partidos que perdio tenista1 contra cualquiera menos tenista2 (eso se reserva para testing)
        loser = frame[(frame['loser_name'].str.contains(tenista1)) & ~frame["winner_name"].str.contains(tenista2)]


        # contateno en dataframe de todos los partidos, los que lei de este agno
        partidos_tenista1_ganados = pd.concat([partidos_tenista1_ganados, winner], ignore_index=True, sort=False)
        partidos_tenista1_perdidos = pd.concat([partidos_tenista1_perdidos, loser], ignore_index=True, sort=False)


    # idem para tenista2

    for year in years:

        frame = dataframes_archivos[f"atp_matches_{str(year)}"]

        winner = frame[(frame['winner_name'].str.contains(tenista2)) & ~frame["loser_name"].str.contains(tenista1)]
        loser = frame[(frame['loser_name'].str.contains(tenista2)) & ~frame["winner_name"].str.contains(tenista1)]

        # busco partidos que hayan jugado entre si
        tenista1_vs_tenista2_this_year = frame[
            ((frame['winner_name'].str.contains(tenista1)) & (frame["loser_name"].str.contains(tenista2))) |
            ((frame['winner_name'].str.contains(tenista2)) & (frame["loser_name"].str.contains(tenista1)))
        ]
        # los guardo separados
        tenista1_vs_tenista2 = pd.concat([tenista1_vs_tenista2, tenista1_vs_tenista2_this_year], ignore_index=True, sort=False)

        partidos_tenista2_ganados = pd.concat([partidos_tenista2_ganados, winner], ignore_index=True, sort=False)
        partidos_tenista2_perdidos = pd.concat([partidos_tenista2_perdidos, loser], ignore_index=True, sort=False)

    # HASTA ACA TENGO 5 DATAFRAMES:
    # PARTIDOS GANADOS Y PERDIDOS DE tenista1
    # PARTIDOS GANADOS Y PERDIDOS DE tenista2
    # PARTIDOS ENTRE tenista1 Y tenista2

    # obtengo sample para testing
    tenista1_testing_ganados = partidos_tenista1_ganados.sample(frac=0.2, random_state=42)
    tenista1_testing_perdidos = partidos_tenista1_perdidos.sample(frac=0.2, random_state=42)

    tenista2_testing_ganados = partidos_tenista2_ganados.sample(frac=0.2, random_state=42)
    tenista2_testing_perdidos = partidos_tenista2_perdidos.sample(frac=0.2, random_state=42)


    # armo training quitando los de testing
    tenista1_training_ganados = partidos_tenista1_ganados.drop(tenista1_testing_ganados.index)
    tenista1_training_perdidos = partidos_tenista1_perdidos.drop(tenista1_testing_perdidos.index)

    tenista2_training_ganados = partidos_tenista2_ganados.drop(tenista2_testing_ganados.index)
    tenista2_training_perdidos = partidos_tenista2_perdidos.drop(tenista2_testing_perdidos.index)

    return {"tenista1_training_ganados": tenista1_training_ganados, "tenista1_training_perdidos": tenista1_training_perdidos,
            "tenista2_training_ganados": tenista2_training_ganados, "tenista2_training_perdidos": tenista2_training_perdidos, 
            "tenista1_testing_ganados": tenista1_testing_ganados, "tenista1_testing_perdidos": tenista1_testing_perdidos,
            "tenista2_testing_ganados": tenista2_testing_ganados, "tenista2_testing_perdidos": tenista2_testing_perdidos,
            "tenista1_vs_tenista2": tenista1_vs_tenista2}


df = dataframe_generator(range(2004, 2025), dataframes_archivos, tenista1='Novak Djokovic', tenista2='Rafael Nadal')


# exporto a csv
df["tenista1_training_ganados"].to_csv("./datos_training/djokovic_training_ganados.csv", index=False)
df["tenista1_training_perdidos"].to_csv("./datos_training/djokovic_training_perdidos.csv", index=False)

df["tenista2_training_ganados"].to_csv("./datos_training/nadal_training_ganados.csv", index=False)
df["tenista2_training_perdidos"].to_csv("./datos_training/nadal_training_perdidos.csv", index=False)

df["tenista1_testing_ganados"].to_csv("./datos_testing/djokovic_testing_ganados.csv", index=False)
df["tenista1_testing_perdidos"].to_csv("./datos_testing/djokovic_testing_perdidos.csv", index=False)

df["tenista2_testing_ganados"].to_csv("./datos_testing/nadal_testing_ganados.csv", index=False)
df["tenista2_testing_perdidos"].to_csv("./datos_testing/nadal_testing_perdidos.csv", index=False)

df["tenista1_vs_tenista2"].to_csv("./datos_testing/djokovic_vs_nadal.csv", index=False)

