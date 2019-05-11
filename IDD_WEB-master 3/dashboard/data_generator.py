import pandas as pd
import random
import math
from datetime import datetime, timedelta
from random import randint
import time
import datetime as dt
import pymongo
from .train_data import data_trainer
from pymongo import MongoClient
# Example of Naive Bayes implemented from Scratch in Python

connection = MongoClient()
db = connection.get_database('sports')
collection = db.get_collection('injury')
collection2 = db.get_collection('body')
data_trainer1 = data_trainer()

df = pd.read_csv("sport.csv",encoding='utf-8')
df_stream = pd.read_csv("injury_stream.csv",encoding='utf-8')
df_stream.drop(df_stream.index, inplace=True)
df_stream.dropna(axis=0, inplace = True)
df_stream.dropna(axis=1, inplace = True)
df_stream.to_csv('injury_stream.csv', index=False)
summaries = {}


def stream_generator(player):
    # print ("generate a row injury")
    # name = player
    # time = dt.datetime.now()
    # playerload = 950 + int(random.uniform(-50, 100))
    # match_index = 45 + int(random.uniform(-10, 32))
    # match_time = 35 + int(random.uniform(-20, 8))
    # heartrate = 110 + int(random.uniform(-20, 10))
    # speed = 1.5 + random.uniform(-1, 3)
    #
    # inputVector = [playerload,speed,heartrate,match_index,match_time,'?']
    #
    # dic_threashold = data_trainer1.calculateClassProbabilities(summaries,inputVector)
    # threashold = 15
    # pa = dic_threashold[0.0]
    # pb = dic_threashold[1.0]
    #
    # k = float(1)/(pa + pb)
    # pa = pa * k * 100
    # # print("--------")
    # # print(pa)
    # # print(pb)
    # # print(k)
    #
    # row = {'Speed': speed, 'Name': name, 'Playerload': playerload, 'Threashold': round(pa,2), 'Match_time': match_time,
    #        'Heartrate': heartrate, 'Match_index': match_index, "Time": time}
    # return row
    time = dt.datetime.now()
    name = player
    playerload = 900 + random.uniform(-300, 200)
    if playerload < 1000:
        threashold = 0
    else:
        threashold = int((playerload - 800) / 8)
    speed = playerload / 2 + random.uniform(-50, 50)
    heartrate = int(playerload / 6)
    duration = 1

    row = {'Time': time, 'Name': name, 'Playerload': playerload, 'Threashold': threashold, 'Speed': speed,
           'Heartrate': heartrate, 'Duration': duration}
    return row


def get_predictor_ready():
    # print ("============================")
    filename = 'real_time_data.csv'
    splitRatio = 0.67
    dataset = data_trainer1.loadCsv(filename)
    trainingSet, testSet = data_trainer1.splitDataset(dataset, splitRatio)
    # print('Split {0} rows into train={1} and test={2} rows'.format(len(dataset), len(trainingSet), len(testSet)))
    # prepare model
    global summaries
    summaries = data_trainer1.summarizeByClass(trainingSet)
    # test model
    predictions = data_trainer1.getPredictions(summaries, testSet)
    accuracy = data_trainer1.getAccuracy(testSet, predictions)
    # print('Predictor Accuracy Based on Historical Data: {0}%'.format(accuracy))


def insert_data():
    #get_predictor_ready()
    name = 'player1'
    collection.delete_many({"Time": {"$lt": (dt.datetime.now() - timedelta(hours=1))}})
    collection2.delete_many({"Time": {"$lt": (dt.datetime.now() - timedelta(hours=1))}})

    for i in range(200):
        collection.insert_one(stream_generator(name))
        collection2.insert_one(body_stream_generator(name))

    for i in range(8000):
        collection.insert_one(stream_generator(name))
        collection2.insert_one(body_stream_generator(name))
        time.sleep(1)


def body_stream_generator(player):
    # name = player
    # time = dt.datetime.now()
    # playerload = preload + int(1 * random.uniform(1, 10))
    # left_arm_playload = playerload * (0.3+random.uniform(0, 0.1))
    # row = {'Name': name, 'Playerload': playerload, "left_arm_load": left_arm_playload, "Time": time}
    # #print (row)
    # return row
    time = dt.datetime.now()
    name = player
    playerload = 900 + random.uniform(-300, 200)
    if playerload < 1000:
        threashold = 0
    else:
        threashold = int((playerload - 800) / 8)

    left_arm_risk = (playerload + random.uniform(100, 200))*0.3
    # print(left_arm_risk)

    right_arm_risk = (playerload + random.uniform(300, 500))*0.3
    left_knee_risk = (playerload + random.uniform(300, 500))*0.3
    right_knee_risk = (playerload + random.uniform(500, 600))*0.3
    left_ankle_risk = (playerload + random.uniform(300, 400))*0.3
    right_ankle_risk = (playerload + random.uniform(100, 200))*0.3

    row = {'Time': time, 'Name': name,
           'Playerload': playerload,
            'left_arm_risk': left_arm_risk,
            'right_arm_risk': right_arm_risk,
            'left_knee_risk': left_knee_risk,
            'right_knee_risk': right_knee_risk,
            'left_ankle_risk': left_ankle_risk,
            'right_ankle_risk':right_ankle_risk}
    return row
