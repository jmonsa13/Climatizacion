# Python File function for streamlit tools
# Climatización Girardota Salon 3 y CBC/BDT
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


# ----------------------------------------------------------------------------------------------------------------------
def plot_on_off(fig, df, column, legend, rgb, visibility="legendonly", axis_y="y2", r=1, c=1):

    fig.add_trace(go.Scatter(x=df.index, y=df[column],
                             fill='tozeroy', mode="lines",
                             fillcolor=rgb,
                             line_color='rgba(0,0,0,0)',
                             legendgroup=legend,
                             showlegend=True,
                             name=legend,
                             yaxis=axis_y,
                             visible=visibility)
                  , secondary_y=True, row=r, col=c)

    return fig


@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_Salon3(df, title):
    """
    Función para dibujar los datos de temperatura del salon 3
    INPUT:
        df = pandas dataframe traído de la base de dato SQL
        title = Título de la gráfica
    OUTPUT:
        fig = objeto figura para dibujarlo externamente de la función
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1,  specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
                        shared_xaxes=True, vertical_spacing=0.02,
                        #subplot_titles=('Temperaturas Entradas',  'Temperatura y humedad Salon 3')
                        )

    # Automatico ON/OFF
    fig = plot_on_off(fig, df, "Automatico_S3", "Manual ON", 'rgba(0,0,0,0.5)', visibility=None)

    # Temp Ware House
    fig.add_trace(go.Scatter(x=df.index, y=df["Tempwh"],
                             line=dict(color='#222a2a', width=1.5), # dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='Temp WH',
                             yaxis="y1",
                             ),
                  row=1, col=1,)

    # Temp Succión
    fig.add_trace(go.Scatter(x=df.index, y=df["TempSuccion"],
                             line=dict(color='#d62728', width=1.5),
                             mode='lines',  # 'lines+markers'
                             name='Temp Succión',
                             yaxis="y1",
                             ),
                  row=1, col=1)

    # TempInyecsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecsalon3"],
                             line=dict(color='#ff9900', width=1.5),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny S3',
                             yaxis="y1",
                             ),
                  row=1, col=1)

    # TempInyecquemsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecquemsalon3"],
                             line=dict(color='#1616a7', width=1.5),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny Quemador S3',
                             yaxis="y1",
                             ),
                  row=1, col=1)

    # Ventilador ON/OFF
    fig = plot_on_off(fig, df, "Montinyecsal3ON", "Ventilador ON", 'rgba(55,126,184,0.2)')

    # QS3ON_PLC
    fig = plot_on_off(fig, df, "QS3ON_PLC", "Quemador ON PLC", 'rgba(102,102,102,0.2)')

    # QS3On_Confirm
    fig = plot_on_off(fig, df, "QS3On_Confirm", "Quemador ON Confirm", 'rgba(228,26,28,0.2)')

    # QS3 Falla
    fig = plot_on_off(fig, df, "QS3Falla", "Quemador Falla", 'rgba(102,17,0,0.3)')

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # S3 temptac
    fig.add_trace(go.Scatter(x=df.index, y=df["S3temptac"],
                             line=dict(color='#9467bd', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp TZ AC',
                             yaxis="y3",
                             ),
                  row=2, col=1)

    # S3 humedad tac
    fig.add_trace(go.Scatter(x=df.index, y=df["S3humtac"],
                             line=dict(color='#9467bd', width=1, dash='dot'),
                             mode='lines', name='HR TZ AC',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # S3temppmax
    fig.add_trace(go.Scatter(x=df.index, y=df["S3temppmax"],
                             line=dict(color='#b68100', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp Power Max',
                             yaxis="y3",
                             ),
                  secondary_y=False, row=2, col=1)

    # S3 humedad power max
    fig.add_trace(go.Scatter(x=df.index, y=df["S3humpmax"],
                             line=dict(color='#b68100', width=1, dash='dot'),
                             mode='lines', name='HR Power Max',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # Set Point temperatura
    fig.add_trace(go.Scatter(x=df.index, y=df["SP_Temp_S3"],
                             line=dict(color='#7f7f7f', width=2),  # dash='dash'),
                             mode='lines', name='Set Point Temp',
                             yaxis="y3", visible="legendonly"
                             ),
                  secondary_y=False, row=2, col=1)

    # Set Point humedad
    fig.add_trace(go.Scatter(x=df.index, y=df["SP_Humedad_S3"],
                             line=dict(color='#7f7f7f', width=2, dash='dash'),
                             mode='lines', name='Set Point HR',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # Compuerta Succión
    fig = plot_on_off(fig, df, "Comp_S3_Succion", "Compuerta Succión", 'rgba(255,127,0,0.3)', axis_y="y4", r=2, c=1)

    # Compuerta Exterior
    fig = plot_on_off(fig, df, "Comp_S3_Exterior", "Compuerta Exterior", 'rgba(55,126,184,0.3)', axis_y="y4", r=2, c=1)

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    # Set x-axis and y-axis title
    fig.update_layout(legend_title_text='Variables Salón 3')
    fig['layout']['xaxis2']['title'] = 'Fecha'

    fig['layout']['yaxis']['title'] = 'Temperaturas Entrada °C'

    fig['layout']['yaxis2']['title'] = 'Estado ON/OFF'
    fig['layout']['yaxis2']['range'] = [0, 1]
    fig['layout']['yaxis2']['fixedrange'] = True

    fig['layout']['yaxis3']['title'] = 'Temperaturas Salon 3 °C'
    fig['layout']['yaxis3']['range'] = [20, 35]
    fig['layout']['yaxis3']['fixedrange'] = True

    fig['layout']['yaxis4']['title'] = 'Apertura Compuerta y HR %'
    fig['layout']['yaxis4']['range'] = [50, 85]

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    return fig


@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_CBC_BDT(df, title):
    """
    Función para dibujar los datos de temperatura de los salones CBC-BDT
    INPUT:
        df = pandas dataframe traído de la base de dato SQL
        title = Título de la gráfica
    OUTPUT:
        fig = objeto figura para dibujarlo externamente de la función
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1,  specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
                        shared_xaxes=True, vertical_spacing=0.02,
                        #subplot_titles=('Temperaturas Entradas',  'Temperatura y humedad Salon 3')
                        )

    # Automatico ON/OFF
    fig = plot_on_off(fig, df, "Automatico_CBCBDT", "Manual ON", 'rgba(0,0,0,0.5)', visibility=None)

    # Temp Ware House
    fig.add_trace(go.Scatter(x=df.index, y=df["Tempwh"],
                             line=dict(color='#222a2a', width=1.5), # dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='Temp WH',
                             yaxis="y1",
                             ),
                  row=1, col=1,)

    # Temp Succión
    fig.add_trace(go.Scatter(x=df.index, y=df["TempSuccion"],
                             line=dict(color='#d62728', width=1.5),
                             mode='lines',  # 'lines+markers'
                             name='Temp Succión',
                             yaxis="y1",
                             ),
                  row=1, col=1)

    # Temp Inyec CBC/BDT
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecbdtcbc"],
                             line=dict(color='#ff9900', width=1.5),
                             mode='lines',  # 'lines+markers'
                             name='Temp Inyección',
                             yaxis="y1",
                             ),
                  row=1, col=1)


    # Ventilador ON/OFF
    fig = plot_on_off(fig, df, "MontinyecbdtON", "Ventilador ON", 'rgba(55,126,184,0.2)')
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # BDT Temp 1&2
    fig.add_trace(go.Scatter(x=df.index, y=df["TempBDT1y2"],
                             line=dict(color='#9467bd', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp BDT 1&2',
                             yaxis="y3", visible="legendonly"
                             ),
                  row=2, col=1)

    # BDT HR 1&2
    fig.add_trace(go.Scatter(x=df.index, y=df["HumBDT1y2"],
                             line=dict(color='#9467bd', width=1, dash='dot'),
                             mode='lines', name='HR BDT 1&2',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # BDT Temp 3&4
    fig.add_trace(go.Scatter(x=df.index, y=df["TempBDT3y4"],
                             line=dict(color='#b68100', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp BDT 3&4',
                             yaxis="y3",
                             ),
                  secondary_y=False, row=2, col=1)

    # BDT HR 3&4
    fig.add_trace(go.Scatter(x=df.index, y=df["HumBDT3y4"],
                             line=dict(color='#b68100', width=1, dash='dot'),
                             mode='lines', name='HR BDT 3&4',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # BDT Temp 5
    fig.add_trace(go.Scatter(x=df.index, y=df["TempBDT5"],
                             line=dict(color='#3366cc', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp BDT 5',
                             yaxis="y3", visible="legendonly"
                             ),
                  secondary_y=False, row=2, col=1)

    # BDT HR 5
    fig.add_trace(go.Scatter(x=df.index, y=df["HumBDT5"],
                             line=dict(color='#3366cc', width=1, dash='dot'),
                             mode='lines', name='HR BDT 5',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # BDT Temp 6
    fig.add_trace(go.Scatter(x=df.index, y=df["TempBDT6"],
                             line=dict(color='#109618', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp BDT 6',
                             yaxis="y3", visible="legendonly"
                             ),
                  secondary_y=False, row=2, col=1)

    # BDT HR 6
    fig.add_trace(go.Scatter(x=df.index, y=df["HumBDT6"],
                             line=dict(color='#109618', width=1, dash='dot'),
                             mode='lines', name='HR BDT 6',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # # BDT Temp Presecadero BDT4
    # fig.add_trace(go.Scatter(x=df.index, y=df["TempPresBDT4"],
    #                          line=dict(color='#d62728', width=1.5),  # dash='dash'),
    #                          mode='lines', name='Temp Pres BDT 4',
    #                          yaxis="y3",
    #                          ),
    #               secondary_y=False, row=2, col=1)
    #
    # # BDT HR Presecadero BDT4
    # fig.add_trace(go.Scatter(x=df.index, y=df["HumPresBDT4"],
    #                          line=dict(color='#d62728', width=1, dash='dot'),
    #                          mode='lines', name='HR Pres BDT 4',
    #                          yaxis="y4",
    #                          ),
    #               secondary_y=True, row=2, col=1)

    # Set Point temperatura
    fig.add_trace(go.Scatter(x=df.index, y=df["SP_TempPresBDT4"],
                             line=dict(color='#7f7f7f', width=2),  # dash='dash'),
                             mode='lines', name='Set Point Temp 4',
                             yaxis="y3",
                             ),
                  secondary_y=False, row=2, col=1)

    # Set Point humedad
    fig.add_trace(go.Scatter(x=df.index, y=df["SP_HumPresBDT4"],
                             line=dict(color='#7f7f7f', width=2, dash='dot'),
                             mode='lines', name='Set Point HR 4',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # Compuerta Succión
    fig = plot_on_off(fig, df, "Comp_BDT_Succion", "Compuerta Succión", 'rgba(255,127,0,0.3)', axis_y="y4", r=2, c=1)

    # Compuerta Exterior
    fig = plot_on_off(fig, df, "Comp_BDT_Exterior", "Compuerta Exterior", 'rgba(55,126,184,0.3)', axis_y="y4", r=2, c=1)

    # Compuerta Recirculación
    fig = plot_on_off(fig, df, "Comp_BDT_Recircula", "Compuerta Recirculación", 'rgba(77,175,74,0.3)', axis_y="y4",
                      r=2, c=1)

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    # Set x-axis and y-axis title
    fig.update_layout(legend_title_text='Variables Salón CBC/BDT')
    fig['layout']['xaxis2']['title'] = 'Fecha'

    fig['layout']['yaxis']['title'] = 'Temperaturas Entrada °C'

    fig['layout']['yaxis2']['title'] = 'Estado ON/OFF'
    fig['layout']['yaxis2']['range'] = [0, 1]
    fig['layout']['yaxis2']['fixedrange'] = True

    fig['layout']['yaxis3']['title'] = 'Temperaturas Salon CBC/BDT °C'
    fig['layout']['yaxis3']['range'] = [20, 35]
    fig['layout']['yaxis3']['fixedrange'] = True

    fig['layout']['yaxis4']['title'] = 'Apertura Compuerta y HR %'
    fig['layout']['yaxis4']['range'] = [50, 85]

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    return fig

@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_CDI(df, title):
    """
    Función para dibujar los datos de temperatura de los salones CDI
    INPUT:
        df = pandas dataframe traído de la base de dato SQL
        title = Título de la gráfica
    OUTPUT:
        fig = objeto figura para dibujarlo externamente de la función
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1,  specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
                        shared_xaxes=True, vertical_spacing=0.02,
                        #subplot_titles=('Temperaturas Entradas',  'Temperatura y humedad Salon 3')
                        )

    # Automatico ON/OFF
    #fig = plot_on_off(fig, df, "Automatico_CBCBDT", "Manual ON", 'rgba(0,0,0,0.5)', visibility=None)

    # Temp Ware House
    fig.add_trace(go.Scatter(x=df.index, y=df["Tempwh"],
                             line=dict(color='#222a2a', width=1.5), # dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='Temp WH',
                             yaxis="y1",
                             ),
                  row=1, col=1,)

    # Temp Succión
    # fig.add_trace(go.Scatter(x=df.index, y=df["TempSuccion"],
    #                          line=dict(color='#d62728', width=1.5),
    #                          mode='lines',  # 'lines+markers'
    #                          name='Temp Succión',
    #                          yaxis="y1",
    #                          ),
    #               row=1, col=1)

    # Ventilador ON/OFF
    fig = plot_on_off(fig, df, "VentInyec", "Ventilador ON", 'rgba(55,126,184,0.2)')

    # Extractores
    fig = plot_on_off(fig, df, "Extrac1", "Extractor1 ON", 'rgba(255, 127, 14,0.2)')
    fig = plot_on_off(fig, df, "Extrac2", "Extractor2 ON", 'rgba(228,26,28,0.2)')
    fig = plot_on_off(fig, df, "Extrac3", "Extractor3 ON", 'rgba(102,17,0,0.3)')
    fig = plot_on_off(fig, df, "Extrac4", "Extractor4 ON", 'rgba(23, 190, 207,0.2)')
    fig = plot_on_off(fig, df, "Extrac5", "Extractor5 ON", 'rgba(188, 189, 34,0.2)')
    fig = plot_on_off(fig, df, "Extrac6", "Extractor6 ON", 'rgba(148, 103, 189,0.2)')
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Temp Zona1
    fig.add_trace(go.Scatter(x=df.index, y=df["TempZ1"],
                             line=dict(color='#1616a7', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp Zona1',
                             yaxis="y3", visible="legendonly"
                             ),
                  row=2, col=1)

    # HR Zona1
    fig.add_trace(go.Scatter(x=df.index, y=df["HumZ1"],
                             line=dict(color='#1616a7', width=1, dash='dot'),
                             mode='lines', name='HR Zona1',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # Humedad absoluta Z1
    fig.add_trace(go.Scatter(x=df.index, y=df["WZ1"],
                             line=dict(color='#1616a7', width=2, dash='dash'),
                             mode='lines', name='Humedad Abs Z1',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # Temp Zona2
    fig.add_trace(go.Scatter(x=df.index, y=df["TempZ2"],
                             line=dict(color='#d62728', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp Zona2',
                             yaxis="y3", visible="legendonly"
                             ),
                  secondary_y=False, row=2, col=1)

    # HR Zona2
    fig.add_trace(go.Scatter(x=df.index, y=df["HumZ2"],
                             line=dict(color='#d62728', width=1, dash='dot'),
                             mode='lines', name='HR Zona2',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # Humedad absoluta Z2
    fig.add_trace(go.Scatter(x=df.index, y=df["WZ2"],
                             line=dict(color='#d62728', width=2, dash='dash'),
                             mode='lines', name='Humedad Abs Z2',
                             yaxis="y4", visible="legendonly"
                             ),
                  secondary_y=True, row=2, col=1)

    # TempProm
    fig.add_trace(go.Scatter(x=df.index, y=df["TempProm"],
                             line=dict(color='#3366cc', width=1.5),  # dash='dash'),
                             mode='lines', name='Temp Promedio',
                             yaxis="y3"
                             ),
                  secondary_y=False, row=2, col=1)

    # HR Prom
    fig.add_trace(go.Scatter(x=df.index, y=(df["HumZ1"] + df["HumZ2"])/2,
                             line=dict(color='#3366cc', width=1, dash='dot'),
                             mode='lines', name='HR Promedio',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # HA Prom
    fig.add_trace(go.Scatter(x=df.index, y=(df["WZ1"] + df["WZ2"])/2,
                             line=dict(color='#3366cc', width=1, dash='dash'),
                             mode='lines', name='HA Promedio',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)


    # Set Point temperatura
    fig.add_trace(go.Scatter(x=df.index, y=df["SPTemp"],
                             line=dict(color='#7f7f7f', width=2),  # dash='dash'),
                             mode='lines', name='Set Point Temp',
                             yaxis="y3",
                             ),
                  secondary_y=False, row=2, col=1)

    # Set Point humedad
    fig.add_trace(go.Scatter(x=df.index, y=df["SPHum"],
                             line=dict(color='#7f7f7f', width=2, dash='dot'),
                             mode='lines', name='Set Point HR',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # Set Point humedad Absoluta
    fig.add_trace(go.Scatter(x=df.index, y=df["SPW"],
                             line=dict(color='#7f7f7f', width=2, dash='dash'),
                             mode='lines', name='Set Point HA',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)


    # Compuerta Succión
    fig = plot_on_off(fig, df, "PosComp", "Compuerta", 'rgba(255,127,0,0.3)', axis_y="y4", r=2, c=1)

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    # Set x-axis and y-axis title
    fig.update_layout(legend_title_text='Variables Salón CDI')
    fig['layout']['xaxis2']['title'] = 'Fecha'

    fig['layout']['yaxis']['title'] = 'Temperaturas Entrada °C'

    fig['layout']['yaxis2']['title'] = 'Estado ON/OFF'
    fig['layout']['yaxis2']['range'] = [0, 2]
    fig['layout']['yaxis2']['fixedrange'] = True

    fig['layout']['yaxis3']['title'] = 'Temperaturas Salon CDI °C'
    fig['layout']['yaxis3']['range'] = [20, 35]
    fig['layout']['yaxis3']['fixedrange'] = True

    fig['layout']['yaxis4']['title'] = 'Apertura Compuerta, HR y HA %'
    fig['layout']['yaxis4']['range'] = [0, 100]

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    return fig