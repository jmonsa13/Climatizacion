# Python File for streamlit tools
# Sales Baños y Cocna
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import datetime

import streamlit as st
from st_aggrid import AgGrid

# Internal Function
from SQL_Function_Climat import sql_plot_climat

# ----------------------------------------------------------------------------------------------------------------------
# Streamlit Setting
st.set_page_config(page_title="IIOT - Corona - Climatización Girardota",
                   initial_sidebar_state="collapsed",
                   page_icon="📈",
                   layout="wide")

#tabs = ["Climatización Salon 3", "Climatización Salon CBC/BDT" ]
#page = st.sidebar.radio("Tabs", tabs)
# ----------------------------------------------------------------------------------------------------------------------
# Importing the DataFrame
st.title(' 📈 IIOT|Corona: Climatización Salones Girardota')

climat = st.radio("¿Que salon desea visualizar?", ["Salon 3", "Salon CBC/BDT"], 0)

if climat == "Salon 3":
    st.header("Climatización Salon 3")
    st.subheader("1.Selección de Data a Analizar")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Opciones de Fecha**")
        sel_fecha = st.radio("¿Que periodo de tiempo desea analizar?",
                             ('Por día', 'Por rango de días'), key="fecha")
    with c2:
        if sel_fecha == "Por día":
            sel_dia = st.date_input("¿Que dia desea analizar?", datetime.date.today(), key="dia")
            if sel_dia > datetime.date.today():
                st.error("Recuerda que el día seleccionado no puede ser superior a la día actual")
                st.stop()
            st.info("Analizaras el día " + str(sel_dia))
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

    st.subheader("2.Visualización de los Datos")
    if st.checkbox("Graficar Información", key="climat"):
        with st.spinner('Descargando la información y dibujandola...'):
            if sel_fecha == "Por día":
                df, fig = sql_plot_climat(tipo="day", day=str(sel_dia), database='CLIMATI', table="CLIMATI",
                                          page=climat)
                st.plotly_chart(fig, use_container_width=True)
            elif sel_fecha == "Por rango de días":
                df, fig = sql_plot_climat(tipo="rango", ini=str(sel_dia_ini), day=str(sel_dia_fin),
                                           database='CLIMATI', table="CLIMATI", page=climat)
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("3. Mostrar Base de datos")
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
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
elif climat == "Salon CBC/BDT":
    st.header("Climatización Salon CBC/BDT")
    st.subheader("1.Selección de Data a Analizar")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Opciones de Fecha**")
        sel_fecha = st.radio("¿Que periodo de tiempo desea analizar?",
                             ('Por día', 'Por rango de días'), key="fecha")
    with c2:
        if sel_fecha == "Por día":
            sel_dia = st.date_input("¿Que dia desea analizar?", datetime.date.today(), key="dia")
            if sel_dia > datetime.date.today():
                st.error("Recuerda que el día seleccionado no puede ser superior a la día actual")
                st.stop()
            st.info("Analizaras el día " + str(sel_dia))
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

    st.subheader("2.Visualización de los Datos")
    if st.checkbox("Graficar Información", key="climat"):
        with st.spinner('Descargando la información y dibujandola...'):
            if sel_fecha == "Por día":
                df, fig = sql_plot_climat(tipo="day", day=str(sel_dia), database='CLIMATI', table="CLIMATI",
                                          page=climat)
                st.plotly_chart(fig, use_container_width=True)
            elif sel_fecha == "Por rango de días":
                df, fig = sql_plot_climat(tipo="rango", ini=str(sel_dia_ini), day=str(sel_dia_fin),
                                          database='CLIMATI', table="CLIMATI", page=climat)
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("3. Mostrar Base de datos")
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



# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.markdown("**Creado por:**")
st.sidebar.write("Juan Felipe Monsalvo Salazar")
st.sidebar.write("jmonsalvo@corona.com.co")
st.sidebar.markdown("**Creado el:** 19/10/2021")
