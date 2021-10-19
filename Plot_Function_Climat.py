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
    # fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": False}], [{"secondary_y": True}]])
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

    # TempInyecsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecsalon3"],
                             line=dict( width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny S3'),
                  secondary_y=False, row=1, col=1)

    # TempInyecquemsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecquemsalon3"],
                             line=dict( width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny Quemador S3'),
                  secondary_y=False, row=1, col=1)

    # S3 temptac
    fig.add_trace(go.Scatter(x=df.index, y=df["S3temptac"],
                             line=dict(color='#9467bd', width=1), # dash='dash'),
                             mode='lines', name='Temp TZ AC'),
                  secondary_y=False, row=2, col=1)

    # S3 humedad tac
    fig.add_trace(go.Scatter(x=df.index, y=df["S3humtac"],
                             line=dict(color='#9467bd', width=0.5, dash='dash'),
                             mode='lines', name='HR TZ AC'),
                  secondary_y=True, row=2, col=1)

    # S3temppmax
    fig.add_trace(go.Scatter(x=df.index, y=df["S3temppmax"],
                             line=dict(color='#d62728', width=1), # dash='dash'),
                             mode='lines', name='Temp Power Max'),
                  secondary_y=False, row=2, col=1)

    # S3 humedad power max
    fig.add_trace(go.Scatter(x=df.index, y=df["S3humpmax"],
                             line=dict(color='#d62728', width=0.5, dash='dash'),
                             mode='lines', name='HR Power Max'),
                  secondary_y=True, row=2, col=1)

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white

    # Set x-axis and y-axis title
    # fig.update_xaxes(title = "xaxis title")
    fig['layout']['xaxis2']['title'] = 'Fecha'
    fig['layout']['yaxis']['title'] = 'Temperaturas Entrada °C'
    #fig['layout']['yaxis2']['title'] = 'Temperaturas  Salones °C'
    fig['layout']['yaxis2']['title'] = 'Temperaturas Salon 3 °C'

    fig.update_yaxes(title_text="Humedad Relativa %", secondary_y=True)

    # fig['layout']['yaxis2']['title']='HR'

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    #fig.show()

    return fig


#@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True)
def plot_html_CBC_BDT(df, title):
    # Create figure with secondary y-axis
    # fig = make_subplots(rows=2, cols=1, specs=[[{"secondary_y": False}], [{"secondary_y": True}]])
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

    # TempInyecsalon3
    fig.add_trace(go.Scatter(x=df.index, y=df["TempInyecbdtcbc"],
                             line=dict( width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Iny CBC/BDT'),
                  secondary_y=False, row=1, col=1)

    # S3 temptac
    fig.add_trace(go.Scatter(x=df.index, y=df["Temppasillo1"],
                             line=dict(color='#9467bd', width=1), # dash='dash'),
                             mode='lines', name='Temp Pasillo'),
                  secondary_y=False, row=2, col=1)

    # S3 humedad tac
    fig.add_trace(go.Scatter(x=df.index, y=df["Temppasillo2"],
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
    #fig['layout']['yaxis2']['title'] = 'Temperaturas  Salones °C'
    fig['layout']['yaxis2']['title'] = 'Temperaturas Salon CBC/BDT °C'

    fig.update_yaxes(title_text="Humedad Relativa %", secondary_y=True)

    # fig['layout']['yaxis2']['title']='HR'

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    #fig.show()

    return fig