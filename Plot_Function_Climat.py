# Python File function for streamlit tools
# Sales Baños y Cocna
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


# ----------------------------------------------------------------------------------------------------------------------
#@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True)
def plot_html_Salon3(df, title):
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1,  specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
                        shared_xaxes=True, vertical_spacing=0.02,
                        #subplot_titles=('Temperaturas Entradas',  'Temperatura y humedad Salon 3')
                        )

    # Temp Ware House
    fig.add_trace(go.Scatter(x=df.index, y=df["Tempwh"],
                             line=dict(width=1), # dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='Temp WH',
                             yaxis="y1",
                             ),
                  row=1, col=1,)

    # TempInyecsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecsalon3"],
                             line=dict( width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny S3',
                             yaxis="y1",
                             ),
                  row=1, col=1)

    # TempInyecquemsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecquemsalon3"],
                             line=dict( width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny Quemador S3',
                             yaxis="y1",
                             ),
                  row=1, col=1)

    # QS3 barrido
    fig.add_trace(go.Scatter(x=df.index, y=df["QS3barrido"],
                             line=dict(width=1, dash='dash'),
                             mode='lines', name='Quemador Barrido S3',
                             visible='legendonly',
                             yaxis="y2",
                             ),
                  secondary_y=True, row=1, col=1)

    # QS3 ON/OFF
    fig.add_trace(go.Scatter(x=df.index, y=df["QS3On"],
                             line=dict(width=1, dash='dash'),
                             mode='lines', name='Quemador ON/OFF S3',
                             visible='legendonly',
                             yaxis="y2",
                             ),
                  secondary_y=True, row=1, col=1)

    # QS3 Falla
    fig.add_trace(go.Scatter(x=df.index, y=df["QS3Falla"],
                             line=dict(width=1, dash='dash'),
                             mode='lines', name='Quemador Falla S3',
                             visible='legendonly',
                             yaxis="y2",
                             ),
                  secondary_y=True, row=1, col=1)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # S3 temptac
    fig.add_trace(go.Scatter(x=df.index, y=df["S3temptac"],
                             line=dict(color='#9467bd', width=1), # dash='dash'),
                             mode='lines', name='Temp TZ AC',
                             yaxis="y3",
                             ),
                  row=2, col=1)

    # S3 humedad tac
    fig.add_trace(go.Scatter(x=df.index, y=df["S3humtac"],
                             line=dict(color='#9467bd', width=0.5, dash='dash'),
                             mode='lines', name='HR TZ AC',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # S3temppmax
    fig.add_trace(go.Scatter(x=df.index, y=df["S3temppmax"],
                             line=dict(color='#d62728', width=1), # dash='dash'),
                             mode='lines', name='Temp Power Max',
                             yaxis="y3",
                             ),
                  secondary_y=False, row=2, col=1)

    # S3 humedad power max
    fig.add_trace(go.Scatter(x=df.index, y=df["S3humpmax"],
                             line=dict(color='#d62728', width=0.5, dash='dash'),
                             mode='lines', name='HR Power Max',
                             yaxis="y4",
                             ),
                  secondary_y=True, row=2, col=1)

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white

    # Set x-axis and y-axis title
    # fig.update_xaxes(title = "xaxis title")
    fig.update_layout(legend_title_text='Variables')
    fig['layout']['xaxis2']['title'] = 'Fecha'
    fig['layout']['yaxis']['title'] = 'Temperaturas Entrada °C'
    fig['layout']['yaxis2']['title'] = 'Estado Quemador'
    fig['layout']['yaxis3']['title'] = 'Temperaturas Salon 3 °C'
    fig['layout']['yaxis4']['title'] = 'Humedad Relativa %'

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')


    return fig


#@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True)
def plot_html_CBC_BDT(df, title):
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1,  specs=[[{"secondary_y": False}], [{"secondary_y": True}]],
                        shared_xaxes=True, vertical_spacing=0.02,
                        #subplot_titles=('Temperaturas Entradas',  'Temperatura y humedad Salon 3')
                        )

    # Temp Ware House
    fig.add_trace(go.Scatter(x=df.index, y=df["Tempwh"],
                             line=dict(width=1), # dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='Temp WH'),
                  row=1, col=1,
                  secondary_y=False,
                  )

    # TempInyec bdt/cbc
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecbdtcbc"],
                             line=dict( width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny CBC/BDT'),
                  secondary_y=False, row=1, col=1)

    # Temp pasillo
    fig.add_trace(go.Scatter(x=df.index, y=df["Temppasillo"],
                             line=dict(color='#9467bd', width=1), # dash='dash'),
                             mode='lines', name='Temp Pasillo'),
                  secondary_y=False, row=2, col=1)

    # Humedad pasillo
    fig.add_trace(go.Scatter(x=df.index, y=df["Humpasillo"],
                             line=dict(color='#9467bd', width=0.5, dash='dash'),
                             mode='lines', name='HR pasillo'),
                  secondary_y=True, row=2, col=1)

    # TODO: agregar las temperaturas que falta, estas deben de agregarse primero a la base de datos

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white

    # Set x-axis and y-axis title
    # fig.update_xaxes(title = "xaxis title")
    fig['layout']['xaxis2']['title'] = 'Fecha'
    fig['layout']['yaxis']['title'] = 'Temperaturas Entrada °C'
    fig['layout']['yaxis2']['title'] = 'Temperaturas Salon CBC/BDT °C'

    fig.update_yaxes(title_text="Humedad Relativa %", secondary_y=True)

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    return fig