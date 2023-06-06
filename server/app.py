from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import networkx as nx
from networkx.readwrite import json_graph
import json
import os
from tqdm import tqdm
import sys
from services.area import CutLine, OneLineDividedArea, TwoLinesDividedArea, ClosedArea
from services.preprocessing import interpolation, slope
from services.kmeans import find_outliers
from utils.data_utils import load_data
from utils.filter import Filter
from services.acceleration import calculate_acceleration, sharp_change_accelerate

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

# define the areas
area_a = OneLineDividedArea([CutLine([-100, -210], [-60, -230])], 1)
area_b = TwoLinesDividedArea([CutLine([-60, -120], [-21, -142]), CutLine([-100, -210], [-60, -230])], 2)
area_c = ClosedArea(
    [CutLine([15, -100], [-50, -60]), CutLine([-80, -120], [-20, -160]), CutLine([-50, -60], [-20, -160]),
     CutLine([15, -100], [-80, -120])], 3)

data = load_data()
filterer = Filter(data)


def filter_by_area_and_length(filter_func, area_id: int, length_lower_bound: int = 5, length_upper_bound: int = 10):
    if filter_func.__self__.__class__.__name__ != 'Filter':
        raise TypeError('filter_func must be a Filter object')

    filtered = None
    if area_id == 1:
        filtered = filter_func(area_a.is_in_area, length_lower_bound, length_upper_bound)
    elif area_id == 2:
        filtered= filter_func(area_b.is_in_area, length_lower_bound, length_upper_bound)
    elif area_id == 3:
        filtered = filter_func(area_c.is_in_area, length_lower_bound, length_upper_bound)
    return filtered


@app.route("/outliers/auto", methods=['GET'])
def get_outliers_auto(area_id: int, length_lower_bound: int = 5, length_upper_bound: int = 10, cluster: int = 10,
                      outlier_threshold: float = 0.05):
    filtered_trajectories = filter_by_area_and_length(filterer.filter_trajectory, area_id, length_lower_bound, length_upper_bound)
    interpolation(filtered_trajectories, length_upper_bound + 1)
    slopes = slope(filtered_trajectories, length_upper_bound)
    outliers = find_outliers(slopes, cluster, outlier_threshold)
    return outliers


@app.route("/outliers/manual/acceleration", methods=['GET'])
def get_acceleration_auto(area_id: int, threshold:float, length_lower_bound: int = 5, length_upper_bound: int = 10):
    filtered_velocity = filter_by_area_and_length(filterer.filter_velocity, area_id, length_lower_bound, length_upper_bound)
    acceleration = calculate_acceleration(filtered_velocity)
    return sharp_change_accelerate(acceleration, threshold)


if __name__ == '__main__':
    path = 'data'
    with open(os.path.join(path, 'laneroad_with9road.geojson')) as f:
        laneroad_with9road = json.load(f)
    laneroad_with9road_features = laneroad_with9road['features']
    app.run(debug='True')