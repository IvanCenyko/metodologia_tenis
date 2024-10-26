import pandas as pd
import numpy as np
import math
# Definición de constantes de ponderación
POND_PORC_VICTORIAS = 17.5
POND_PORC_VICTORIAS_TIPO_SUELO = 17.5
POND_ACES = 9
POND_DOBLES_FALTAS = 11
POND_PORC_PRIMER_SERVICIO_IN = 5
POND_PORC_PTS_GANADOS_PRIMER_SAQUE = 11
POND_PORC_PTS_GANADOS_SEGUNDO_SAQUE = 11
POND_BREAK_POINTS_ENFRENTADOS = 6
POND_PORC_BREAK_POINTS_SALVADOS = 12


def promedio(df_win, df_lose, total, col:str):
    return (df_win["w_" + col].sum() + df_lose["l_" + col].sum()) / total

def acum_total(df_win, df_lose, param:str):
    return df_win["w_" + param].sum() + df_lose["l_" + param].sum()

def normalizacion_positiva(valor, min, max):
    norm = (valor-min)/(max-min) * 100
        
    if norm >= 100:
        return 100
    elif norm <= 0:
        return 0
    else:
        return norm

def normalizacion_negativa(valor, min, max):
    norm = (1 - (valor-min)/(max-min)) * 100

    if norm >= 100:
        return 100
    elif norm <= 0:
        return 0
    else:
        return norm

def ponderar(valor, pond):
    return valor * pond / 100


def calc_puntaje(ganados_testing, perdidos_testing):
    ########## PORCENTAJE DE VICTORIAS ##########

    # Victorias, derrotas y partidos totales de Nadal en testing
    victorias_totales = len(ganados_testing)
    derrotas_totales = len(perdidos_testing)
    partidos_totales = derrotas_totales + victorias_totales

    ## VALOR A NORMALIZAR:
    # Porcentaje de victorias, no necesita normalizacion
    porc_victorias = (victorias_totales/partidos_totales) * 100


    ########## PROMEDIO ACES POR PARTIDO ##########

    ## VALOR A NORMALIZAR:
    # Promedio Aces por partido
    aces_por_partido = promedio(ganados_testing, perdidos_testing, partidos_totales, "ace")


    ########## PROMEDIO DOBLE FALTAS POR PARTIDO ##########

    ## VALOR A NORMALIZAR:
    # Promedio dobles faltas por partido
    dobles_faltas_por_partido =  promedio(ganados_testing, perdidos_testing, partidos_totales, "df")


    ########## PORCENTAJE DE 1ER SERVICIO ADENTRO, DE TODOS LOS SERVICIOS JUGADOS ##########

    # todos los servicios de Nadal sin contar doble falta
    total_servicios_sin_df = perdidos_testing["l_svpt"].sum() - perdidos_testing["l_df"].sum() + ganados_testing["w_svpt"].sum() - ganados_testing["w_df"].sum()# Porcentaje de primeros servicios adentro
    # todos los servicios de Nadal contando doble falta
    total_servicios_con_df = perdidos_testing["l_svpt"].sum() + ganados_testing["w_svpt"].sum()

    # Total de primeros servicios adentro
    total_primer_servicio_in = acum_total(ganados_testing, perdidos_testing, "1stIn")

    ## VALOR A NORMALIZAR:
    # porcentaje de primer servicio adentro de todos los servicios jugados
    porc_primer_servicio_in = total_primer_servicio_in / total_servicios_sin_df * 100

    ########## PORCENTAJE DE PTS GANADOS CON 1ER Y 2DO SAQUE RESPECTO A LOS JUGADOS DE ESE TIPO ##########

    # Total de pts ganados por nadal de primer saque
    pts_ganados_primer_saque = acum_total(ganados_testing, perdidos_testing, "1stWon")
    # idem pero 2do saque
    pts_ganados_segundo_saque = acum_total(ganados_testing, perdidos_testing, "2ndWon")

    ## VALORES A NORMALIZAR:
    # porcentaje de pts ganados de primer saque, de todos los bien convertidos
    porc_pts_ganados_primer_saque = pts_ganados_primer_saque / total_primer_servicio_in * 100
    # porcentaje de pts ganados de 2do saque, de todos los bien convertidos
    porc_pts_ganados_segundo_saque = pts_ganados_segundo_saque / (total_servicios_sin_df - total_primer_servicio_in) *100

    ########## PROMEDIO BREAK POINTS SALVADOS POR PARTIDO ##########

    ## VALOR A NORMALIZAR:
    # promedio de break points 
    prom_break_por_partido = promedio(ganados_testing, perdidos_testing, partidos_totales, "bpFaced")

    ########## PORCENTAJE DE BREAK POINTS SALVADOS RESPECTO A LOS JUGADOS ##########

    break_jugados = acum_total(ganados_testing, perdidos_testing, "bpFaced")
    break_salvados = acum_total(ganados_testing, perdidos_testing, "bpSaved")

    ## VALOR A NORMALIZAR:
    porc_break_salvados = break_salvados / break_jugados * 100

    ########## PORC VICTORIAS SEGUN SUELO RESPECTO A PARTIDOS JUGADOS EN ESE SUELO ##########

    # Total de partidos ganados en cada superficie
    partidos_ganados_clay = len(ganados_testing[ganados_testing["surface"].str.contains("Clay")])
    partidos_ganados_grass = len(ganados_testing[ganados_testing["surface"].str.contains("Grass")])
    partidos_ganados_hard = len(ganados_testing[ganados_testing["surface"].str.contains("Hard")])

    # total de partidos jugados en cada superficie
    partidos_totales_clay = partidos_ganados_clay + len(perdidos_testing[perdidos_testing["surface"].str.contains("Clay")])
    partidos_totales_grass = partidos_ganados_grass + len(perdidos_testing[perdidos_testing["surface"].str.contains("Grass")])
    partidos_totales_hard = partidos_ganados_hard + len(perdidos_testing[perdidos_testing["surface"].str.contains("Hard")])

    ## VALORES A NORMALIZAR:
    # porcentaje de victorias en cada superficie
    porc_victorias_clay = partidos_ganados_clay / partidos_totales_clay * 100
    porc_victorias_grass = partidos_ganados_grass / partidos_totales_grass * 100
    porc_victorias_hard = partidos_ganados_hard / partidos_totales_hard * 100


    ########## NORMALIZACIONES Y PONDERACIONES ##########

    # Definición de constantes de ponderación
    global POND_PORC_VICTORIAS
    global POND_PORC_VICTORIAS_TIPO_SUELO
    global POND_ACES
    global POND_DOBLES_FALTAS
    global POND_PORC_PRIMER_SERVICIO_IN
    global POND_PORC_PTS_GANADOS_PRIMER_SAQUE
    global POND_PORC_PTS_GANADOS_SEGUNDO_SAQUE
    global POND_BREAK_POINTS_ENFRENTADOS
    global POND_PORC_BREAK_POINTS_SALVADOS

    porc_victorias_normalizado = ponderar(normalizacion_positiva(porc_victorias, 0, 100), POND_PORC_VICTORIAS)

    porc_victorias_tipo_de_suelo_normalizado = ponderar(
        ponderar(porc_victorias_clay, 60) + ponderar(porc_victorias_grass, 30) + ponderar(porc_victorias_hard, 10),
        POND_PORC_VICTORIAS_TIPO_SUELO
    )

    # Aces
    aces_normalizado = ponderar(normalizacion_positiva(aces_por_partido, 0, 12), POND_ACES)

    # dobles faltas
    dobles_faltas_por_partido_normalizado = ponderar(normalizacion_negativa(dobles_faltas_por_partido, 2, 8), POND_DOBLES_FALTAS)

    # porc primeros servicios adentro
    porc_primer_servicio_in_normalizado = ponderar(normalizacion_positiva(porc_primer_servicio_in, 40, 65), POND_PORC_PRIMER_SERVICIO_IN)

    # prom puntos ganados 1er saque
    porc_pts_ganados_primer_saque_normalizado = ponderar(normalizacion_positiva(porc_pts_ganados_primer_saque, 45, 65), POND_PORC_PTS_GANADOS_PRIMER_SAQUE)

    # prom puntos ganados 2do saque
    porc_pts_ganados_segundo_saque_normalizado = ponderar(normalizacion_positiva(porc_pts_ganados_segundo_saque, 45, 65), POND_PORC_PTS_GANADOS_SEGUNDO_SAQUE)

    # break points enfrentados
    break_points_enfrentados_normalizado = ponderar(normalizacion_negativa(prom_break_por_partido, 0, 8), POND_BREAK_POINTS_ENFRENTADOS)

    # break points salvados
    porc_break_points_salvados_normalizado = ponderar(normalizacion_positiva(porc_break_salvados, 0, 100), POND_PORC_BREAK_POINTS_SALVADOS)

    aces_lista = pd.concat([perdidos_testing["l_ace"], ganados_testing["w_ace"]])
    dobles_faltas_lista = pd.concat([perdidos_testing["l_df"], ganados_testing["w_df"]])
    primer_servicio_in_lista = pd.concat([perdidos_testing["l_1stIn"], ganados_testing["w_1stIn"]])
    porc_pts_ganados_primer_saque_lista = pd.concat([perdidos_testing["l_1stWon"], ganados_testing["w_1stWon"]])
    prom_break_por_partido_lista = pd.concat([perdidos_testing["l_bpFaced"], ganados_testing["w_bpFaced"]])
    prom_break_salvados_lista = pd.concat([perdidos_testing["l_bpSaved"], ganados_testing["w_bpSaved"]])

    # Calcular varianza y desviación estándar
    varianza_desviacion = {
        "jugador": ganados_testing.loc[0, "winner_name"],
        "aces_varianza": aces_lista.var(),
        "aces_desviacion": aces_lista.std(),
        "dobles_faltas_varianza": dobles_faltas_lista.var(),
        "dobles_faltas_desviacion": dobles_faltas_lista.std(),
        "primer_servicio_in_varianza": primer_servicio_in_lista.var(),
        "primer_servicio_in_desviacion": primer_servicio_in_lista.std(),
        "porc_pts_ganados_primer_saque_varianza": porc_pts_ganados_primer_saque_lista.var(),
        "porc_pts_ganados_primer_saque_desviacion": porc_pts_ganados_primer_saque_lista.std(),
        "prom_break_por_partido_varianza": prom_break_por_partido_lista.var(),
        "prom_break_por_partido_desviacion": prom_break_por_partido_lista.std(),
        "prom_break_salvados_varianza": prom_break_salvados_lista.var(),
        "prom_break_salvados_desviacion": prom_break_salvados_lista.std()
    }
    # Crear un DataFrame con los datos de varianza y desviación estándar
    df_varianza_desviacion = pd.DataFrame(varianza_desviacion, index=[0])
    df_varianza_desviacion = df_varianza_desviacion.round(2)

    
    valores_normaliz = [value for name, value in locals().items() if "normalizado" in name]

    dict_normalizado = {"jugador": ganados_testing.loc[0, "winner_name"]} | {name: value for name, value in locals().items() if "normalizado" in name}

    valores_sin_normalizar = {
    "jugador": ganados_testing.loc[0, "winner_name"],
    "porc_victorias": porc_victorias,
    "porc_victorias_clay": porc_victorias_clay,
    "porc_victorias_grass": porc_victorias_grass,
    "porc_victorias_hard": porc_victorias_hard,
    "aces_por_partido": aces_por_partido,
    "dobles_faltas_por_partido": dobles_faltas_por_partido,
    "porc_primer_servicio_in": porc_primer_servicio_in,
    "porc_pts_ganados_primer_saque": porc_pts_ganados_primer_saque,
    "porc_pts_ganados_segundo_saque": porc_pts_ganados_segundo_saque,
    "prom_break_por_partido": prom_break_por_partido,
    "porc_break_salvados": porc_break_salvados
    }

    puntaje = 0
    for i in valores_normaliz:
        puntaje += i

    return puntaje, dict_normalizado, valores_sin_normalizar, df_varianza_desviacion




# lista de pares de jugadores
player_pairs = [("roger_federer", "juan_martin_del_potro"), ("novak_djokovic", "rafael_nadal")]

testing_data = {}

for player1, player2 in player_pairs:
    testing_data[player1] = {
        "ganados": pd.read_csv(f"datos_testing/{player1}_vs_{player2}_{player1}_winner.csv"),
        "perdidos": pd.read_csv(f"datos_testing/{player1}_vs_{player2}_{player2}_winner.csv")
    }
    testing_data[player2] = {
        "ganados": pd.read_csv(f"datos_testing/{player1}_vs_{player2}_{player2}_winner.csv"),
        "perdidos": pd.read_csv(f"datos_testing/{player1}_vs_{player2}_{player1}_winner.csv")
    }

# Diccionario para almacenar los resultados de entrenamiento
testing_results = {}

# Calcular el puntaje para cada jugador y almacenar los resultados
for player1, player2 in player_pairs:
    testing_results[player1] = calc_puntaje(testing_data[player1]["ganados"], testing_data[player1]["perdidos"])
    testing_results[player2] = calc_puntaje(testing_data[player2]["ganados"], testing_data[player2]["perdidos"])

    # Obtener las columnas de los resultados sin normalizar
    columnas = testing_results[player1][2].keys()

    # Crear un DataFrame para los resultados sin normalizar
    df_testing = pd.DataFrame(columns=columnas)
    df_testing.loc[len(df_testing)] = testing_results[player1][2].values()
    df_testing.loc[len(df_testing)] = testing_results[player2][2].values()

    # Crear un DataFrame para los resultados normalizados
    df_testing_normalized = pd.DataFrame(columns=testing_results[player1][1].keys())
    df_testing_normalized.loc[len(df_testing_normalized)] = testing_results[player1][1].values()
    df_testing_normalized.loc[len(df_testing_normalized)] = testing_results[player2][1].values()

    # Redondear todos los valores numéricos a dos cifras decimales
    df_testing = df_testing.round(2)
    df_testing_normalized = df_testing_normalized.round(2)

    # Imprimir los datos de entrenamiento
    print(f"Datos de entrenamiento para {player1} y {player2}:")
    print(df_testing)
    print(f"Datos de entrenamiento normalizados para {player1} y {player2}:")
    print(df_testing_normalized)

    # Guardar en CSV si es necesario
    df_testing.to_csv(f"./enfrentamientos_resultados/testing_results_{player1}_{player2}.csv", index=False)
    df_testing_normalized.to_csv(f"./enfrentamientos_resultados/testing_results_normalized_{player1}_{player2}.csv", index=False)

    # Imprimir los puntajes
    print(f"Puntajes para {player1} y {player2}:")
    print(testing_results[player1][0])
    print(testing_results[player2][0])

    # Calcular la diferencia, multiplicar por 100 y dividir por los valores de la lista
    diff = (df_testing_normalized.iloc[0, 1:-1] - df_testing_normalized.iloc[1, 1:-1]) * 100 / df_testing_normalized.iloc[:, 1:-1].max()
    diff = diff.round(2)  # Redondear la diferencia a dos cifras decimales
    print(f"Diferencia normalizada multiplicada por 100 y dividida por los valores superiores para {player1} y {player2}:")
    print(diff)
    
    # Añadir la diferencia como una nueva fila en el DataFrame normalizado
    df_testing_normalized.loc[len(df_testing_normalized)] = ["diferencia porcentual, a favor del 1ero positiva"] + list(diff) + [None]

    # Guardar el DataFrame actualizado en CSV si es necesario
    df_testing_normalized.to_csv(f"./enfrentamientos_resultados/testing_results_normalized_{player1}_{player2}.csv", index=False)

    testing_results[player1][3].to_csv(f"./enfrentamientos_resultados/varianza_desviacion_{player1}.csv", index=False)
    testing_results[player2][3].to_csv(f"./enfrentamientos_resultados/varianza_desviacion_{player2}.csv", index=False)

    










