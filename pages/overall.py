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


def get_overall_graph_activities(activity):
    overall_activities = get_overall_activities(activity)
    return dcc.Graph(
        figure={
            'data': [
                {'x': overall_activities["name"], 'y': overall_activities["PerformanceDuration"],
                 'type': 'bar', 'textposition':'inside', 'textfont':{'color':'#fff'},'text': overall_activities["PerformanceDuration"], 'name': "PerformanceDuration", 'marker': {"color": "#EF553B"}},
                {'x': overall_activities["name"], 'y': overall_activities["AverageDuration"],
                 'type': 'bar', 'textposition':'inside','textfont':{'color':'#fff'}, 'text':overall_activities["AverageDuration"], 'name': "AverageDuration", 'marker': {"color": "#636EFA"}},
            ],
            'layout': {
                'xaxis': {
                    'title': 'Name'
                },
                'yaxis': {
                    'title': 'Duration in Minutes'
                },
                'plot_bgcolor': '#14142b',
                'paper_bgcolor': '#14142b',
                'border-radius': '10px',
                'font': {
                    'color': 'white'
                }

            }
        }
    )


def get_overall_graph_properties(properties):
    overall_properties = get_overall_properties(properties)
    return dcc.Graph(
        figure={
            'data': [
                {'x': overall_properties["prop"], 'y': overall_properties["PerformanceDuration"],
                 'type': 'bar',  'textposition':'inside','textfont':{'color':'#fff'}, 'text': overall_properties["PerformanceDuration"], 'name': "PerformanceDuration", 'marker': {"color": "#EF553B"}},
                {'x': overall_properties["prop"], 'y': overall_properties["AverageDuration"],
                 'type': 'bar', 'textposition':'inside', 'textfont':{'color':'#fff'},'text':overall_properties["AverageDuration"], 'name': "AverageDuration", 'marker': {"color": "#636EFA"}},
            ],
            'layout': {
                'xaxis': {
                    'title': properties
                },
                'yaxis': {
                    'title': 'Duration in Minutes'
                },
                'plot_bgcolor': '#14142b',
                'paper_bgcolor': '#14142b',
                'border-radius': '10px',
                'font': {
                    'color': 'white'
                }
            }
        }
    )



layout = html.Div(id="overall", children=[
    dcc.Dropdown(id="overall_activity", style={"display": "none"}),
    dcc.Dropdown(id="overall_emp_properties", style={"display": "none"})])

@app.callback(Output('overall', 'children'), 
              Input('overall_activity', 'value'), 
              Input('overall_emp_properties', 'value'))
def overall(activity, properties):
    activities = sorted(
        set(time_distribution.iloc[i][time_distribution.columns[1]] for i in range(len(time_distribution))))
    prop = emp_details.columns[1:-3]
    if activity == None or properties == None:
        activity = activities[0]
        properties = prop[0]
    activity = str(activity)
    properties = str(properties)

    leaderboard = get_leaderboard()
    return [html.Div(className='overall-layout', children=[


        html.Div(style={'border-radius': '10px'}, className='grid-col-span-2', children=[html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'background-color': '#14142b', 'border-radius': '10px'}, children=[html.P("Timing Distribution", style={
            'font-size': '1.5rem',
            'margin-left': '1.5rem',
            'margin-top': '1rem',
            'color': '#fff'}), dcc.Dropdown(id="overall_activity",  options=activities, value=activity, clearable=False,  style={
                'background-color': '#14142b',
                'width': '20rem',
                'border': 'none',
                "color": "black",
                'margin-right': '0',

            })]),
            get_overall_graph_activities(activity),

        ]),

        html.Div(style={'display': 'flex', 'background-color': '#14142b', 'border-radius': '10px'}, children=[
            html.Div(style={'width': '100%'}, children=[html.Div(style={'display': 'flex', 'justify-content': 'space-between'},
                                                                 children=[html.P("Metric Productivity Distribution", style={
                                                                     'font-size': '1.5rem',
                                                                     'margin-left': '1.5rem',
                                                                     'margin-top': '1rem',
                                                                     'color': '#fff'}),
                dcc.Dropdown(id="overall_emp_properties", clearable=False,  style={
                    'background-color': '#14142b',
                    'width': '20rem',
                    'border': 'none',
                    "color": "black",
                    'margin-right': '0',
                    'font': {
                        'color': '#fff'
                    }
                },
                options=prop, value=properties)]),
                get_overall_graph_properties(properties),
            ]),


        ]),
        html.Div(style={'color': '#fff', 'background-color': '#14142b', 'border-radius': '10px'}, children=[
            html.P(" Metric Laderboard", style={
                'font-size': '1.5rem',
                'margin-left': '3rem',
                'margin-top': '1rem',
                'margin-bottom': '2rem',
            }),

            html.Table(className='table-head',
                       children=[
                           html.Tr([
                               html.Th("ACTIVITY", style={'padding-right': '7rem',
                                                          'padding-left': '3rem'}),
                               html.Th("MOST PERFORMANCE", style={
                                       'padding-right': '5rem'}),
                               html.Th("LEAST PERFORMANCE", style={}),
                           ])
                       ]),

            html.Table(children=[
                html.Tr(children=[
                    html.Td(i, style={'padding-left': '4rem',
                                      'padding-right': '10rem',
                                      'padding-bottom': '1rem'
                                      }),
                    html.Td(str(leaderboard[i][0]), style={
                        'padding-right': '13rem',
                        'padding-bottom': '1rem'}),
                    html.Td(str(leaderboard[i][1])),
                ])for i in leaderboard
            ])
        ])
        # html.Div(style={'color':'#fff','background-color':'#14142b'},children=[i+" "+str(leaderboard[i][0]) +
        #                                " ->"+str(leaderboard[i][1]) for i in leaderboard])
    ])
    ]


