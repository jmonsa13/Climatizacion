# Python File for streamlit tools
# Climatización Girardota Salon 3 y CBC/BDT
# 01-Marzo-2022
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import os
import datetime
import time

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from st_aggrid import AgGrid

# Internal Function
from SQL_Function_Climat import get_data_day, get_data_range
from Plot_Function_Climat import plot_html_Salon3
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Streamlit Setting
st.set_page_config(page_title="IIOT - Corona - Climatización Girardota",
                   initial_sidebar_state="collapsed",
                   page_icon="📈",
                   layout="wide")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Initial page
st.title(' 📈 IIOT|Corona: Climatización Salones Girardota')

st.markdown("""---""")
st.header("Selección de Salon a Visualizar")
climat = st.radio("¿Que salon desea visualizar?", ["Salon 3", "Salon CBC/BDT"], 0)
st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if climat == "Salon 3":
    st.header("Climatización Salon 3")
    st.subheader("1) Selección de Periodo a Analizar")
    col1, col2 = st.columns(2)
    with col1:
        sel_fecha = st.radio("¿Que periodo de tiempo desea analizar?",
                             ('Por día', 'Por rango de días'), key="fecha")

        # Descargar nuevamente flag
        flag_download = False
        if st.checkbox("Descargar nuevamente"):
            flag_download = True
            st.legacy_caching.clear_cache()

    with col2:
        # Opciones por día
        if sel_fecha == "Por día":
            sel_dia = st.date_input("¿Que dia desea analizar?", datetime.date.today(), key="dia")
            if sel_dia > datetime.date.today():
                st.error("Recuerda que el día seleccionado no puede ser superior a la día actual")
                st.stop()
            st.info("Analizaras el día " + str(sel_dia))

        # Opciones por rango de días
        elif sel_fecha == "Por rango de días":
            sel_dia_ini = st.date_input("Seleccione el día inicial", datetime.date.today() -
                                        datetime.timedelta(days=1), key="dia_ini")
            sel_dia_fin = st.date_input("Seleccione el día final", datetime.date.today(), key="dia_fin")

            if sel_dia_fin <= sel_dia_ini:
                st.error("Recuerda seleccionar una fecha inicial anterior a la fecha final!!!")
                st.stop()
            elif sel_dia_fin > datetime.date.today():
                st.error("Recuerda que la fecha final no puede ser superior a la fecha actual")
                st.stop()
            else:
                st.info("Analizaras un periodo de tiempo de " + str((sel_dia_fin - sel_dia_ini).days + 1) + " días.")

    st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # Visualizando la información
    st.subheader("2) Graficar Información")
    descargar = st.checkbox("Graficar", key="climat")
    if descargar is True:
        # Descargando la información
        with st.spinner('Descargando la información...'):
            if sel_fecha == "Por día":
                df, salud_list, salud_datos, title = get_data_day(sel_dia, flag_download)
                text_dia = str(sel_dia)
            elif sel_fecha == "Por rango de días":
                df, salud_list, salud_datos, title = get_data_range(sel_dia_ini, sel_dia_fin,
                                                                         flag_download)
                text_dia = "from_" + str(sel_dia_ini) + "_to_" + str(sel_dia_fin)
            # ----------------------------------------------------------------------------------------------------------
            # Salud de los datos descargada
            c1, c2, c3 = st.columns(3)
            c1.success("Información descargada")
            c2.metric(label="Salud global de los datos", value="{:.2f}%".format(salud_datos))
            # ----------------------------------------------------------------------------------------------------------
        # Dibujando la grafica
        with st.spinner('Dibujando la información...'):
            fig = plot_html_Salon3(df, title)
            st.plotly_chart(fig, use_container_width=True)
        st.expander("Ver los datos")
        tabla = AgGrid(df,
                       editable=False,
                       sortable=True,
                       filter=True,
                       resizable=True,
                       defaultWidth=5,
                       fit_columns_on_grid_load=False,
                       theme="streamlit",  # "light", "dark", "blue", "fresh", "material"
                       key='analisis_table',
                       reload_data=True,
                       )
    st.markdown("""---""")

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # Visualizando la información
    st.subheader("3) Analizar los datos")

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
elif climat == "Salon CBC/BDT":
    st.header("Climatización Salon CBC/BDT")
    st.subheader("1.Selección de Data a Analizar")


# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.markdown("**Creado por:**")
st.sidebar.write("Juan Felipe Monsalvo Salazar")
st.sidebar.write("jmonsalvo@corona.com.co")
st.sidebar.markdown("**Creado el:** 01/03/2022")
