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


def get_report_emp_activity_graph(emp_name, activity_type, work_time):
        activities_graph = get_emp_activity_graph(
            emp_name, activity_type, work_time)
        return dcc.Graph(
            figure={
                'data': [
                    {'x': [1], 'y': [activities_graph[0]], 'text':[activities_graph[0]],'textposition':'inside',
                     'textfont':{'color':'#fff'},
                     'type': 'bar', 'name': 'Performed Duration', 'marker': {"color": "#EF553B"}},
                    {'x': [1], 'y': [activities_graph[1]],'text':[activities_graph[1]],'textposition':'inside',
                     'textfont':{'color':'#fff'},
                     'type': 'bar', 'name': 'Benchmark Duration', 'marker': {"color": "#636EFA"}},
                ],
                'layout': {
                    'xaxis': {
                        'title': 'ACtivity No. 1'
                    },
                    'yaxis': {
                        'title': 'Duration in Minutes'
                    },
                    'plot_bgcolor': '#14142b',
                    'paper_bgcolor': '#14142b',
                    'border-radius': '10px',
                    'font': {
                        'color': '#fff'
                    }

                }
            }
        )



layout =  html.Div(id="report", children=[
    dcc.Dropdown(id="report_emp_name", style={"display": "none"}),
    dcc.Dropdown(id="report_emp_activity", style={"display": "none"}),
    dcc.Dropdown(id="report_emp_work_time", style={"display": "none"})]
)

@app.callback(Output('report', 'children'),
Input('report_emp_name', 'value'), Input('my-date-picker-single', 'date'), Input('report_emp_activity', 'value'), Input('report_emp_work_time', 'value'),)


def report(emp_name, date, activity_type, work_time):
    if emp_name == None:
        return [html.Div(children=[html.Div("Select an employee for "+date, style={"color": "white", "display": "block"}),
                                   dcc.Dropdown(id="report_emp_activity", clearable=False,  style={
                                                "display": "none"}),
                                   dcc.Dropdown(clearable=False,
                                                id="report_emp_work_time", style={"display": "none"}),
                                   dcc.Dropdown(clearable=False, options=emp_details["Name"], id="report_emp_name", style={
                                       'background-color': '#05050f',
                                       'width': '20rem',
                                       'border': 'none',


                                   })], style={
            'display': 'flex',
            'align-items': 'center',
            "flex-direction": "column",
            'justify-content': 'center',
            'background-color': '#05050f',
            'height': '50rem', })]
    emp_data = get_emp_data(emp_name, emp_details)
    activities = get_emp_activity(emp_name)
    activities2 = get_emp_activity2(emp_name)
    if not activity_type:
        activity_type = activities[0]
    if not work_time:
        work_time = activities2[0]
    # activities_graph = get_emp_activity_graph(
    #     emp_name, activity_type, work_time)
    microactivity = get_micro_activities(emp_name, activity_type, work_time)
    activity_eff = get_activity_efficiency(emp_name)

    return html.Div(className='report', children=[
        dcc.Dropdown(options=[emp_name], value=emp_name, clearable=False,
                     id="report_emp_name", style={"display": "none"}),
        html.Div(children=[
            html.Div(children=[html.Div(style={'display': 'grid',
                                               'grid-template-columns': '1fr 1fr '}, className='emp-name', children=[
                html.Div(children=[html.Img(src=emp_data["Image"], style={
                         "height": "100px", "width": "100px", "border-radius": "50px", 'margin-left': '10rem'}),
                ]),
                html.Div(children=[html.Div(emp_name), html.Br(),
                                   html.Div(emp_data["Age"])])

            ]),
                html.Div(children=[
                    html.Div(children=[html.Div(emp_data["Weight"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Weight")], className='employee_data'),
                    html.Div(children=[html.Div(emp_data["Height"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Height")], className='employee_data'),
                    html.Div(children=[html.Div(emp_data["Certification"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Certification")], className='employee_data'),
                    html.Div(children=[html.Div(emp_data["Trainings"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Trainings")], className='employee_data'),
                    html.Div(children=[html.Div(emp_data["Expriance"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Expriance")], className='employee_data'),
                    html.Div(children=[html.Div(emp_data["Location"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Location")], className='employee_data'),
                    html.Div(children=[html.Div(emp_data["Phone Number"], style={
                             'color': '#fff', 'padding-bottom': '5px'}), html.Div("Phone Number")], className='employee_data'),
                ], className='emp-details')])


        ], className="container-data"),
        html.Div(children=[html.P("Timing Distribution", style={
            'font-size': '1.5rem',
            'margin-left': '1.5rem',
            'margin-top': '1rem',
        }),
            html.Div(id="report_distribution_graph", children=[html.Div(style={'display': 'flex', 'flex-direction': 'row-reverse'}, children=[
                dcc.Dropdown(id="report_emp_work_time", style={
                    'background-color': '#14142b',
                    'width': '10rem',
                    'border': 'none',
                    "color": "black",
                    'border-bottom': '1px solid #5A5A89',
                }, clearable=False,  options=activities2, value=work_time),
                dcc.Dropdown(id="report_emp_activity", style={
                    'background-color': '#14142b',
                    'width': '20rem',
                    'border': 'none',
                    "color": "black",
                    'border-bottom': '1px solid #5A5A89',
                    'margin-right': '1rem',


                }, options=activities, value=activity_type)
            ]),
                get_report_emp_activity_graph(
                    emp_name, activity_type, work_time)

            ]
        )], className="container-data grid-col-span-2"),

        html.Div(className="container-data", children=[
            html.P(" Micro-Activity Distribution", style={
                'font-size': '1.5rem',
                'margin-left': '3rem',
                'margin-top': '1rem',
                'margin-bottom': '1rem',
            }),
            html.Table(className='table-head',
                       children=[
                           html.Tr([
                               html.Th("ACTIVITY", style={'width': '200px' }),
                               html.Th("COMPILANCE", style={
                                       'width': '200px' }),
                               html.Th("AVERAGE DURATION", style={
                                       'width': '200px' }),
                           ])
                       ]),
            html.Table([
                # Body
                html.Tr(children=[
                    html.Td(i[0], style={'width': '300px',
                                         'padding':'1rem'
                                         }),
                    html.Td(i[1], style={'width': '300px',
                                         'padding':'1rem'
                                         }),
                    html.Td(i[2], style={'width': '500px' ,
                                         'padding':'1rem'      
                                         })
                ])for i in microactivity],className='table-row',
            )
        ]),
        html.Div(className="container-data", children=[
            html.P(" Activity Efficiency Distribution", style={
                'font-size': '1.5rem',
                'margin-left': '3rem',
                'margin-top': '1rem',
                'margin-bottom': '2rem',
            }),
            html.Table(className='table-head',
                       children=[
                           html.Tr([
                               html.Th("ACTIVITY", style={'padding-right': '8rem',
                                                          'padding-left': '3rem'}),
                               html.Th("EFFICIENCY", style={
                                       'padding-right': '5rem'}),
                           ])
                       ]),
            html.Table([
                # Body
                html.Tr(children=[
                    html.Td(activity_eff[0], style={'padding-left': '3rem',
                                                    'padding-right': '3rem',
                                                    'padding-bottom': '2rem'}),
                    html.Td(str(activity_eff[1])+"%", style={'padding-right': '3rem',
                                                             'padding-bottom': '2rem'
                                                             }),

                ])]
            )
        ]),

        html.Div(className="container-data",
                 children=[html.P(" Potential Earning/Loss", style={
                     'font-size': '1.5rem',
                     'margin-left': '3rem',
                     'margin-top': '1rem',
                     'margin-bottom': '2rem',
                 }),
                     html.Div("₹ "+report_potential_earning(emp_name), style={'display': 'flex',
                                                                              'align-items': 'center',
                                                                              'justify-content': 'center',
                                                                              'height': '50%',
                                                                              'font-size': '2rem'})
                 ])
    ]
    )

