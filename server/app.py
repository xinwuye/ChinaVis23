from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import pickle
import networkx as nx
from networkx.readwrite import json_graph
import json
import os
from tqdm import tqdm
import sys

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/TrafficSituationViewInit', methods=['POST', 'GET'])
def traffic_situation_view_init():
    # read data/vis_mat.csv using numpy
    vis_mat = np.loadtxt('data/vis_mat.csv', delimiter=',')
    # absolute value of vis_mat
    vis_mat = np.abs(vis_mat)
    # caculate the min and max of vis_mat
    vis_mat_min = np.min(vis_mat)
    vis_mat_max = np.max(vis_mat)
    unique_fids = list(map(lambda x: x['properties']['fid'], laneroad_with9road_features))
    # convert vis_mat to list of list, each list represents a cell in the matrix.
    # the formate of each list is [row, col, value]
    vis_mat_list = [[i, j, vis_mat[i][j]] 
        for i in range(len(unique_fids)) 
        for j in range(len(unique_fids))
        if vis_mat[i][j] != 0]
    return jsonify({'vis_mat_list': vis_mat_list, 
                    'vis_mat_min': vis_mat_min, 
                    'vis_mat_max': vis_mat_max,
                    'unique_fids': unique_fids})

@app.route('/TrafficSituationViewRespond', methods=['POST', 'GET'])
def traffic_situation_view_respond():
    feat_names = [
                #   '#未识别', # 0
                  '#小型车辆',
                  '#行人',
                  '#非机动车',
                  '#卡车',
                #   '#厢式货车、面包车', # 5
                  '#客车',
                  '#静态物体',
                #   '#路牙', # 8
                #   '#锥桶', # 9
                  '#手推车、三轮车',
                #   '#信号灯', # 11
                  '#门、阀门、闸机、出入口',
                  '#停止车辆',
                  '#慢行车辆',
                  '#超速车辆',
                  '平均车速',
                  '交通参与者运动方向方差',
                  '交通参与者车头朝向方差',]
    fid = str(request.json['fid'])
    situation = np.load('data/situation/situation_' + fid + '.npy')
    ret = [[feat_names[j], i, situation[i, j]] 
           for i in range(situation.shape[0]) 
           for j in range(situation.shape[1])]

    n = len(feat_names)

    return jsonify({'situation': ret,
                    'n': n})


if __name__ == '__main__':
    path = 'data'
    with open(os.path.join(path, 'laneroad_with9road.geojson')) as f:
        laneroad_with9road = json.load(f)
    laneroad_with9road_features = laneroad_with9road['features']
    app.run(debug='True')