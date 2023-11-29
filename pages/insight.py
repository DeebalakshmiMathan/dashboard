from calendar import day_abbr
import pathlib
import dash
from dash import dcc
from dash import html
from datetime import date, datetime, timedelta
from dash.dependencies import Input, Output
from matplotlib.pyplot import title
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
from app import app
from server.server import *


bar_colors = ['#636efa', '#ef553b', '#00cc96']
colors = {
    'background': '#14142B', 'text': "#5A5A89"
}




def get_insight_graph(emp_name):
    if emp_name == 'Overall':
        title_name="Overall Technician Report"
    else:
        title_name = emp_name
    data = get_insight_data(emp_name)
   
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=("Pre-Lunch 1", "Post-Lunch", "Full-Day", ))
    fig.add_trace(row=1, col=1,
                  trace=go.Bar(x=["idel Duration", "During Service", "Total Unutilized"],
                               y=[data["Pre-lunch"][0], data["Pre-lunch"]
                                  [1], sum(data["Pre-lunch"])],
                               showlegend=False,
                               marker_color=bar_colors,
                               textfont={'color':'#fff'},
                               textposition='inside', text=[data["Pre-lunch"][0], data["Pre-lunch"][1], sum(data["Pre-lunch"])]
                               ))
    fig.add_trace(row=1, col=2,
                  trace=go.Bar(x=["idel Duration", "During Service", "Total Unutilized"],
                               y=[data["Post-Lunch"][0], data["Post-Lunch"]
                                  [1], sum(data["Post-Lunch"])],
                               showlegend=False,
                               marker_color=bar_colors,
                               textfont={'color':'#fff'},
                               textposition='inside', text=[data["Post-Lunch"][0], data["Post-Lunch"][1], sum(data["Post-Lunch"])]))
    fig.add_trace(row=1, col=3,
                  trace=go.Bar(x=["idel Duration", "During Service", "Total Unutilized"],
                               y=[data["Pre-lunch"][0]+data["Post-Lunch"][0], data["Pre-lunch"][1] +
                                  data["Post-Lunch"][1], sum(data["Pre-lunch"])+sum(data["Post-Lunch"])],
                               marker_color=bar_colors,
                               textfont={'color':'#fff'},
                               showlegend=False,
                               textposition='inside', text=[data["Pre-lunch"][0]+data["Post-Lunch"][0], data["Pre-lunch"][1]+data["Post-Lunch"][1], sum(data["Pre-lunch"])+sum(data["Post-Lunch"])]))
    fig.update_traces(textposition='auto')
    fig.update_xaxes(tickangle=-45)
    fig.update_yaxes(
        range=[-100, sum(data["Pre-lunch"])+sum(data["Post-Lunch"])+100])
    # fig =insight_graph_data(rows=1, cols=3,
    #     subplot_titles=("Pre-Lunch", "Post-Lunch", "Full-Day"),
    #     y_title= "Duration (mins.)"
    # )
    fig.update_layout(
        title_text=str(title_name),
        uniformtext_minsize=8,
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            color="#ffffff"
        ),
    )

    return dcc.Graph(figure=fig)


layout = html.Div(id='insight', children=[
    dcc.Dropdown(id="insight-emp-name", style={"display": "none"}),])

@app.callback(Output('insight', 'children'),
              Input('insight-emp-name', 'value'))
def insight(emp_name):
    employies_name = sorted(set(map(
        str, [insight_graph_data.iloc[i]['Name'] for i in range(len(insight_graph_data))])))
    employies_name.append("Overall")
        
    if emp_name == None:
        emp_name = str(employies_name[0])
    data = get_insight_data(emp_name)
    return [html.Div(className='insight-layout', children=[
        html.Div(children=[
            html.Div([
                 html.Div([
                     html.H1("Total Unutilized time"),
                     html.Div(convert_mins(sum(data["Pre-lunch"])+sum(data["Post-Lunch"])),
                              id="total-unutilized-value")
                 ], className="total-unutilized-container",),
                 html.Div([
                     html.Div("Within service"),
                     html.Div(convert_mins(data["Pre-lunch"][1]+data["Post-Lunch"][1]),
                              id="within-service-value")
                 ], className="within-service-container"),
                 html.Div([
                     html.Div("Idle duration"),
                     html.Div(convert_mins(data["Pre-lunch"][0]+data["Post-Lunch"][0]),
                              id="idle-duration-value")
                 ], className="idle-duration-container"),
                 html.Div(["Unutilized Time = Within service + Idle Duration"],
                          className="unutilized-formula")
                 ], className="unutilized-main-container"),
            html.Div([
                html.Div("Un-utilized time (%)"),
                html.Div(mins_to_perst(sum(data["Pre-lunch"])+sum(data["Post-Lunch"]))+" %"),
            ], className="unutilized-time-container"),
            html.Div(["Unutilized Time (%)= Total Unutilized time/ 8 hours"],
                     className="unutilized-percentage-formula"),
            html.Div([
                html.Div("Potential loss incurred"),
                html.Div("Rs. " + potential_loss(data),
                         id="potential-loss-value")
            ], className="potential-loss-container"),
            html.Div([
                html.Div("Unproductive Half"),
                html.Div(overall_unprod_half(data),
                         id="unproductive-half-value")
            ], className="unproductive-half-container"),
        ], className="parent-div", style={"fontWeight": "bold"}),
        html.Div(className='graph-container', children=[
            dcc.Dropdown(id='insight-emp-name', options=employies_name, value=emp_name, style={
                 'width': '30rem'
                 }),

            get_insight_graph(emp_name)
        ])
    ])]
