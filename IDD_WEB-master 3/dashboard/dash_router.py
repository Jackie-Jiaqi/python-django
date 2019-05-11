from dash.dependencies import Output, Input
from .dash_server import app
from . import dash_layouts
import pandas as pd
import dash
import plotly.graph_objs as go
from plotly import tools
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
from flask import send_from_directory
from flask import Flask, request, redirect
import pandas as pd
import numpy as np
from plotly.graph_objs import *
import plotly.graph_objs as go
import plotly.plotly as py
import os
from datetime import datetime, timedelta
import datetime as dt
import random
from random import randint
import time
import pymongo
from pymongo import MongoClient


game_df1 = pd.read_csv('game_data.csv')

date_list = {0:pd.to_datetime("2015-11-01"),
             1:pd.to_datetime("2015-12-01"),
             2:pd.to_datetime("2016-01-01"),
             3:pd.to_datetime("2016-02-01"),
             4:pd.to_datetime("2016-03-01")}

game_df = game_df1[game_df1['period.name'] == 'Session']
game_df.date = pd.to_datetime(game_df.date,dayfirst=True)
player_name_list = list(game_df['player.name'].unique())
# print(player_name_list)


connection = MongoClient()
db = connection.get_database('sports')
collection = db.get_collection('injury')
collection2 = db.get_collection('body')
df = pd.read_csv('sport.csv')
df = df[df['game.or.practice'] == 1]
df = df.sort_values('date').reset_index(drop=True)
date_slider = df['date'].tolist()
indicators = df['period.name'].unique()
game_indicators = ['TP', 'FGA', 'FGA3PT', 'FTA', 'TO', 'duration']
player_indicators = df.columns

# Define a dictionary of the pages in the urlpatterns that you wish to associate Dash.
# Dash will match what is in the url to the keys in this dictionary and return the corresponding layout
dash_routes = (
                ('team', dash_layouts.team_layout),
                ('player', dash_layouts.player_layout),
                ('body', dash_layouts.body_layout),
                ('playerload',dash_layouts.playerload_layout),
               )
dash_routes = dict(dash_routes)

@app.callback(Output('dash_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    '''
    comments here
    '''

    if pathname is None:
        return ''

    # print("\n\nPrinting pathname:%s" %(pathname) )
    # print("Printing dash url routes:")
    for k, v in dash_routes.items():
        if k in pathname:
            page = dash_routes[k]
            print("\tCurrent key: '%s' has a page matched. Returning the corresponding layout" %(k))
        else:
            print("\tCurrent key: '%s' has no page match" %(k))
    # print("\n\n")


    if callable(page):
        layout = page(pathname)
    else:
        layout = page

    return layout



@app.callback(
    dash.dependencies.Output('playerload1', 'figure'),
    [
     dash.dependencies.Input('playerload_dropdown', 'value'),
     ]
)
def update_graph(Player_name_1):
    print ("1jasbdfubagba;fhahf======================k")
    game_df = game_df1[game_df1['player.name']==Player_name_1]
    avg_playerload = game_df.groupby("period.name")
    avg_playerload = avg_playerload['player.load'].mean()
    print(list(avg_playerload))
    print(list(game_df1['period.name'].unique()))

    # data1 = go.Bar(
    #         x=[100,200,300,400,500,600,700,800,900,1000,1100,1200],
    #         y=[avg_playerload],
    #         xaxis='x',
    #         yaxis='y',
    #         name='Team1',
    #         #orientation='h',
    #         textposition='auto')
    data1 = {
        "x":list(avg_playerload),
        "y":list(game_df1['period.name']),
        "name":"sdf",
        "type": "histogram",
        "orientation":"h"
    }
    # data1 = go.Histogram(
    #     x = avg_playerload,
    #     y = game_df1["period.name"],
    #     xaxis='x',
    #     yaxis='y',
    #     orientation='h'
    #
    # )
    layout = {
        "margin":{
            "l":150
        }
    }
    data = Data([data1])
    fig = Figure(data=data,layout=layout)
    # fig = tools.make_subplots(rows=1, cols=1)
    #
    # fig.append_trace(data1, 1, 1)
    #
    # fig['layout'].update(yaxis=dict(range=[0, 15]),
    #                      title='Player Load Visualisation')

    return fig











@app.callback(
    dash.dependencies.Output('g1', 'figure'),
    [dash.dependencies.Input('home_away_1', 'value'),
     dash.dependencies.Input('Player_name_1', 'values'),
     dash.dependencies.Input('slider_1', 'value'),
     ]
)
def update_graph(home_away_1, Player_name_1, slide_value):
    fir_date = date_list[slide_value[0]]
    sec_date = date_list[slide_value[1]]

    team1_dff = game_df[game_df["home.or.away"] == home_away_1]
    team1_dff = team1_dff[team1_dff['player.name'].isin(Player_name_1)]
    team1_dff = team1_dff[(team1_dff.date >= fir_date) & (team1_dff.date <= sec_date)]

    total_point = team1_dff["tp"].sum()
    total_fta = team1_dff['tot.fga'].sum()
    total_play = team1_dff.shape[0]
    total_to = team1_dff.to.sum()
    total_per = team1_dff.shoot_percentage.sum()


    data1 = go.Bar(
            x=["TP","FGA","TO" , "SP"],
            y=[total_point/total_play, total_fta/total_play, total_to/total_play,total_per/total_play],
            xaxis='x',
            yaxis='y',
            name='Team1',
            #orientation='h',
            textposition='auto')

    fig = tools.make_subplots(rows=1, cols=1)

    fig.append_trace(data1, 1, 1)

    fig['layout'].update(yaxis=dict(range=[0, 15]),
                         title='Player/Team A Status')

    return fig

@app.callback(
    dash.dependencies.Output('g2', 'figure'),
    [
     dash.dependencies.Input('home_away_2', 'value'),
     dash.dependencies.Input('Player_name_2', 'values'),
     dash.dependencies.Input('slider_2', 'value'),
     ]
)
def update_graph(home_away_2, Player_name_2, slide_value2):

    fir_date = date_list[slide_value2[0]]
    sec_date = date_list[slide_value2[1]]

    game_dff_2 = game_df[game_df["home.or.away"] == home_away_2]
    game_dff_2 = game_dff_2[game_dff_2['player.name'].isin(Player_name_2)]
    game_dff_2 = game_dff_2[(game_dff_2.date >= fir_date) & (game_dff_2.date <= sec_date)]

    total_point2 = game_dff_2["tp"].sum()
    total_fta2 = game_dff_2['tot.fga'].sum()
    total_play2 =  game_dff_2.shape[0]
    total_to2 = game_dff_2.to.sum()
    total_per2 = game_dff_2.shoot_percentage.sum()


    data2 = go.Bar(
                x=["TP", "FGA", "TO", "SP"],
                y=[total_point2 / total_play2, total_fta2 / total_play2, total_to2 / total_play2,
                   total_per2 / total_play2],
                xaxis='x2',
                yaxis='y2',
                name='Team2',
                #text=y,
                #textposition='auto',
                #orientation='h',

                marker=dict(
                    color='rgb(255, 102, 51)',
    ))



    fig = tools.make_subplots(rows=1, cols=1)

    fig.append_trace(data2, 1, 1)
    fig['layout'].update(yaxis=dict(range=[0, 15]),
                         title='Player/Team B Status')
    return fig

@app.callback(
    dash.dependencies.Output('g3', 'figure'),
    [dash.dependencies.Input('home_away_1', 'value'),
     dash.dependencies.Input('Player_name_1', 'values'),
     dash.dependencies.Input('slider_1', 'value'),

     dash.dependencies.Input('home_away_2', 'value'),
     dash.dependencies.Input('Player_name_2', 'values'),
     dash.dependencies.Input('slider_2', 'value'),
     ]
)
def update_graph(home_away_1, Player_name_1, slide_value,home_away_2, Player_name_2, slide_value2):
    # print(slide_value)

    fir_date = date_list[slide_value[0]]
    sec_date = date_list[slide_value[1]]

    team1_dff = game_df[game_df["home.or.away"] == home_away_1]
    team1_dff = team1_dff[team1_dff['player.name'].isin(Player_name_1)]
    team1_dff = team1_dff[(team1_dff.date >= fir_date) & (team1_dff.date <= sec_date)]

    fir_date = date_list[slide_value2[0]]
    sec_date = date_list[slide_value2[1]]

    game_dff_2 = game_df[game_df["home.or.away"] == home_away_2]
    game_dff_2 = game_dff_2[game_dff_2['player.name'].isin(Player_name_2)]
    game_dff_2 = game_dff_2[(game_dff_2.date >= fir_date) & (game_dff_2.date <= sec_date)]

    total_point = team1_dff["tp"].sum()
    total_fta = team1_dff['tot.fga'].sum()
    total_play = team1_dff.shape[0]
    total_to = team1_dff.to.sum() * 5
    total_per = team1_dff.shoot_percentage.sum() * 20

    total_point2 = game_dff_2["tp"].sum()
    total_fta2 = game_dff_2['tot.fga'].sum()
    total_play2 = team1_dff.shape[0]
    total_to2 = game_dff_2.to.sum() * 5
    total_per2 = game_dff_2.shoot_percentage.sum() * 20

    radar1 = go.Scatterpolar(
        r=[total_point/total_play, total_fta/total_play, total_to/total_play,total_per/total_play, total_point/total_play],
        theta=["TP", "FGA", "TO", "SP","TP"],
        fill='toself',
        name='Team A'
    )

    radar2 = go.Scatterpolar(
        r=[total_point2 / total_play2, total_fta2 / total_play2, total_to2 / total_play2,
                   total_per2 / total_play2, total_point2 / total_play2,],
        theta=["TP", "FGA", "TO", "SP","TP"],
        fill='toself',
        name='Team B'
    )

    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
            )
        ),
        showlegend=True
    )

    fig = go.Figure(data=[radar1,radar2], layout=layout)

    return fig


def get_initials(fullname):
    xs = (fullname)
    name_list = xs.split()

    initials = ""

    for name in name_list:  # go through each name
        initials += name[0].upper()  # append the initial

    return initials


@app.callback(
    dash.dependencies.Output('scatter-filter', 'figure'),
    [dash.dependencies.Input('period-filter', 'value'),
     dash.dependencies.Input('player-data-filter', 'value'),
     dash.dependencies.Input('period-filter-type', 'value'),
     dash.dependencies.Input('player-data-filter-type', 'value'),
     # dash.dependencies.Input('crossfilter-year--slider', 'value')
     ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 # date_value
                 ):
    # dff = df[df['date'] == date_value
    dff = df.groupby('player.name').sum()
    dff.reset_index(inplace=True)
    # metric = yaxis_column_name,

    return {
        'data': [go.Scatter(
            # x=dff[dff['period.name'] == xaxis_column_name]['player.load'],
            # y=dff[dff['period.name'] == yaxis_column_name]['player.load'],
            y=dff[yaxis_column_name],
            x=dff['player.load.minute'],
            # text=dff[dff['period.name'] == yaxis_column_name]['player.name'],
            # customdata=dff[dff['period.name'] == yaxis_column_name]['player.name'],
            text=dff['player.name'].map(lambda x: get_initials(x)),
            # font = {'color': 'black', 'size': 8},
            textposition='middle center',
            customdata=dff['player.name'],
            mode='markers+text',
            # hoverinfo='skip',
            # mode='markers',
            marker={
                'size': 40,
                'opacity': 0.7,
                'color': '#2aa9d2',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            yaxis={
                'title': 'Avg.' + str(yaxis_column_name),
                'type': 'log' if xaxis_type == 'Log' else 'linear',
                'titlefont': {'family': 'Verdana', 'size': 10, 'color': '#8f8f8f'}
            },
            xaxis={
                'title': 'Avg. Player Load per minute    Radius = Game minutes',
                'type': 'log' if yaxis_type == 'Log' else 'linear',
                'titlefont': {'family': 'Verdana', 'size': 10, 'color': '#8f8f8f'}
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 10},
            height=400,
            # hovermode='closest',
            # title='All Players'
        )
    }

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['date'],
            y=dff['player.load'],
            mode='lines+markers',
            hoverinfo='skip',
            marker={
                'color': '#2aa9d2',
                'line': {'width': 0.5, 'color': '#2aa9d2'}
            },
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 50},
            'annotations': [{
                'x': 0, 'y': 1, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': True}
        }
    }

def create_time_series2(dff, axis_type, metric, title):
    return {
        'data': [go.Scatter(
            x=dff['date'],
            y=dff[metric],
            mode='lines+markers',
            hoverinfo='skip',
            marker={
                'color': '#2aa9d2',
                'line': {'width': 0.5, 'color': '#2aa9d2'}
            },
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 50, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'line' if axis_type == 'Line' else 'log'},
            'xaxis': {'showgrid': True}
        }
    }

@app.callback(
    dash.dependencies.Output('player-load', 'figure'),
    [dash.dependencies.Input('scatter-filter', 'hoverData'),
     dash.dependencies.Input('period-filter', 'value'),
     dash.dependencies.Input('period-filter-type', 'value')])
def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
    player_name = hoverData['points'][0]['customdata']
    dff = df[df['player.name'] == player_name]
    dff = dff[dff['period.name'] == xaxis_column_name]
    # title = '<b>{}</b><br>{}'.format(player_name, xaxis_column_name)
    title = '<b>{}'.format(player_name)
    return create_time_series(dff, axis_type, title)


@app.callback(dash.dependencies.Output('performance-metrics', 'figure'),
    [dash.dependencies.Input('scatter-filter', 'hoverData'),
     dash.dependencies.Input('player-data-filter', 'value'),
     dash.dependencies.Input('player-data-filter-type', 'value')])
def update_y_timeseries(hoverData, yaxis_column_name, axis_type):
    player_name = hoverData['points'][0]['customdata']
    dff = df[df['player.name'] == hoverData['points'][0]['customdata']]
    metric = yaxis_column_name
    title = '<b>{}'.format(player_name)
    return create_time_series2(dff, axis_type, metric, title)


@app.callback(dash.dependencies.Output('realtime-injury', 'figure'),
    [dash.dependencies.Input('realtime-injury-update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_injury(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.injury.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),

        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['Playerload'].map(lambda x: x / 3 if x > 1070 else x / 2),
        x=dff['Time'],
        mode='lines+markers',
        name='Injury Probability',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),

        hoverinfo='skip')

    layout = Layout(
        title='Heart Rate: ' + str(dff['Heartrate'].iloc[-1]) + '/RPM' + '  |  Injury Probability: ' + str(dff['Threashold'].iloc[-1]) + '%',
        #font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
        height=450,
        xaxis=dict(
            title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[200, 1200],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)








@app.callback(dash.dependencies.Output('left_arm_graph', 'figure'),
    [dash.dependencies.Input('left_arm_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['left_arm_risk'],
        x=dff['Time'],
        mode='lines+markers',
        name='Left arm risk',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    layout = Layout(
        #title= ' Left arm risk: ' + str(dff['left_arm_risk'].iloc[-1]),
        #font=dict(family='Courier New, monospace', size=5, color='#7f7f7f'),
        height = 200,
        width = 200,
        margin = {'l': 35, 'b': 8, 't': 20, 'r': 10},

        xaxis=dict(
            #title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            #tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[0, 2000],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)


@app.callback(dash.dependencies.Output('right_arm_graph', 'figure'),
    [dash.dependencies.Input('right_arm_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['right_arm_risk'],
        x=dff['Time'],
        mode='lines+markers',
        name='Right arm risk',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    layout = Layout(
        #title= ' Left arm risk: ' + str(dff['left_arm_risk'].iloc[-1]),
        #font=dict(family='Courier New, monospace', size=5, color='#7f7f7f'),
        height = 200,
        width = 200,
        margin = {'l': 35, 'b': 8, 't': 20, 'r': 10},

        xaxis=dict(
            #title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            #tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[0, 2000],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)


@app.callback(dash.dependencies.Output('left_knee_graph', 'figure'),
    [dash.dependencies.Input('left_knee_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['left_knee_risk'],
        x=dff['Time'],
        mode='lines+markers',
        name='Left knee risk',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    layout = Layout(
        #title= ' Left arm risk: ' + str(dff['left_arm_risk'].iloc[-1]),
        #font=dict(family='Courier New, monospace', size=5, color='#7f7f7f'),
        height = 200,
        width = 200,
        margin = {'l': 35, 'b': 8, 't': 20, 'r': 10},

        xaxis=dict(
            #title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            #tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[0, 2000],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)


@app.callback(dash.dependencies.Output('right_knee_graph', 'figure'),
    [dash.dependencies.Input('right_knee_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['right_knee_risk'],
        x=dff['Time'],
        mode='lines+markers',
        name='Right knee risk',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    layout = Layout(
        #title= ' Left arm risk: ' + str(dff['left_arm_risk'].iloc[-1]),
        #font=dict(family='Courier New, monospace', size=5, color='#7f7f7f'),
        height = 200,
        width = 200,
        margin = {'l': 35, 'b': 8, 't': 20, 'r': 10},

        xaxis=dict(
            #title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            #tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[0, 2000],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)


@app.callback(dash.dependencies.Output('left_ankle_graph', 'figure'),
    [dash.dependencies.Input('left_ankle_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['left_ankle_risk'],
        x=dff['Time'],
        mode='lines+markers',
        name='Left ankle risk',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    layout = Layout(
        #title= ' Left arm risk: ' + str(dff['left_arm_risk'].iloc[-1]),
        #font=dict(family='Courier New, monospace', size=5, color='#7f7f7f'),
        height = 200,
        width = 200,
        margin = {'l': 35, 'b': 8, 't': 20, 'r': 10},

        xaxis=dict(
            #title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            #tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[0, 2000],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)



@app.callback(dash.dependencies.Output('right_ankle_graph', 'figure'),
    [dash.dependencies.Input('right_ankle_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour
    #total_time = (hour * 3600) + (minute * 60) + (sec)
    #title = '<b>{}'.format(player_name)

    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(100)))
    player_name = 'player1'
    dff = df_stream[df_stream['Name'] == player_name]


    trace = Scatter(
        y=dff['Playerload'],
        x=dff['Time'],
        fill='tozeroy',
        #mode='none',
        mode='lines',
        name='Player Load',
        line=dict(width=0.5, color='#2aa9d2'),
        marker=dict(
            color='#2aa9d2',
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    trace1 = Scatter(
        y=dff['right_ankle_risk'],
        x=dff['Time'],
        mode='lines+markers',
        name='Right ankle risk',
        line=dict(width=0.5, color='#f95959'),
        marker=dict(
            color='#f95959',
            size=2,
            line=dict(width=0.5)
        ),
        hoverinfo='skip')

    layout = Layout(
        #title= ' Left arm risk: ' + str(dff['left_arm_risk'].iloc[-1]),
        #font=dict(family='Courier New, monospace', size=5, color='#7f7f7f'),
        height = 200,
        width = 200,
        margin = {'l': 35, 'b': 8, 't': 20, 'r': 10},

        xaxis=dict(
            #title='Player Load:' + str(int(dff['Playerload'].iloc[-1])) + '(sec)',
            range=[dff['Time'].iloc[-1], dff['Time'].iloc[50]],
            showgrid=True,
            showline=True,
            zeroline=True,
            fixedrange=True,
            #tickvals=[dff['Time'].iloc[-1], dff['Time'].iloc[-25], dff['Time'].iloc[-50]],
            #ticktext=[dff['Time'].iloc[-1].dt.strftime('%Y/%m/%d'), dff['Time'].iloc[-25].dt.strftime('%Y/%m/%d'), dff['Time'].dt.strftime('%Y/%m/%d')],

        ),
        yaxis=dict(
            range=[0, 2000],
            showline=True,
            showgrid=True,
            zeroline=True,
            fixedrange=True,
            nticks=10),
    )

    return Figure(data=[trace, trace1], layout=layout)



@app.callback(dash.dependencies.Output('left_arm_image', 'style'),
    [dash.dependencies.Input('left_arm_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(1)))
    dff = df_stream.iloc[-1]["left_arm_risk"]

    style = {'top': '153px',
             'left': '109px',
             'position': 'absolute',
             'opacity': '0',
             }
    # if dff.iloc[0]["left_arm_risk"] > 300:
    if 320>dff>300:
        style['opacity'] = 0.3
    elif 340>dff>320:
        style['opacity'] = 0.7
    elif dff >340:
        style['opacity'] = 1
    return style

@app.callback(dash.dependencies.Output('right_arm_image', 'style'),
    [dash.dependencies.Input('right_arm_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(1)))
    dff = df_stream.iloc[-1]["right_arm_risk"]

    style = {'top': '156px',
             'left': '308px',
             'position': 'absolute',
             'opacity': '0',
             }
    if 420>dff>400:
        style['opacity'] = 0.3
    elif 440>dff>420:
        style['opacity'] = 0.7
    elif dff >440:
        style['opacity'] = 1
    return style

@app.callback(dash.dependencies.Output('left_knee_image', 'style'),
    [dash.dependencies.Input('left_knee_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(1)))
    dff = df_stream.iloc[-1]["left_knee_risk"]

    style = {'top': '389px',
             'left': '217px',
             'position': 'absolute',
             'opacity': '0',
             }
    if 420>dff>400:
        style['opacity'] = 0.3
    elif 440>dff>420:
        style['opacity'] = 0.7
    elif dff >440:
        style['opacity'] = 1
    return style

@app.callback(dash.dependencies.Output('right_knee_image', 'style'),
    [dash.dependencies.Input('right_knee_update', 'n_intervals'),
               ])
# dash.dependencies.Input('scatter-filter', 'hoverData')])
def gen_realtime_body(intervals):
    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(1)))
    dff = df_stream.iloc[-1]["right_knee_risk"]

    style = {'top': '389px',
             'left': '275px',
             'position': 'absolute',
             'opacity': '0',
             }
    if 470>dff>450:
        style['opacity'] = 0.3
    elif 490>dff>470:
        style['opacity'] = 0.7
    elif dff >490:
        style['opacity'] = 1
    return style


@app.callback(dash.dependencies.Output('left_ankle_image', 'style'),
    [dash.dependencies.Input('left_ankle_update', 'n_intervals'),])
def gen_realtime_body(intervals):
    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(1)))
    dff = df_stream.iloc[-1]["left_ankle_risk"]

    style = {'top': '500px',
             'left': '217px',
             'position': 'absolute',
             'opacity': '0',
             }
    if 390>dff>370:
        style['opacity'] = 0.3
    elif 410>dff>390:
        style['opacity'] = 0.7
    elif dff >410:
        style['opacity'] = 1
    return style


@app.callback(dash.dependencies.Output('right_ankle_image', 'style'),
    [dash.dependencies.Input('right_ankle_update', 'n_intervals'),])
def gen_realtime_body(intervals):
    df_stream = pd.DataFrame(list(db.body.find().sort([("_id", pymongo.DESCENDING)]).limit(1)))
    dff = df_stream.iloc[-1]["right_ankle_risk"]

    style = {'top': '500px',
             'left': '285px',
             'position': 'absolute',
             'opacity': '0',
             }
    if 320>dff>300:
        style['opacity'] = 0.3
    elif 340>dff>320:
        style['opacity'] = 0.7
    elif dff >340:
        style['opacity'] = 1
    return style


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })
