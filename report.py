from dash import Dash, dcc, html, Input, Output
import pandas as pd


app = Dash(__name__)

df = pd.read_csv("pokeymon.csv")
test = df['Name'].unique()
options = [{'label': t, 'value': t} for t in test]

technician = html.Div([
    html.Div("Technician information "),
    html.Div("Timing Distribution"),
    html.Div("Micro-Activity Distribution "),
    html.Div("Activity efficiancy Distribution "),
    html.Div("potential earning/ loss "),
])



app.layout=html.Div(children=[
    dcc.Dropdown(options=options,id="dropdown", searchable=False),
    html.Div(id="parent",style={'background-color':'blue'})     
])

@app.callback(
    Output("parent",'children'),
    Input("dropdown",'value')
)




def update_dropdown(value):
    return html.Div(children=[
     technician,value
    ])

if __name__ == '__main__':
    app.run_server(debug=True)