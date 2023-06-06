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


if __name__ == '__main__':
    path = 'data'
    with open(os.path.join(path, 'laneroad_with9road.geojson')) as f:
        laneroad_with9road = json.load(f)
    laneroad_with9road_features = laneroad_with9road['features']
    app.run(debug='True')