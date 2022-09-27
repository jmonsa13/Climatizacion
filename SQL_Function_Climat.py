# Python File function for streamlit tools
# Climatización Girardota Salon 3 y CBC/BDT
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import datetime
import os

import numpy as np
import pandas as pd
import pyodbc
import streamlit as st


# ----------------------------------------------------------------------------------------------------------------------
# Function definition
@st.experimental_memo(suppress_st_warning=True, show_spinner=True)
def load_data(folder="./Data/Raw/", filename="tabla_robot1_2021_04_22_1012.csv"):
    """
    Función que carga el archivo csv guardado al conectar con la base de datos y devuelve un dataframe
    """
    df = pd.read_csv(folder + filename, )

    return df


def organize_df(df, sql_table="Salón 3"):
    """
    Función que organiza el data frame, generando nuevas columnas de informaciónd e fechas, reorganizando las columnas
    y redodeando los valores a 2 cifras decimales.
    INPUT:
        df = data frame original
        sql_table = Selección de la tabla SQL de climatización a la que se conectara
    OUTPUT:
        df = data frame  reorganizado
    """
    # Organizar el tema de fecha
    df["fecha"] = pd.to_datetime(df['fecha'], format='%Y/%m/%d', exact=False)
    df['fecha'] += pd.to_timedelta(df["hora"], unit='h')
    df['fecha'] += pd.to_timedelta(df["minuto"], unit='m')
    df['fecha'] += pd.to_timedelta(df["segundo"], unit='s')

    # Separar los años, meses y días
    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["dia"] = df["fecha"].dt.day
    df["ndia"] = df["fecha"].dt.day_name()

    # Creo columna de fecha organizacional
    df["fecha_planta"] = [elem - datetime.timedelta(days=1) if df["hora"].iloc[x] < 6 else elem for x, elem in
                          enumerate(df["fecha"])]

    if sql_table in ["Salón 3", "Salón CBC/BDT"]:
        # Creo columna de encendido ventiladores
        df["MontinyecbdtON"] = [1 if i > 0 else 0 for i in df["Motinyecbdthz"]]
        df["Montinyecsal3ON"] = [1 if i > 0 else 0 for i in df["Motinyecsal3hz"]]

        # Organizo las columnas
        re_columns = ['fecha', 'Tempwh', 'TempSuccion', 'Temp_Exterior_Amb',
                      'Tempcirc_caldera', 'Tempentagua', "Tempcircagua", "Prescircagua",
                      'TempInyecbdtcbc', 'TempBDT1y2', 'HumBDT1y2', 'TempBDT3y4', 'HumBDT3y4',
                       'TempPresBDT4', 'HumPresBDT4', 'SP_TempPresBDT4', 'SP_HumPresBDT4',
                      'TempBDT5', 'HumBDT5', 'TempBDT6', 'HumBDT6',
                      'Motinyecbdtamp', 'Motinyecbdtpot', 'Motinyecbdthz', "MontinyecbdtON",
                      "Automatico_CBCBDT", 'Comp_BDT_Succion', 'Comp_BDT_Exterior', 'Comp_BDT_Recircula',
                      'TempInyecsalon3', 'TempInyecquemsalon3', 'S3temppmax', 'S3humpmax', 'S3temptac', 'S3humtac',
                      'SP_Temp_QS3', 'SP_Temp_S3', 'SP_Humedad_S3',
                      'Motinyecsal3amp', 'Motinyecsal3pot', 'Motinyecsal3hz', "Montinyecsal3ON",
                      'Automatico_S3', 'Comp_S3_Exterior', 'Comp_S3_Succion', 'ExtS3Estado',
                      'QS3ON_PLC', 'QS3On_Confirm', 'QS3Falla',
                      'año', 'mes', 'dia', 'ndia', 'hora', 'minuto', 'segundo', "fecha_planta"
                      ]
        df = df[re_columns]

        # Round the complete dataframe
        df = df.round(2)

        # Converting to 0/1
        df['ExtS3Estado'] = df['ExtS3Estado'].fillna(value=False)
        boolean_list = ['Automatico_CBCBDT', 'Automatico_S3', 'QS3ON_PLC', 'QS3On_Confirm', 'QS3Falla', 'ExtS3Estado']
        for item in boolean_list:
            df[item] = df[item].astype(int)

    elif sql_table == "Salón CDI":
        # Organizo las columnas
        re_columns = ['fecha', 'Tempwh', 'CDITempprom', 'CDISPTemp', 'CDISPHum', 'CDITempz1', 'CDIHumz1', 'CDITempz2',
                      'CDIHumz2', 'CDISPW', 'CDIWZ1','CDIWZ2',
                      'CDIPosComp', 'CDIVentInyec',
                      'Extrac1', 'Extrac2', 'Extrac3',
                      'Extrac4', 'Extrac5', 'Extrac6', 'PresionSalon',
                      'año', 'mes', 'dia', 'ndia', 'hora', 'minuto', 'segundo', "fecha_planta"]
        df = df[re_columns]

        # Renaming the columns
        df.columns = ['fecha', 'Tempwh', 'TempProm', 'SPTemp', 'SPHum', 'TempZ1', 'HumZ1', 'TempZ2', 'HumZ2',
                      'SPW', 'WZ1','WZ2',
                      'PosComp', 'VentInyec',
                      'Extrac1', 'Extrac2', 'Extrac3',
                      'Extrac4', 'Extrac5', 'Extrac6', 'PresionSalon',
                      'año', 'mes', 'dia', 'ndia', 'hora', 'minuto', 'segundo', "fecha_planta"]

        # Round the complete dataframe
        df = df.round(2)

        # Converting to 0/1
        boolean_list = ['VentInyec', 'Extrac1', 'Extrac2', 'Extrac3', 'Extrac4', 'Extrac5', 'Extrac6']
        for item in boolean_list:
            df[item] = df[item].astype(int)

    # Sorting the df by the date
    df = df.sort_values(by='fecha', ascending=True)

    # Setting fecha as an index
    df.set_index("fecha", inplace=True, drop=False)

    return df


def add_day(day, add=1):
    """
    Función agrega o quita dias, teniendo en cuenta inicio de mes e inicio de año
    INPUT
        day = "2021-02-01"  EN STRING
    OUTPUT
        ini_date = día entregado en STR
        fin_date = día con los días sumados o restados en STR al día ingresado
    """
    l_day_n = [int(x) for x in day.split("-")]
    ini_date = datetime.date(l_day_n[0], l_day_n[1], l_day_n[2])
    fin_date = ini_date + datetime.timedelta(days=add)

    return str(ini_date), str(fin_date)


@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def get_data_day(sel_dia="2022-01-01", sql_table="Salón 3", flag_download=False):
    """
    Programa que permite conectar con una base de dato del servidor y devuelve la base de dato como un pandas dataframe
    INPUT:
        sel_dia = Día inicial EN STR
        sql_table = Selección de la tabla SQL de climatización a la que se conectara
        redownload = Debe descargarse la data o buscar dentro de los archivos previamente descargados.
    OUTPUT:
        df = pandas dataframe traído de la base de dato SQL
        salud_list = lista con el dato de salud por día
        salud_datos = Número | Salud total de los datos
        title = Título para la gráfica
    """
    # Definición del numero total de datos por días
    datos_días = 24 * 60 * 2  # 24 horas en un día x 60 minutos en cada hora x 2 veces que tomo el dato cada minuto

    # Conexión a la base de datos SQL
    if sql_table in ["Circuito Agua", "Salón 3", "Salón CBC/BDT"]:
        df = find_load(tipo="day_planta", day=str(sel_dia), ini=None, database="CLIMATI",
                       table="CLIMATI", redownload=flag_download)
    elif sql_table == "Salón CDI":
        df = find_load(tipo="day_planta", day=str(sel_dia), ini=None, database="CLIMATI",
                       table="CLIMATI_CDI", redownload=flag_download)

    # Organizing the raw DF
    df = organize_df(df, sql_table)

    # Defining the title and filename for saving the plots
    title = "Variables de Climatización Día " + str(sel_dia)

    # Salud de los datos
    salud_datos = (df.shape[0] / datos_días) * 100
    salud_list = [np.round(salud_datos, 2)]

    return df, salud_list, salud_datos, title


@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def get_data_range(sel_dia_ini="2022-01-01", sel_dia_fin="2022-01-02", sql_table="Salón 3", flag_download=False):
    """
    Programa que permite conectar con una base de dato del servidor y devuelve la base de dato como un pandas dataframe
    del periodo de fecha ingresado
    INPUT:
        sel_dia_ini = Día inicial en STR ("2022-01-01")
        sel_dia_fin = Día final en STR ("2022-01-02")
        sql_table = Selección de la tabla SQL de climatización a la que se conectara
        redownload = Debe descargarse la data o buscar dentro de los archivos previamente descargados
    OUTPUT:
        df = pandas dataframe traído de la base de dato SQL
        salud_list = lista con el dato de salud por día
        salud_datos = Número | Salud total de los datos.
        title = Título para la gráfica
        """
    # Definición del numero total de datos por días
    datos_días = 24 * 60 * 2  # 24 horas en un día x 60 minutos en cada hora x 2 veces que tomo el dato cada minuto

    # Conexión a la base de datos SQL
    if sql_table in ["Circuito Agua", "Salón 3", "Salón CBC/BDT"]:
        df = find_load(tipo="rango_planta", ini=str(sel_dia_ini), day=str(sel_dia_fin), database="CLIMATI",
                       table="CLIMATI", redownload=flag_download)
    elif sql_table == "Salón CDI":
        df = find_load(tipo="rango_planta", ini=str(sel_dia_ini), day=str(sel_dia_fin), database="CLIMATI",
                       table="CLIMATI_CDI", redownload=flag_download)

    # Organizing the raw DF
    df = organize_df(df, sql_table)

    # Defining the title and filename for saving the plots
    title = "Variables de Climatización entre " + str(sel_dia_ini) + " y " + str(sel_dia_fin)

    # Salud de cada día en el periodo
    salud_list = []
    while sel_dia_ini <= sel_dia_fin:
        df_filter = df.loc[(df.index >= str(sel_dia_ini) + ' 06:00:00') &
                           (df.index <= str(sel_dia_ini + datetime.timedelta(days=1)) + ' 05:59:59')]

        salud_dia = np.round((df_filter.shape[0] / datos_días) * 100, 2)
        salud_list.append(salud_dia)
        # Avanzo un día
        sel_dia_ini = sel_dia_ini + datetime.timedelta(days=1)
    salud_datos = sum(salud_list) / len(salud_list)

    return df, salud_list, salud_datos, title


# No poner cache en esta función para poder cargar los ultimos datos del día.
def find_load(tipo, day, ini, database, table, redownload):
    """
    Función que busca y carga el archivo de datos si este ya ha sido descargado. En caso contrario lo descarga a través
    de la función sql_connet
    INPUT:
        tipo: ["day_planta", "rango_planta"].
        day: día final o unico día a analizar como STR ("2022-01-01").
        ini: día inicial a analizar en el rango como STR ("2021-12-28").
        database: base de dato a la cual se debe conectar.
        table: tabla a la cual se debe conectar.
        redownload = TRUE or FALSE statement si es TRUE se omite la parte de buscar el archivo y se descarga nuevamente.
    OUTPUT:
        pd_sql: dataframe con los datos buscados o descargados
    """
    # Setting the folder where to search
    directory = './Data/Raw/' + day[:-3] + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filenames = os.listdir(directory)

    # Empty dataframe
    pd_sql = pd.DataFrame()

    if tipo == "day_planta":
        # Creo el nombre del archivo a buscar
        filename = 'tabla_' + table + '_' + day + '.csv'
        if filename in filenames and redownload is False:
            pd_sql = load_data(folder=directory, filename=filename)
        else:
            pd_sql = sql_connect(tipo=tipo, day=day, database=database, table=table)

    elif tipo == "rango_planta":
        # Fecha Inicial
        l_ini_n = [int(x) for x in ini.split("-")]
        ini_date = datetime.date(l_ini_n[0], l_ini_n[1], l_ini_n[2])
        # Fecha Final
        l_day_n = [int(x) for x in day.split("-")]
        day_date = datetime.date(l_day_n[0], l_day_n[1], l_day_n[2])

        # Recorro los días de ese periodo de tiempo
        while ini_date <= day_date:
            # Creo el nombre del archivo a buscar
            filename = 'tabla_' + table + '_' + str(ini_date) + '.csv'
            if filename in filenames and redownload is False:
                aux = load_data(folder=directory, filename=filename)
            else:
                aux = sql_connect(tipo="day_planta", day=str(ini_date), database=database, table=table)

            pd_sql = pd.concat([pd_sql, aux])
            # Avanzo un día
            ini_date = ini_date + datetime.timedelta(days=1)

    return pd_sql

# No poner cache en esta función para poder cargar los ultimos datos del día
def sql_connect(tipo="day", day="2021-04-28", server='EASAB101', database='CLIMATI',
                table="CLIMATI", username='IOTVARPROC', password='10Tv4rPr0C2021*'):
    """
    Programa que permite conectar con una base de dato del servidor y devuelve la base de dato como un pandas dataframe
    INPUT:
        tipo = ["day_planta", "day"]
        day = Día a descargar en  STR ("2021-04-28")
        database: base de dato a la cual se debe conectar
        table: tabla a la cual se debe conectar
    OUTPUT:
        pd_sql = pandas dataframe traído de la base de dato SQL
    """
    # Connecting to the sql database
    conn = pyodbc.connect(
        'driver={SQL Server};server=%s;database=%s;uid=%s;pwd=%s' % (server, database, username, password))
    # ------------------------------------------------------------------------------------------------------------------
    # Tipos de conexiones establecidas para traer distintas cantidades de datos
    # ------------------------------------------------------------------------------------------------------------------
    if tipo == "day":
        pd_sql = pd.read_sql_query("SELECT * FROM " + database + ".dbo." + table + " WHERE fecha like '" + day + "'",
                                   conn)

        # Guardando los datos en archivos estaticos
        if day == str(datetime.date.today()):
            pass  # No guardar datos si el día seleccionado es el día actual del sistema
        else:
            pd_sql.to_csv('./Data/Raw/tabla_' + table + '_' + day + '.csv', index=False)
            # pd_sql.to_excel('./Data/Raw/tabla_' + table + '_'+ day + '.xlsx', index = False )

    elif tipo == "day_planta":
        ini, fin = add_day(day)
        pd_sql_1 = pd.read_sql_query("SELECT * FROM " + database + ".dbo." + table + " WHERE fecha like '" + ini + "'"
                                     + " AND hora between 6 and 23", conn)

        pd_sql_2 = pd.read_sql_query("SELECT * FROM " + database + ".dbo." + table + " WHERE fecha like '" + fin + "'"
                                     + " AND hora between 0 and 5", conn)
        pd_sql = pd.concat([pd_sql_1, pd_sql_2])

        # Guardando los datos en archivos estaticos
        if day == str(datetime.date.today()):
            pass  # No guardar datos si el día seleccionado es el día actual del sistema
        else:
            # Checking and creating the folder
            folder = day[:-3]
            if not os.path.exists('./Data/Raw/' + folder):
                os.makedirs('./Data/Raw/' + folder)
            # Saving the raw data
            pd_sql.to_csv('./Data/Raw/' + folder + '/tabla_' + table + '_' + day + '.csv', index=False)

    return pd_sql
