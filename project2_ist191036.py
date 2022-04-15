# -*- coding: utf-8 -*-
"""
Project 2 - Catarina Neves - 91036
07-04-22
@author: catarina
@herokuapp : dash-app91036.herokuapp.com
"""

import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

#dashboard style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#import files
df_pred_2019 = pd.read_csv('predictions.csv')
df_tab = pd.read_csv('metrics.csv')
df_graph = pd.read_csv('graph.csv')
df_bar = pd.read_csv('bar_plots.csv')


def generate_table(dataframe, max_rows=1, row=0):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[row][col]) for col in dataframe.columns
            ]) #for i in range(min(len(dataframe), max_rows))
        ])
    ])

image_filename = 'ist.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename1 = 'central.png'
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())

#create dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={
                'height': '30%',
                'width': '30%'
            }),
    html.H1('Energy Services',style={'textAlign':'center', 'fontSize': 30}),
    html.H2('Project 2',style={'textAlign':'center', 'fontSize': 24}),
    html.H3('Catarina Neves 91036',style={'textAlign':'center', 'fontSize': 16}),
    html.Div('''
        Dashboard of Project 1 - Forecasting Power Consumption of Central Building in Jan-Mar 2019
    ''',style={'textAlign':'center', 'fontSize': 24}),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()),style={
                'height': '30%',
                'width': '30%'
            }),
    html.H1('Online at https://dash-app91036.herokuapp.com/',style={'textAlign':'right', 'fontSize': 16}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Raw Data', value='tab-1'),
        dcc.Tab(label='Forecasting Methods', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
],style={'textAlign':'center'})

@app.callback(Output('tabs-content', 'children'),
                     Input('tabs', 'value'))  

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Label('Type of Graph'),
            dcc.Dropdown(
                id='dropdown1',
                options=[
                    {'label':'Yearly Evolution','value':0},
                    {'label':'Bar Graph','value':1}
                    ],
                    value=0
                ),
            html.Div(id='drop1')
        ],style={'textAlign':'left'})

    elif tab == 'tab-2':
        return html.Div([
    html.Div([
            html.Label('Type of Forecasting Method'),
            dcc.Dropdown(
                id='dropdown2',
                options=[
                    {'label':'Extreme Gradient Boosting','value':0},
                    {'label':'Bootstrapping','value':1},
                    {'label':'Gradient Boosting','value':2}

                    ],
                    value=0
                ),
        ],style={'textAlign':'left'}),
    html.Div([
        html.Label('Metrics of the Forecast'),
        dcc.Dropdown(
            id='dropdown4',
            options=[
                {'label':'Graph','value':3},
                {'label':'Table (values)','value':4},
                ],
                value=3
            ),
    ],style={'textAlign':'left'}),
            html.Div(id='drop2')

    ])
    
@app.callback(Output('drop1', 'children'),
                  Input('dropdown1', 'value'))

def drop_graph(dropdown):
    if dropdown == 0:
        return html.Div([
                dcc.Graph(
                    id='yearly_data',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Central'},
                        ],
                        'layout': {
                            'title': 'Central Building Power Consumption throughout Jan-Mar 2019 (kWh)'
                        }
                    }
                ),
                dcc.Graph(
                    id='yearly_temp',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['temp_C'], 'type': 'line', 'name': 'Central','line':dict(color='red')},
                        ],
                        'layout': {
                            'title': 'Temperature at Central Building throghout Jan-Mar 2019 (ºC)'
                        }
                    }
                ),
                
                dcc.Graph(
                    id='yearly_rad',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['solarRad_W/m2'], 'type': 'line', 'name': 'Central','line':dict(color='orange')},
                        ],
                        'layout': {
                            'title': 'Solar Radiation at Central Building throughout Jan-Mar 2019 (W/m^2)'
                        }
                    }
                ),
                
                dcc.Graph(
                    id='yearly_hol',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['Holiday'], 'type': 'line', 'name': 'Central','line':dict(color='brown')},
                        ],
                        'layout': {
                            'title': 'Holidays at Central Building throughout Jan-Mar 2019'
                        }
                    }
                ),
                
                dcc.Textarea(
                    id='textarea-example',
                    value='0- Teaching Period and Exam Season,\n1- Holidays and Weekends,\n2- Exam Preparation, \n3- Break',
                    style={'textAlign':'center','width': '50%', 'height': 85},
                ),

                dcc.Graph(
                    id='yearly_hour',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['Hour'], 'type': 'line', 'name': 'Central','line':dict(color='green')},
                        ],
                        'layout': {
                            'title': 'Hours at Central Building throughout Jan-Mar 2019'
                        }
                    }
                ),
                
                dcc.Graph(
                    id='yearly_weekday',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['Weekday'], 'type': 'line', 'name': 'Central','line':dict(color='purple')},
                        ],
                        'layout': {
                            'title': 'Weekdays at Central Building throughout Jan-Mar 2019'
                        }
                    }
                ),
                dcc.Textarea(
                    id='textarea-example1',
                    value='0- Monday,\n1- Tuesday,\n2- Wednesday, \n3- Thursday, \n4- Friday, \n5- Saturday, \n6- Sunday',
                    style={'textAlign':'center','width': '50%', 'height': 140},
                ),
                
                dcc.Graph(
                    id='yearly_power-1',
                    figure={
                        'data': [
                        {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power-1'], 'type': 'line', 'name': 'Central','line':dict(color='gray')},
                        ],
                        'layout': {
                            'title': 'Power-1 at Central Building throughout Jan-Mar 2019 (kWh)'
                        }
                    }
                ),
        ],style={'textAlign':'center'})
    
    if dropdown == 1:
        return html.Div([
                dcc.Graph(
                    id='yearly_power_bar',
                    figure=px.histogram(df_bar, x='Power_kW', nbins=5, title='Histogram of Daily Average of Power Consumption at Central Building Jan-Mar 2019', labels={
                         "Power_kW": "Power Consumption Jan-Mar 2019 (kWh)",
                         "count": "Count"
                     })
                ),
                
                dcc.Graph(
                    id='yearly_temp_bar',
                    figure=px.histogram(df_bar, x='temp_C', nbins=5, title='Histogram of Daily Average of Temperature at Central Building Jan-Mar 2019',labels={
                         "temp_C": "Temperature Jan-Mar 2019 (ºC)",
                         "count": "Count"
                     },color_discrete_sequence=['red']),
                ),
                
                dcc.Graph(
                    id='yearly_solar_bar',
                    figure=px.histogram(df_bar, x='solarRad_W/m2', nbins=5, title='Histogram of Daily Average of Solar Radiation at Central Building Jan-Mar 2019', labels={
                         "solarRad_W/m2": "Solar Radiaiton Jan-Mar 2019 (kWh)",
                         "count": "Count"
                     }, color_discrete_sequence=['orange']),
                ),
        ], style={'textAlign':'center'})
    
       
@app.callback(Output('drop2', 'children'),
                    [Input('dropdown2', 'value'),
                     Input('dropdown4', 'value')])  

def drop_reg(dropdown2,dropdown4):
    if dropdown2 == 0 and dropdown4 == 3:
        return html.Div([
            dcc.Graph(
                id='pred_data',
                figure={
                    'data': [
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Real Data'},
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW_XGB'], 'type': 'line', 'name': 'Prediction XGB'},
                    ],
                    'layout': {
                        'title': 'Central Building Power Consumption Jan-Mar 2019 + Extreme Gradient Boosting Prediction (kWh)'
                    }
                }
            ),
            
            dcc.Graph(
                id='pred_graph',
                figure=px.scatter(df_graph, x='data',y='pred_XGB',labels={
                     "data": "Real Data Jan-Mar 2019 (kWh)",
                     "pred_XGB": "XGB Prediction Jan-Mar 2019 (kWh)"
                 }),
            ),
            
        ])
    
    if dropdown2 == 0 and dropdown4 == 4:
        return html.Div([
            dcc.Graph(
                id='pred_data',
                figure={
                    'data': [
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Real Data'},
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW_XGB'], 'type': 'line', 'name': 'Prediction XGB'},
                    ],
                    'layout': {
                        'title': 'Central Building Power Consumption Jan-Mar 2019 + Extreme Gradient Boosting Prediction (kWh)'
                    }
                }
            ),
           generate_table(df_tab,1,0)
        ])
    
    if dropdown2 == 1 and dropdown4 == 3:
        return html.Div([
            dcc.Graph(
                id='pred_data',
                figure={
                    'data': [
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Real Data'},
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW_BT'], 'type': 'line', 'name': 'Prediction BT'},
                    ],
                    'layout': {
                        'title': 'Central Building Power Consumption Jan-Mar 2019 + Bootstrapping Prediction (kWh)'
                    }
                }
            ),
            dcc.Graph(
                id='pred_graph',
                figure=px.scatter(df_graph, x='data',y='pred_BT',labels={
                     "data": "Real Data Jan-Mar 2019 (kWh)",
                     "pred_BT": "BT Prediction Jan-Mar 2019 (kWh)"
                 }),
            ),
        ])
    
    if dropdown2 == 1 and dropdown4 == 4:
        return html.Div([
            dcc.Graph(
                id='pred_data',
                figure={
                    'data': [
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Real Data'},
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW_BT'], 'type': 'line', 'name': 'Prediction BT'},
                    ],
                    'layout': {
                        'title': 'Central Building Power Consumption Jan-Mar 2019 + Bootstrapping Prediction (kWh)'
                    }
                }
            ),
            generate_table(df_tab,1,1)
        ])
    
    if dropdown2 == 2 and dropdown4 == 3:
        return html.Div([
            dcc.Graph(
                id='pred_data',
                figure={
                    'data': [
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Real Data'},
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW_GB'], 'type': 'line', 'name': 'Prediction GB'},
                    ],
                    'layout': {
                        'title': 'Central Building Power Consumption Jan-Mar 2019 + Gradient Boosting Prediction (kWh)'
                    }
                }
            ),
            dcc.Graph(
                id='pred_graph',
                figure=px.scatter(df_graph, x='data',y='pred_GB',labels={
                     "data": "Real Data Jan-Mar 2019 (kWh)",
                     "pred_GB": "GB Prediction Jan-Mar 2019 (kWh)"
                 }),
            ),
        ])
    
    if dropdown2 == 2 and dropdown4 == 4:
        return html.Div([
            dcc.Graph(
                id='pred_data',
                figure={
                    'data': [
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW'], 'type': 'line', 'name': 'Real Data'},
                       {'x': df_pred_2019['Date'], 'y': df_pred_2019['Power_kW_GB'], 'type': 'line', 'name': 'Prediction GB'},
                    ],
                    'layout': {
                        'title': 'Central Building Power Consumption Jan-Mar 2019 + Gradient Boosting Prediction (kWh)'
                    }
                }
            ),
            generate_table(df_tab,1,2)
        ])


    
   

if __name__ == '__main__':
    app.run_server(debug=True)
