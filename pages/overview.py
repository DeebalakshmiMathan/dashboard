from calendar import day_abbr
import dash
from dash import dcc
from dash import html
from datetime import date, datetime, timedelta
from dash.dependencies import Input, Output
from matplotlib.pyplot import title
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app
from server.server import *

def generate_table(date, week, max_rows=10):
    if week:
        data = generate_table_week_data(date, max_rows)
    else:
        data = generate_table_data( date, max_rows)
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={'padding-right': '3rem',
                                      'padding-bottom': '1rem',
                                      'font-weight': '800',
                                      'font-size': '1.2rem'}) for col in df.columns[1:]], className="table-head")] +
        # Body
        [html.Tr([
            html.Td(col, style={'padding-right': '1rem',
                                'padding-bottom': '1rem',
                                'padding-left': '1rem'}) for col in i
        ], className='table-row') for i in data]
    )



def displayActivityDistribution( date, week):
    data = displayActivityDistribution_Data(date, week)
    fig = go.Figure(
        data=[go.Pie(labels=data[0], values=data[1], hole=.5)],
        layout=go.Layout(
            paper_bgcolor='#14142B',
            font_color="#fff",
        )
    )
    return dcc.Graph(id='pie-graph',
                     figure=fig)

layout = html.Div(id="overview")
@app.callback(Output('overview', 'children'),
              Input('my-date-picker-single', 'date'), Input('week', 'n_clicks'))
def overview(date, week):
    week = "week" in [p['prop_id'] for p in dash.callback_context.triggered][0]
    return html.Div(className="page", children=[
        html.Div(className="top-container", children=[
            html.Div(className='top-row', children=[
                html.Div(className='summary', children=[
                    html.P(" Summary",
                           style={
                               'font-size': '1.5rem',
                               'margin-left': '1.5rem',
                               'margin-top': '1rem',
                               'margin-bottom': '1rem'
                           }),
                    html.Table(style={
                        'font-size': '1.3rem',
                        'margin-left': '1.5rem',
                        'margin-top': '1.5rem',

                    },
                        children=[
                        html.Tr(style={
                            'padding': '.5rem',
                            'margin-bottom': '1rem'
                        }, children=[
                            html.Td("Compilance", style={
                                'padding': '.5rem',
                            }),
                            html.Td(summaryCompilance(date, week), style={
                                'padding': '.5rem',
                            })
                        ]),
                        html.Tr(style={
                            'margin-bottom': '1rem',
                            'padding': '.5rem'
                        }, children=[
                            html.Td("Fast/Slow", style={
                                'padding': '.5rem',
                            }),
                            html.Td(summarySpeed(summary, date, week), style={
                                'padding': '.5rem',
                            })
                        ]),
                    ])
                ]),
                html.Div(id="top-performer", children=[
                    html.P(f" Top Performers", style={
                        'font-size': '1.5rem',
                        'margin-left': '1.5rem',
                        'margin-top': '1rem',
                    }),
                    html.Div(generate_table( date, week), style={'margin-left': '1.5rem',
                                                                    'margin-top': '1rem',
                                                                    'margin-right': '1rem',
                                                                    'overflowY': 'auto',
                                                                    'height': '10rem'
                                                                    })
                    #  html.Div(display_table())
                ]),
                html.Div(children=[
                    html.P(" Worst Performers", style={
                        'font-size': '1.5rem',
                        'margin-left': '1.5rem',
                        'margin-top': '1rem',
                    }),

                    html.Div(generate_table( date, week), style={'margin-left': '1.5rem',
                                                                    'margin-top': '1rem',
                                                                    'overflowY': 'auto',
                                                                    'height': '10rem'})
                ])])
        ]),
        html.Div(className="bottom-container", children=[
            html.Div(children=[
                html.P(" Potential Earning/Loss", style={
                    'font-size': '1.5rem',
                    'margin-left': '1.5rem',
                    'margin-top': '1rem',
                    'margin-bottom': '1rem'
                }),
                html.P("Potential Earnings = (Time taken by trainer - Time Taken by Technician) X Rs 650/hour",
                       style={
                           'font-size': '1.1rem',
                           'margin-left': '1.5rem',
                           'margin-top': '2rem',
                           'margin-bottom': '1rem'
                       }),
                html.P(display_Earning(date, week),
                       style={
                    'font-size': '2rem',
                    'text-align': 'center',
                    'margin-top': '3rem',
                    'margin-bottom': '1rem'
                })]),
            html.Div(children=[
                html.P(" Activity Distibution", style={
                    'font-size': '1.5rem',
                    'margin-left': '1.5rem',
                    'margin-top': '1rem',
                    'margin-bottom': '1rem'
                }),

                displayActivityDistribution(date, week)

            ])
        ])
    ]
    )




