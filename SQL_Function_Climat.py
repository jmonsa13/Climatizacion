# Python File function for streamlit tools
# Sales Baños y Cocna
# 03-August-2021
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import pandas as pd

import datetime
import calendar as cl

import streamlit as st
import pyodbc

from Plot_Function_Climat import plot_html
# ----------------------------------------------------------------------------------------------------------------------

# Function definition
@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=False)
def load_data(folder="./Data/Raw/", filename="tabla_robot1_2021_04_22_1012.csv"):
    """
    Función que carga el archivo csv guardado al conectar con la base de datos y devuelve un dataframe
    """
    df = pd.read_csv(folder + filename, )

    return df

def fecha_format(df):
    """
    Función que hace el manejo de la columna de fecha de la base de datos
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

    # Organizo las columnas
    #re_columns = ['estado', 'fecha', 'referencia', 'peso_antes', 'peso_despues', 'sp_fmasico', 'fmasico',
                  #'sp_patomizacion', 'patomizacion',
                  #'sp_pabanico', 'pabanico', 'presion_red', 'año', 'mes', 'dia', 'ndia', 'hora', 'minuto', 'segundo',
                  #"fecha_planta"]
    #df = df[re_columns]

    # Ordeno la data por la fecha
    df = df.sort_values(by='fecha', ascending=True)

    df.set_index("fecha", inplace=True, drop=False)

    return df

@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=600)
def sql_connect(tipo="day", day="2021-04-28", ini="2021-04-27", server='EASAB101', database='CLIMATI',
                table="CLIMATI", username='IOTVARPROC', password='10Tv4rPr0C2021*'):
    """
    Programa que permite conectar con una base de dato del seervidor y devuelve la base de dato como un pandas dataframe
    INPUT:
        tipo = ["day", "all", "turno", "rango"]
        day = Día inicial EN STR
    OUTPUT:
        pd_sql = pandas dataframe traido de la base de dato SQL
    """

    # Connecting to the sql database
    conn = pyodbc.connect(
        'driver={SQL Server};server=%s;database=%s;uid=%s;pwd=%s' % (server, database, username, password))

    if tipo == "all":
        pd_sql = pd.read_sql_query('SELECT * FROM ' + database + '.dbo.' + table, conn)

        # Saving the sql dataframe to a output file
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y_%m_%d_%H%M")

        #pd_sql.to_csv('./Data/Raw/All_tabla_' + table + '_' + dt_string + '.csv', index=False)
        #pd_sql.to_excel('./Data/Raw/All_tabla_' + table + '_'+ dt_string + '.xlsx', index = False )

    elif tipo == "day":
        pd_sql = pd.read_sql_query("SELECT * FROM " + database + ".dbo." + table + " WHERE fecha like '" + day + "'",
                                   conn)

        # Saving the files
        #pd_sql.to_csv('./Data/Raw/tabla_' + table + '_' + day + '.csv', index=False)
        # pd_sql.to_excel('./Data/Raw/tabla_' + table + '_'+ day + '.xlsx', index = False )

    elif tipo == "rango":
        pd_sql = pd.read_sql_query(
            "SELECT * FROM " + database + ".dbo." + table + " WHERE fecha between '" + ini + "'" + " AND '" + day + "'",
            conn)

        # Saving the files
        #pd_sql.to_csv('./Data/Raw/tabla_' + table + '_entre_' + ini + "_y_" + day + '.csv', index=False)
        # pd_sql.to_excel('./Data/Raw/tabla_' + table + '_entre_'+ ini +"_y_"+ day + '.xlsx', index = False )

    return pd_sql

@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=600)
def sql_plot_climat(tipo="day", day="2021-04-28", ini="2021-04-27", database='CLIMATI', table="CLIMATI"):
    """
    Función que se conecta a la base de dato y crea el archivo de visualización a la vez que lo guarda
    INPUT:
        tipo = ["day", "all", "turno", "rango"]
        turno = 1 or 2 or 3
        day = Día inicial EN STR
        ini = Día final EN STR (util cuando el tipo es rango)
    OUTPUT:
        df = pandas dataframe traido de la base de dato SQL
    """
    df = sql_connect(tipo=tipo, day=day, ini=ini, database=database, table=table)
    df = fecha_format(df)

    # Defining the title and filename for saving the plots
    if tipo == "day":
        filename = table + '_día_' + day + '.html'
        title = "Climatización Salon 3 del Día " + day
    elif tipo == "rango":
        filename = table + '_entre_' + ini + "_y_" + day + '.html'
        title = " Climatización Salon 3 entre " + ini + " y " + day

    # Plotting the DF
    fig = plot_html(df, title, filename)
    return df, fig