from turtle import color
import dash
from dash import html,dcc,Output,Input
from datetime import date, datetime, timedelta

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from pages import overview,overall,report,insight


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
   
    html.Div([
         html.H1("Maruti Analytics Dashboard",),
        dcc.Link('OVERVIEW', href='/pages/overview'),
        dcc.Link('REPORT', href='/pages/report'),
        dcc.Link('OVERALL', href='/pages/overall'),
        dcc.Link('INSIGHTS', href='/pages/insight'),
    ],className="nav-link"),
     html.Div(className="title-bar",
             children=[
                 html.P("welcome"),
                 html.Div(className='btn-group',
                          children=[
                              dcc.DatePickerSingle(

                                  className='button',
                                  id='my-date-picker-single',
                                  min_date_allowed=date(
                                      1995, 8, 5),
                                  max_date_allowed=date(
                                      2025, 9, 19),
                                  initial_visible_month=date(
                                      2017, 8, 5),
                                  date=date(2022, 2, 16)
                              ),
                              html.Button(
                                  'Week', id='week'),
                          ])

             ]),
    
    html.Div(id='page-content', children=[],style={'background-color':'#05050F',
                                                   'height':'100%'})
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/overview':
        return overview.layout
    if pathname == '/pages/report':
        return report.layout
    if pathname == '/pages/overall':
        return overall.layout
    if pathname == '/pages/insight':
        return insight.layout
    else:
        return overview.layout


if __name__ == '__main__':
    app.run_server(debug=True)