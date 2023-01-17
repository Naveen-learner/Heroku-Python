#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 11:49:15 2023

@author: naveenkumaruppara
"""

#import necessary libraries for dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import *
import random
from jupyter_dash import JupyterDash
from dash_slicer import VolumeSlicer
from dash import Dash, html
from dash.dependencies import Input, Output
import numpy as np
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.subplots as sp


#Data Manipulation

#Input data - sheet 1
Input_data = pd.read_excel("/Users/naveenkumaruppara/Downloads/Sales-Dashboard-practice-file.xlsx")

#Master data - sheet 2
Master_data = pd.read_excel("/Users/naveenkumaruppara/Downloads/Sales-Dashboard-practice-file.xlsx", sheet_name='Master Data')

Master_data['TOTAL BUYING VALUE'] = Input_data['QUANTITY'] * Master_data["BUYING PRIZE"]
Master_data['TOTAL SELLING VALUE'] = Input_data['QUANTITY'] * Master_data["SELLING PRICE"]
Input_data['YEAR'] = pd.DatetimeIndex(Input_data['DATE']).year
Input_data['MONTH'] = pd.DatetimeIndex(Input_data['DATE']).month
Input_data['DAY'] = pd.DatetimeIndex(Input_data['DATE']).day
BUYING_PRIZE = []
SELLING_PRIZE=[]
PRODUCT=[]
CATEGORY=[]
UOM=[]


for i in range(527):
    for j in range(45):
        if Input_data['PRODUCT ID'][i] == Master_data['PRODUCT ID'][j]:
            BUYING_PRIZE.append(Master_data['BUYING PRIZE'][j])
            SELLING_PRIZE.append(Master_data['SELLING PRICE'][j])
            PRODUCT.append((Master_data['PRODUCT'][j]))
            CATEGORY.append((Master_data['CATEGORY'][j]))
            UOM.append((Master_data['UOM'][j]))
            
Input_data['BUYING PRIZE'] = pd.DataFrame(BUYING_PRIZE)
Input_data['SELLING PRICE'] = pd.DataFrame(SELLING_PRIZE)
Input_data['PRODUCT'] = pd.DataFrame(PRODUCT)
Input_data['CATEGORY'] = pd.DataFrame(CATEGORY)
Input_data['UOM'] = pd.DataFrame(UOM)
Input_data['TOTAL BUYING VALUE'] = Input_data['QUANTITY'] * Input_data["BUYING PRIZE"]
Input_data['TOTAL SELLING VALUE'] = Input_data['QUANTITY'] * Input_data["SELLING PRICE"]


pivot = pd.pivot_table(Input_data,index=['DAY'],aggfunc= 'sum')
pivot_1 = pd.pivot_table(Input_data,index=['MONTH'],aggfunc= 'sum')
pivot_2 = pd.pivot_table(Input_data,index=['PRODUCT','UOM'],aggfunc= 'sum')
pivot_3 = pd.pivot_table(Input_data,index=['CATEGORY'],aggfunc= 'sum')
pivot_4 = pd.pivot_table(Input_data,index=['SALE TYPE'],aggfunc= 'sum')
pivot_5 = pd.pivot_table(Input_data,index=['PAYMENT MODE'],aggfunc= 'sum')
pivot_6 = pd.pivot_table(Input_data,index=['YEAR'],aggfunc= 'sum')
pivot_7 = pd.pivot_table(Input_data,index=['PRODUCT'],aggfunc= 'sum')

pivot_4['SALE TYPE'] = pivot_4.index
pivot_1['MONTH'] = pivot_1.index
pivot_3['CATEGORY'] = pivot_3.index
pivot_7['PRODUCT'] = pivot_7.index
pivot_5['PAYMENT MODE'] = pivot_5.index
pivot_6['YEAR']=pivot_6.index
pivot['DAY'] = pivot.index

#Dash themes

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                )
app.title = "SALES DASHBOARD"

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}
'''app.css.append_css({
"external_url": "  https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
})

# Bootstrap Javascript.
app.scripts.append_script({
"external_url": "https://code.jquery.com/jquery-3.2.1.slim.min.js"
})
app.scripts.append_script({
"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
})'''

#creating figures

fig1 = go.Pie(
     values=pivot_4['TOTAL SELLING VALUE'],
     labels=pivot_4['SALE TYPE'],
     domain=dict(x=[0, 0.5]),
     name="SALE TYPE",
     hoverinfo="label+percent+name",
)
fig5 = go.Pie(
     values=pivot_5['TOTAL SELLING VALUE'],
     labels=pivot_5['PAYMENT MODE'],
     domain=dict(x=[0, 0.5]),
     name="PAYEMENT MODE",
     hoverinfo="label+percent+name",
)

fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = sum(Input_data["TOTAL SELLING VALUE"]),
    number = {'prefix': "$"},
    delta = {'position': "top", 'reference': 320},
    domain = {'x': [0, 1], 'y': [0, 1]}))


layout = go.Layout(title="TOTAL SELLING VALUE",)
data = [fig1, fig5]
fig1 = go.Figure(data=data, layout=layout)
years = Input_data['YEAR'].unique()
month = Input_data['MONTH'].unique()
#app layout
app.layout = html.Div(children=[
    html.Div(children=[
        html.H3(children='Sales Data'),
        html.H6(children='Superstore Shop', style={'marginTop': '-15px', 'marginBottom': '30px'}),
    html.Div([
        html.Label(['Total Selling Value']),
        dcc.Dropdown(
            id='Year',
            options=[{'label': y, 'value': y} for y in years],
            value=years[0],
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
        dcc.Dropdown(
            id='Month',
            options=[{'label': m, 'value': m} for m in month],
            value=month[0],
            multi=False,
            clearable=False,
            style={"width": "50%"})
    ]),

    html.Div([
        dcc.Graph(figure=fig),
        dcc.Graph(id='the_graph',style={'display': 'inline-block'}),
        dcc.Graph(id='the_graph2',style={'display': 'inline-block'}),
        dcc.Graph(id='the_graph3',style={'display': 'inline-block'}),
        dcc.Graph(id='Categorical',style={'display': 'inline-block'},className='plot')
    ])]
        ,style={'textAlign': 'center'})],
        style={'padding': '2rem'})

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='Year', component_property='value')]
)


def update_graph(year):
    piechart = px.pie(
        Input_data[Input_data['YEAR'] == int(year)],
        values='TOTAL SELLING VALUE',
        names='SALE TYPE',
        hole=.3)
    return piechart
@app.callback(
    Output(component_id='the_graph2', component_property='figure'),
    [Input(component_id='Year', component_property='value')]
)
def update_graph(year):
    piechart2 = px.pie(
        Input_data[Input_data['YEAR'] == int(year)],
        values='TOTAL SELLING VALUE',
        names='PAYMENT MODE',
        hole=.3,
    )
    return piechart2

@app.callback(
    Output(component_id='the_graph3', component_property='figure'),
    [Input(component_id='Year', component_property='value')]
)  
def update_graph(year):
    barchart = px.bar(
        Input_data[Input_data['YEAR'] == int(year)],
        x='MONTH',
        y=["TOTAL SELLING VALUE", "TOTAL BUYING VALUE"],
        title='MONTH'
    )
    return barchart
@app.callback(
    Output(component_id='Categorical', component_property='figure'),
    [Input(component_id='Year', component_property='value')]
)
def update_graph(year):
    treemap = px.treemap(
        Input_data[Input_data['YEAR'] == int(year)],
        path=[px.Constant("Category"), 'CATEGORY'],
        values='TOTAL SELLING VALUE',
        title='MONTH'
    )
    return treemap

if __name__ == '__main__':
    app.run_server(debug=True,port=4050)