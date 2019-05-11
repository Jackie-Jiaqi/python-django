import dash_core_components as dcc
import dash_html_components as html
from .models import Author
from django.shortcuts import get_object_or_404
import pandas as pd
import plotly.graph_objs as go
import numpy as np
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
import os
from datetime import datetime, timedelta
import datetime as dt
import random
from random import randint
import time
import pymongo
from pymongo import MongoClient


team_team_df = pd.read_csv('game_data.csv')

date_list = {0:pd.to_datetime("2015-11-01"),
             1:pd.to_datetime("2015-12-01"),
             2:pd.to_datetime("2016-01-01"),
             3:pd.to_datetime("2016-02-01"),
             4:pd.to_datetime("2016-03-01")}

team_team_df = team_team_df[team_team_df['period.name'] == 'Session']
team_team_df.date = pd.to_datetime(team_team_df.date,dayfirst=True)
player_name_list = list(team_team_df['player.name'].unique())
#print(player_name_list)

df = pd.read_csv('sport.csv')
df = df[df['game.or.practice'] == 1]
df = df.sort_values('date').reset_index(drop=True)
date_slider = df['date'].tolist()
indicators = df['period.name'].unique()
indicators1 = df['player.name'].unique()
game_indicators = ['TP', 'FGA', 'FGA3PT', 'FTA', 'TO', 'duration']
player_indicators = df.columns



def playerload_layout(pathname):
    # Here we extract context from the url in order to render relevant data:
    pathelements = pathname.split('/')
    for count, element in enumerate(pathelements):
        if element == 'playerload':
            break
    record_id = pathelements[count - 1]

    author = get_object_or_404(Author, pk=record_id)

    # message = html.P("ID: %s  |   Inspector: %s" %(record_id, author.name))
    message = html.P('')
    playerload_layout = [message, html.Div([
        html.Div([
            dcc.Graph(
                id='playerload1'),
        ], style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            html.H2("Player Name"),
        ], style={ 'float':'left'
                  }),
        html.Div([
            dcc.Dropdown(
                id='playerload_dropdown',
                options=[{'label': i, 'value': i} for i in player_name_list],
                # value='player.name'player_name_list
            )], style={'width': '30%'}),

    ])]
    return playerload_layout

def team_layout(pathname):
    # Here we extract context from the url in order to render relevant data:
    pathelements = pathname.split('/')
    for count, element in enumerate(pathelements):
        if element == 'team':
            break
    record_id = pathelements[count-1]

    author = get_object_or_404(Author, pk=record_id)

    #message = html.P("ID: %s  |   Inspector: %s" %(record_id, author.name))
    message = html.P('')

    team_layout = [message, html.Div([
    html.Div([
        html.Div([
            html.H2("PLAYER AND TEAM PERFORMANCE COMPARISON"),
        ], style={'background-color': '#2aa9d2', 'color': 'white', 'border-radius': '2px',
                  'padding': '10px 0px 10px 10px'}),
        html.Div([
            dcc.Graph(
                id='g1'),
                ], style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='g3'),
                ], style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
            id='g2'),
            ], style={'width': '34%', 'float': 'right', 'display': 'inline-block'}),
    ]),

    html.Div([
            html.Div(
            [
                dcc.RangeSlider(
                    id='slider_1',
                    marks={i: '{}'.format(month) for i, month in enumerate(["Nov 2015","Dec 2015",'Jan 2015','Feb 2016','Mar 2016'])},
                    min=0,
                    max=4,
                    value=[0, 4],
                    step=None,
                )
            ],
                style={'display': 'inline-block','width': '100%',  'float': 'left', 'marginBottom':50,},
            ),

            html.Div([
            dcc.RadioItems(
                id='home_away_1',
                options=[{'label': "Host", 'value': 0}, {'label': 'Guest', 'value': 1}],
                value=0,
                labelStyle={'display': 'inline-block'}
            ),],
                style={'display': 'inline-block', 'float': 'none', 'margin':'auto'},),

            html.Div([
            dcc.Checklist(
                id='Player_name_1',
                options=[{'label': i, 'value': i} for i in player_name_list],
                values=['Cheatham Hannif'],
                labelStyle={'display': 'inline-block'}
            )],
                style={'display': 'inline-block', 'float': 'right',  'margin':'auto'},),
        ],
            style={'marginTop': 50, 'width': '45%', 'float': 'left', 'display': 'inline-block', 'padding': '0px 0px 100px 40px', 'font-size': '16px'},
        ),

        html.Div([
            html.Div([
            dcc.RangeSlider(
                id='slider_2',
                marks={i:'{}'.format(month) for i,month in enumerate(["Nov 2015","Dec 2015",'Jan 2015','Feb 2016','Mar 2016'])},
                min=0,
                max=4,
                value=[0, 4]
            ),],
                style={'display': 'inline-block','width': '100%',  'float': 'middle', 'marginBottom':50, },),

            html.Div([
            dcc.RadioItems(
                id='home_away_2',
                options=[{'label': "Host", 'value': 0}, {'label': "Guest", 'value': 1}],
                value=0,
                labelStyle={'display': 'inline-block'}
            ),],
                style={'display': 'inline-block', 'width': '30%', 'float': 'left', 'margin':'auto'},),

            html.Div([
            dcc.Checklist(
                id='Player_name_2',
                options=[{'label': i, 'value': i} for i in player_name_list],
                values=['Henry Ellenson']
            )],
                style={'display': 'inline-block', 'float': 'right', 'width': '100%', 'margin':'auto'},),
        ],
            style={'marginTop': 50, 'width': '45%', 'float': 'right', 'display': 'inline-block', 'padding': '0px 40px 100px 50px', 'font-size': '16px'})


],style={'width': '100%', 'float': 'left', 'marginLeft': 'auto', 'marginRight': 'auto', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})]

    return team_layout

def player_layout(pathname):

    # Here we extract context from the url in order to render relevant data:
    pathelements = pathname.split('/')
    for count, element in enumerate(pathelements):
        if element == 'player':
            break
    record_id = pathelements[count-1]

    author = get_object_or_404(Author, pk=record_id)

    message = html.P("From the URL, I am record: %s. This corresponds to author: %s. Info relevant to this record can be extracted\
                       from a database" %(record_id, author.name))


    # Create random data with numpy
    player_layout = html.Div([
        # html.Link(
        #   rel='stylesheet',
        #    href='/static/sport_analytics.css'
        # ),
        # html.Link(
        #   rel='stylesheet',
        #   href='/static/skeleton.min.css'
        # ),
        html.Div([
            html.H2("PLAYER ANALYTICS"),
        ], style={'background-color': '#2aa9d2', 'color': 'white', 'border-radius': '2px',
                  'padding': '10px 0px 10px 10px'}),

        html.Div([
            html.Div([  # block 1 left
                html.Div([
                    html.Div([
                        html.P("PLAY PERFORMANCE")],
                        style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2', 'width': '30%',
                               'float': 'left'}),
                    html.Div([
                        dcc.Dropdown(
                            id='player-data-filter',
                            options=[{'label': i, 'value': i} for i in game_indicators],
                            value='TP'
                        )], style={'width': '70%', 'float': 'right'}),
                    html.Div([
                        dcc.RadioItems(
                            id='player-data-filter-type',
                            options=[{'label': i, 'value': i} for i in ['Line', 'Scatter']],
                            value='Line',
                            labelStyle={'display': 'inline-block'})]),
                ], style={'font-size': '12px', 'font-weight': 'bold',
                          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                          'padding': '10px 0px 0px 10px'}
                ),

                html.Div([
                    html.Div([
                        dcc.Graph(id='performance-metrics')],
                    )], style={'font-size': '12px', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
                ),

                html.Div([
                    html.Div([
                        html.P('REAL_TIME INJURY MONITOR'),
                    ], style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2'}
                    ),
                    dcc.Graph(
                        id='realtime-injury',
                    ),
                    dcc.Interval(id='realtime-injury-update', interval=1000, n_intervals=0),
                ], style={'font-size': '12px', 'color': '#2aa9d2',
                          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)', 'padding': '10px 10px 10px 10px'}
                ),
            ]),

        ], style={'width': '52%', 'float': 'left', 'marginLeft': 'auto', 'marginRight': 'auto',
                  'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),

        html.Div([
            html.Div([
                html.Div([
                    html.P('SELECT PLAYER')],
                    style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2', 'float': 'left',
                           'padding': '10px 0px 0px 10px'}),
                html.Div([
                    dcc.Graph(
                        id='scatter-filter',
                        hoverData={'points': [{'customdata': 'Traci Carter'}]}
                    )], style={'padding': '60px 0px 0px 0px'})
            ]),

            html.Div([
                html.Div([
                    html.P("GAME PERIODS")],
                    style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2', 'width': '30%',
                           'float': 'left'}),
                html.Div([
                    dcc.Dropdown(
                        id='period-filter',
                        options=[{'label': i, 'value': i} for i in indicators],
                        value='Session'
                    )], style={'width': '70%', 'float': 'right'}),
                html.Div([
                    dcc.RadioItems(
                        id='period-filter-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'})]),
            ], style={'font-size': '12px', 'font-weight': 'bold', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                      'padding': '39px 0px 0px 10px'}
            ),

            html.Div([
                dcc.Graph(id='player-load')],
                style={'font-size': '1.5rem', 'marginLeft': 'auto', 'marginRight': 'auto',
                       'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
            ),

        ], style={'width': '47%', 'float': 'right', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),

    ], style={'font-family': 'Verdana', 'padding': '0px 0px 0px 0px',
              'marginLeft': 'auto', 'marginRight': 'auto', "width": "1200px",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})

    return player_layout

def body_layout(pathname):
    pathelements = pathname.split('/')
    for count, element in enumerate(pathelements):
        if element == 'body':
            break
    record_id = pathelements[count - 1]
    author = get_object_or_404(Author, pk=record_id)
    message = html.P('')
    body_image_path = '/static/images/body.png'
    arm_image_path = '/static/images/arm.png'
    body_layout = [message, html.Div([
        html.Div([
            html.Div([
                html.H2("PLAYER BODY ANALYSIS"),
            ], style={'background-color': '#2aa9d2', 'color': 'white', 'border-radius': '2px',
                      'padding': '10px 0px 10px 10px'}),
            html.Div([

                html.Img(src=body_image_path, id='body_image'),
                # style={'position': 'relative', 'top': '0', 'left': '0'}),
                html.Img(src='/static/images/info1.png', id='info_image',
                         style={
                             'width': '110px',
                             'height': '270px',
                             'position': 'absolute',
                             'top': '73px',
                             'left': '30px',

                         }),
                html.Img(src='/static/images/left_arm.png', id='left_arm_image',
                         style={
                             'position': 'absolute',
                             'top': '153px',
                             'left': '109px',
                             'opacity': '0'
                         }),
                html.Img(src='/static/images/right_arm.png', id='right_arm_image',
                         style={
                             'position': 'absolute',
                             'top': '156px',
                             'left': '308px',
                             'opacity': '0'
                         }),
                html.Img(src='/static/images/left_knee.png', id='left_knee_image',
                         style={
                             'position': 'absolute',
                             'top': '389px',
                             'left': '217px',
                             'opacity': '0'
                         }),
                html.Img(src='/static/images/right_knee.png', id='right_knee_image',
                         style={
                             'position': 'absolute',
                             'top': '389px',
                             'left': '275px',
                             'opacity': '0.5'
                         }),
                html.Img(src='/static/images/left_ankle.png', id='left_ankle_image',
                         style={
                             'position': 'absolute',
                             'top': '500px',
                             'left': '217px',
                             'opacity': '0.5'
                         }),
                html.Img(src='/static/images/right_ankle.png', id='right_ankle_image',
                         style={
                             'position': 'absolute',
                             'top': '500px',
                             'left': '285px',
                             'opacity': '0.5'
                         }),

            ],style={'width': '40%', 'float': 'left', 'display': 'inline-block'}
            # style="position: relative; overflow: auto; width: 100; height: 100;"
            ),

            html.Div([
                html.Div([
                    html.H2("Left Arm Injury Risk"),
                    dcc.Graph(
                        id='left_arm_graph',
                        figure={
                            'layout': {
                                'height': 200,
                                'width': 200,
                                'display': 'inline-block',
                                'margin': {'l': 35, 'b': 8, 't': 20, 'r': 10}
                            }
                        }),
                    dcc.Interval(id='left_arm_update', interval=500, n_intervals=0.3),
                ]),
                html.Div([
                    html.H2("Right Arm Injury Risk"),
                    dcc.Graph(
                        id='right_arm_graph',
                        figure={
                            'layout': {
                                'height': 200,
                                'width': 200,
                                'display': 'inline-block',
                                'margin': {'l': 35, 'b': 8, 't': 20, 'r': 10}
                            }
                        }),
                    dcc.Interval(id='right_arm_update', interval=1000, n_intervals=0),
                ]),

                    ],style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),

            html.Div([
                html.Div([
                    html.H2("Left Knee Injury Risk"),
                    dcc.Graph(
                        id='left_knee_graph',
                        figure={
                            'layout': {
                                'height': 200,
                                'width': 200,
                                'display': 'inline-block',
                                'margin': {'l': 35, 'b': 8, 't': 20, 'r': 10}
                            }
                        }),
                    dcc.Interval(id='left_knee_update', interval=1000, n_intervals=0),
                ]),
                html.Div([
                    html.H2("Right Knee Injury Risk"),
                    dcc.Graph(
                        id='right_knee_graph',
                        figure={
                            'layout': {
                                'height': 200,
                                'width': 200,
                                'display': 'inline-block',
                                'margin': {'l': 35, 'b': 8, 't': 20, 'r': 10}
                            }
                        }),
                    dcc.Interval(id='right_knee_update', interval=1000, n_intervals=0),
                ]),
            ], style={ 'width':'20%','float': 'left', 'display': 'inline-block'}),
            html.Div([
                html.Div([
                    html.H2("Left Ankle Injury Risk"),
                    dcc.Graph(
                        id='left_ankle_graph',
                        figure={
                            'layout': {
                                'height': 200,
                                'width': 200,
                                'display': 'inline-block',
                                'margin': {'l': 35, 'b': 8, 't': 20, 'r': 10}
                            }
                        }),
                    dcc.Interval(id='left_ankle_update', interval=1000, n_intervals=0),
                ]),
                html.Div([
                    html.H2("Right Ankle Injury risk"),
                    dcc.Graph(
                        id='right_ankle_graph',
                        figure={
                            'layout': {
                                'height': 200,
                                'width': 200,
                                'display': 'inline-block',
                                'margin': {'l': 35, 'b': 8, 't': 20, 'r': 10}
                            }
                        }),
                    dcc.Interval(id='right_ankle_update', interval=1000, n_intervals=0),
                ]),
            ], style={'width': '20%', 'float': 'left', 'display': 'inline-block'})

    ]),
    ], style={'width': '100%', 'float': 'left', 'marginLeft': 'auto', 'marginRight': 'auto', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})]

    return body_layout



# def body_layout(pathname):
#
#     # Here we extract context from the url in order to render relevant data:
#     pathelements = pathname.split('/')
#     for count, element in enumerate(pathelements):
#         if element == 'body':
#             break
#     record_id = pathelements[count-1]
#
#     author = get_object_or_404(Author, pk=record_id)
#
#     message = html.P("From the URL, I am record: %s. This corresponds to author: %s. Info relevant to this record can be extracted\
#                        from a database" %(record_id, author.name))
#
#     # Create random data with numpy
#     body_layout = html.Div([
#         # html.Link(
#         #   rel='stylesheet',
#         #    href='/static/sport_analytics.css'
#         # ),
#         # html.Link(
#         #   rel='stylesheet',
#         #   href='/static/skeleton.min.css'
#         # ),
#         html.Div([
#             html.H2("PLAYER ANALYTICS"),
#         ], style={'background-color': '#2aa9d2', 'color': 'white', 'border-radius': '2px',
#                   'padding': '10px 0px 10px 10px'}),
#
#         html.Div([
#             html.Div([  # block 1 left
#                 html.Div([
#                     html.Div([
#                         html.P("PLAY PERFORMANCE")],
#                         style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2', 'width': '30%',
#                                'float': 'left'}),
#                     html.Div([
#                         dcc.Dropdown(
#                             id='player-data-filter',
#                             options=[{'label': i, 'value': i} for i in game_indicators],
#                             value='TP'
#                         )], style={'width': '70%', 'float': 'right'}),
#                     html.Div([
#                         dcc.RadioItems(
#                             id='player-data-filter-type',
#                             options=[{'label': i, 'value': i} for i in ['Line', 'Scatter']],
#                             value='Line',
#                             labelStyle={'display': 'inline-block'})]),
#                 ], style={'font-size': '12px', 'font-weight': 'bold',
#                           'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
#                           'padding': '10px 0px 0px 10px'}
#                 ),
#
#                 html.Div([
#                     html.Div([
#                         dcc.Graph(id='performance-metrics')],
#                     )], style={'font-size': '12px', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
#                 ),
#
#                 html.Div([
#                     html.Div([
#                         html.P('REAL_TIME INJURY MONITOR'),
#                     ], style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2'}
#                     ),
#                     dcc.Graph(
#                         id='realtime-body',
#                     ),
#                     dcc.Interval(id='realtime-body-update', interval=1000, n_intervals=0),
#                 ], style={'font-size': '12px', 'color': '#2aa9d2',
#                           'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)', 'padding': '10px 10px 10px 10px'}
#                 ),
#             ]),
#
#         ], style={'width': '52%', 'float': 'left', 'marginLeft': 'auto', 'marginRight': 'auto',
#                   'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),
#
#         html.Div([
#             html.Div([
#                 html.Div([
#                     html.P('SELECT PLAYER')],
#                     style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2', 'float': 'left',
#                            'padding': '10px 0px 0px 10px'}),
#                 html.Div([
#                     dcc.Graph(
#                         id='scatter-filter',
#                         hoverData={'points': [{'customdata': 'Traci Carter'}]}
#                     )], style={'padding': '60px 0px 0px 0px'})
#             ]),
#
#             html.Div([
#                 html.Div([
#                     html.P("GAME PERIODS")],
#                     style={'font-size': '12px', 'font-weight': 'bold', 'color': '#2aa9d2', 'width': '30%',
#                            'float': 'left'}),
#                 html.Div([
#                     dcc.Dropdown(
#                         id='period-filter',
#                         options=[{'label': i, 'value': i} for i in indicators],
#                         value='Session'
#                     )], style={'width': '70%', 'float': 'right'}),
#                 html.Div([
#                     dcc.RadioItems(
#                         id='period-filter-type',
#                         options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                         value='Linear',
#                         labelStyle={'display': 'inline-block'})]),
#             ], style={'font-size': '12px', 'font-weight': 'bold', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
#                       'padding': '39px 0px 0px 10px'}
#             ),
#
#             html.Div([
#                 dcc.Graph(id='player-load')],
#                 style={'font-size': '1.5rem', 'marginLeft': 'auto', 'marginRight': 'auto',
#                        'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
#             ),
#
#         ], style={'width': '47%', 'float': 'right', 'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),
#
#     ], style={'font-family': 'Verdana', 'padding': '0px 0px 0px 0px',
#               'marginLeft': 'auto', 'marginRight': 'auto', "width": "1200px",
#               'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})
#
#     return body_layout
