import pandas as pd
import numpy as np

def promedio(df_win, df_lose, total, col:str):
    return (df_win["w_" + col].sum() + df_lose["l_" + col].sum()) / total

def acum_total(df_win, df_lose, param:str):
    return df_win["w_" + param].sum() + df_lose["l_" + param].sum()

def normalizacion_positiva(valor, min, max):
    norm = (valor-min)/(max-min) * 100
    
    return 100 if norm >= 100 else norm

def normalizacion_negativa(valor, min, max):
    norm = (1 - (valor-min)/(max-min)) * 100

    return 100 if norm >= 100 else norm

def ponderar(valor, pond):
    return valor * pond / 100


def calc_puntaje(ganados_training, perdidos_training):
    ########## PORCENTAJE DE VICTORIAS ##########

    # Victorias, derrotas y partidos totales de Nadal en training
    victorias_totales = len(ganados_training)
    derrotas_totales = len(perdidos_training)
    partidos_totales = derrotas_totales + victorias_totales

    ## VALOR A NORMALIZAR:
    # Porcentaje de victorias, no necesita normalizacion
    porc_victorias = (victorias_totales/partidos_totales) * 100


    ########## PROMEDIO ACES POR PARTIDO ##########

    ## VALOR A NORMALIZAR:
    # Promedio Aces por partido
    aces_por_partido = promedio(ganados_training, perdidos_training, partidos_totales, "ace")


    ########## PROMEDIO DOBLE FALTAS POR PARTIDO ##########

    ## VALOR A NORMALIZAR:
    # Promedio dobles faltas por partido
    dobles_faltas_por_partido =  promedio(ganados_training, perdidos_training, partidos_totales, "df")


    ########## PORCENTAJE DE 1ER SERVICIO ADENTRO, DE TODOS LOS SERVICIOS JUGADOS ##########

    # todos los servicios de Nadal sin contar doble falta
    total_servicios_sin_df = perdidos_training["l_svpt"].sum() - perdidos_training["l_df"].sum() + ganados_training["w_svpt"].sum() - ganados_training["w_df"].sum()# Porcentaje de primeros servicios adentro
    # todos los servicios de Nadal contando doble falta
    total_servicios_con_df = perdidos_training["l_svpt"].sum() + ganados_training["w_svpt"].sum()

    # Total de primeros servicios adentro
    total_primer_servicio_in = acum_total(ganados_training, perdidos_training, "1stIn")

    ## VALOR A NORMALIZAR:
    # porcentaje de primer servicio adentro de todos los servicios jugados
    porc_primer_servicio_in = total_primer_servicio_in / total_servicios_sin_df * 100

    ########## PORCENTAJE DE PTS GANADOS CON 1ER Y 2DO SAQUE RESPECTO A LOS JUGADOS DE ESE TIPO ##########

    # Total de pts ganados por nadal de primer saque
    pts_ganados_primer_saque = acum_total(ganados_training, perdidos_training, "1stWon")
    # idem pero 2do saque
    pts_ganados_segundo_saque = acum_total(ganados_training, perdidos_training, "2ndWon")

    ## VALORES A NORMALIZAR:
    # porcentaje de pts ganados de primer saque, de todos los bien convertidos
    porc_pts_ganados_primer_saque = pts_ganados_primer_saque / total_primer_servicio_in * 100
    # porcentaje de pts ganados de 2do saque, de todos los bien convertidos
    porc_pts_ganados_segundo_saque = pts_ganados_segundo_saque / (total_servicios_sin_df - total_primer_servicio_in) *100

    ########## PROMEDIO BREAK POINTS SALVADOS POR PARTIDO ##########

    ## VALOR A NORMALIZAR:
    # promedio de break points 
    prom_break_por_partido = promedio(ganados_training, perdidos_training, partidos_totales, "bpFaced")

    ########## PORCENTAJE DE BREAK POINTS SALVADOS RESPECTO A LOS JUGADOS ##########

    break_jugados = acum_total(ganados_training, perdidos_training, "bpFaced")
    break_salvados = acum_total(ganados_training, perdidos_training, "bpSaved")

    ## VALOR A NORMALIZAR:
    porc_break_salvados = break_salvados / break_jugados * 100

    ########## PORC VICTORIAS SEGUN SUELO RESPECTO A PARTIDOS JUGADOS EN ESE SUELO ##########

    # Total de partidos ganados en cada superficie
    partidos_ganados_clay = len(ganados_training[ganados_training["surface"].str.contains("Clay")])
    partidos_ganados_grass = len(ganados_training[ganados_training["surface"].str.contains("Grass")])
    partidos_ganados_hard = len(ganados_training[ganados_training["surface"].str.contains("Hard")])

    # total de partidos jugados en cada superficie
    partidos_totales_clay = partidos_ganados_clay + len(perdidos_training[perdidos_training["surface"].str.contains("Clay")])
    partidos_totales_grass = partidos_ganados_grass + len(perdidos_training[perdidos_training["surface"].str.contains("Grass")])
    partidos_totales_hard = partidos_ganados_hard + len(perdidos_training[perdidos_training["surface"].str.contains("Hard")])

    ## VALORES A NORMALIZAR:
    # porcentaje de victorias en cada superficie
    porc_victorias_clay = partidos_ganados_clay / partidos_totales_clay * 100
    porc_victorias_grass = partidos_ganados_grass / partidos_totales_grass * 100
    porc_victorias_hard = partidos_ganados_hard / partidos_totales_hard * 100

    ########## NORMALIZACIONES Y PONDERACIONES ##########

    # Porc de victorias no necesita normalizacion ni en gral ni en tipo de suelo
    porc_victorias_normalizado = ponderar(normalizacion_positiva(porc_victorias,40, 70), 20)


    porc_victorias_tipo_de_suelo_normalizado = ponderar(ponderar(porc_victorias_clay, 60) + ponderar(porc_victorias_grass, 30) + ponderar(porc_victorias_hard, 10), 3)

    # Aces
    aces_normalizado = ponderar(normalizacion_positiva(aces_por_partido, 0, 12), 15)

    # dobles faltas

    dobles_faltas_por_partido_normalizado = ponderar(normalizacion_negativa(dobles_faltas_por_partido, 2, 8), 9)

    # porc primeros servicios adentro

    porc_primer_servicio_in_normalizado = ponderar(normalizacion_positiva(porc_primer_servicio_in, 45, 60), 11)


    # prom puntos ganados 1er saque

    porc_pts_ganados_primer_saque_normalizado = ponderar(normalizacion_positiva(porc_pts_ganados_primer_saque, 45, 65), 15)

    # prom puntos ganados 2do saque

    porc_pts_ganados_segundo_saque_normalizado = ponderar(normalizacion_positiva(porc_pts_ganados_segundo_saque, 45, 65), 7)

    # break points enfrentados

    break_points_enfrentados_normalizado = ponderar(normalizacion_negativa(prom_break_por_partido, 2, 8), 10)

    # break points salvados

    porc_break_points_salvados_normalizado = ponderar(normalizacion_positiva(porc_break_salvados, 40, 70), 10)


    valores_normaliz = [value for name, value in locals().items() if "normalizado" in name]

    dict_normalizado = {"jugador": ganados_training.loc[0, "winner_name"]} | {name: value for name, value in locals().items() if "normalizado" in name}

    valores_sin_normalizar = {
    "jugador": ganados_training.loc[0, "winner_name"],
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

    return puntaje, dict_normalizado, valores_sin_normalizar



nadal_ganados_training = pd.read_csv("datos_training/nadal_training_ganados.csv")
nadal_perdidos_training = pd.read_csv("datos_training/nadal_training_perdidos.csv")

djokovic_ganados_training = pd.read_csv("datos_training/djokovic_training_ganados.csv")
djokovic_perdidos_training = pd.read_csv("datos_training/djokovic_training_perdidos.csv")



datos_nadal = calc_puntaje(nadal_ganados_training, nadal_perdidos_training)
datos_djokovic = calc_puntaje(djokovic_ganados_training, djokovic_perdidos_training)


columnas = datos_nadal[2].keys()

df = pd.DataFrame(columns=columnas)
df.loc[len(df)] = datos_nadal[2].values()
df.loc[len(df)] = datos_djokovic[2].values()

df2 = pd.DataFrame(columns=datos_nadal[1].keys())
df2.loc[len(df2)] = datos_nadal[1].values()
df2.loc[len(df2)] = datos_djokovic[1].values()


print(df2)
#df.to_csv("./test.csv")
#df2.to_csv("./test2.csv")

