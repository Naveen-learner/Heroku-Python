
#Importing necessaary libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State#, Event
import random
import plotly
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import os

#Import dataframe
url='https://raw.githubusercontent.com/Naveen-learner/Heroku-Python/main/Sales.csv'
df=pd.read_csv(url,sep=',')

df['YEAR']=df['YEAR'].astype(str)
df['MONTH']=df['MONTH'].astype(str)

#creating pivot tables
pivot = pd.pivot_table(df,index=['DAY'],aggfunc= 'sum')
pivot_1 = pd.pivot_table(df,index=['MONTH'],aggfunc= 'sum')
pivot_2 = pd.pivot_table(df,index=['PRODUCT','UOM'],aggfunc= 'sum')
pivot_3 = pd.pivot_table(df,index=['CATEGORY'],aggfunc= 'sum')
pivot_4 = pd.pivot_table(df,index=['SALE TYPE'],aggfunc= 'sum')
pivot_5 = pd.pivot_table(df,index=['PAYMENT MODE'],aggfunc= 'sum')
pivot_6 = pd.pivot_table(df,index=['YEAR'],aggfunc= 'sum')
pivot_7 = pd.pivot_table(df,index=['PRODUCT'],aggfunc= 'sum')

pivot_4['SALE TYPE'] = pivot_4.index
pivot_1['MONTH'] = pivot_1.index
pivot_3['CATEGORY'] = pivot_3.index
pivot_7['PRODUCT'] = pivot_7.index
pivot_5['PAYMENT MODE'] = pivot_5.index
pivot_6['YEAR']=pivot_6.index
pivot['DAY'] = pivot.index
years = df['YEAR'].unique()
month = df['MONTH'].unique()

# Instantiate our App and incorporate BOOTSTRAP theme stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Treemap for categorical data
fig3 = px.treemap(pivot_3,path=[px.Constant("Category"), 'CATEGORY'],values='TOTAL SELLING VALUE')

# Build the layout to define what will be displayed on the page
app.layout = dbc.Container([
    dbc.Row([
       dbc.Col([
           html.H1("SALES DASHBOARD"),
           html.Label('Supermarket Shop')
       ], width=12)
    ], justify="left-align"),
    
    dbc.Row([
       dbc.Col([
           html.H2("Total Sales 4014119$")
       ], width=4),
        dbc.Col([
           html.H2("Total profit 68907.92$")
       ], width=4),
        dbc.Col([
           html.H2("Total profit% 17.16")
       ], width=4)
    ]),
    
    
    dbc.Row([
        dbc.Col([
             html.Div([
                 html.Div([
            html.Label('Sales Type'),
            dcc.Dropdown(id='linedropdown',
                options=[
                         {'label': 'TOTAL BUYING VALUE', 'value': 'TOTAL BUYING VALUE'},
                         {'label': 'TOTAL SELLING VALUE', 'value': 'TOTAL SELLING VALUE'}
                ],
                value='TOTAL BUYING VALUE',
                multi=False,
                clearable=False
            ),
            ],className='six columns'),
               html.Div(id='dd-output-container'),

    ],className='row'),  
                 
            
        ], width=6),
        
        dbc.Col([
            
            html.Div([
                 html.Div([
            html.Label('select year'),
             dcc.RadioItems(id='linedropdown@1',
                options=['2021','2022'],
                value='2021'
               
            ),
            ],className='six columns'),
                
                html.Div([
            html.Label('select month'),
            dcc.Dropdown(id='linedropdown@2',
                options=[
                         {'label': 'JAN', 'value': '1'},
                         {'label': 'FEB', 'value': '2'},
                    {'label': 'MAR', 'value': '3'},
                    {'label': 'APR', 'value': '4'},
                    {'label': 'MAY', 'value': '5'},
                    {'label': 'JUN', 'value': '6'},
                    {'label': 'JUL', 'value': '7'},
                    {'label': 'AUG', 'value': '8'},
                    {'label': 'SEP', 'value': '9'},
                    {'label': 'OCT', 'value': '10'},
                    {'label': 'NUV', 'value': '11'},
                    {'label': 'DEC', 'value': '12'}
                    
                ],
                value='1',
                multi=False,
                clearable=False
            ),
            ],className='six columns'),
                
               html.Div(id='dd-output-container@1'),

    ],className='row'),
            
            
        ], width=6)
        ]),
        
    
    dbc.Row([
        dbc.Col([
            
            
            html.Div([
                 html.Div([
            html.Label('Payment Type'),
                     html.Br(),
            dcc.Dropdown(id='linedropdown01',
                options=[
                         {'label': 'TOTAL BUYING VALUE', 'value':'TOTAL BUYING VALUE'},
                         {'label': 'TOTAL SELLING VALUE','value':'TOTAL SELLING VALUE'}
                ],
                value='TOTAL BUYING VALUE',
                multi=False,
                clearable=False
            ),
            ],className='six columns'),
               html.Div(id='dd-output-container01'),

    ],className='row'), 
            
            
            
        ], width=4),
        dbc.Col([
            
            html.Div([
                 html.Div([
            html.Label('Day Statistics'),
                     html.Br(),
            dcc.Dropdown(id='linedropdown@9',
                options=[
                         {'label': 'TOTAL BUYING VALUE', 'value': 'TOTAL BUYING VALUE'},
                         {'label': 'TOTAL SELLING VALUE', 'value': 'TOTAL SELLING VALUE'}
                ],
                value='TOTAL BUYING VALUE',
                multi=False,
                clearable=False
            ),
            ],className='six columns'),
               html.Div(id='dd-output-container@9'),

    ],className='row'),
            
            
        ], width=4),
        
        dbc.Col([
            html.Label('Different Categories'),
            dcc.Graph(
        id='PAYMENT MODE',
        figure=fig3),
        ], width=4)
    ])
])

# callback is used to create app interactivity
#@callback()
@app.callback(
    Output('dd-output-container', 'children'),
    Input('linedropdown', 'value')
)
def  update_table(input_value):
    return dcc.Graph(figure=px.pie(pivot_4, values=input_value, names='SALE TYPE',hole=.3))   
            
                
@app.callback(
    Output('dd-output-container01', 'children'),
    Input('linedropdown01', 'value')
)
def  update_table(input_value):
    return dcc.Graph(figure=px.pie(pivot_5, values=input_value, names='PAYMENT MODE',hole=.3)) 


@app.callback(
    Output('dd-output-container@1', 'children'),
    Input('linedropdown@1', 'value'),
    Input('linedropdown@2', 'value')
)
def building(a,b):
    df1=df.loc[df['YEAR']==a]
    df2=df1.loc[df['MONTH']==b]
    return dcc.Graph(figure=px.bar(df2, x="TOTAL SELLING VALUE", y="PRODUCT", orientation='h'))
    #return df2
    
@app.callback(
    Output('dd-output-container@9', 'children'),
    Input('linedropdown@9', 'value')
)
def  update_table(input_value):
    return dcc.Graph(figure=px.area(pivot, x='DAY', y=input_value)) 
    


# Run the App
if __name__ == '__main__':
    app.listen(process.env.PORT || 3000, function(){
  console.log("Express server listening on port %d in %s mode", this.address().port, app.settings.env);
});
