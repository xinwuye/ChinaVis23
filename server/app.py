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
from services.kmeans import find_distances
from utils.data_utils import load_data, pack_data
from utils.filter import Filter
from services.acceleration import calculate_acceleration, sharp_change_accelerate
from services.heading import calculate_heading_change, sharp_change_heading

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

outliers = []
kmeans_dis_min = -1
kmeans_dis_max = -1
auto_filter_params = [-1, -1, -1, -1]
ids = []
distances = []
filtered_trajectories = {}


@app.route('/HeatmapViewInit', methods=['POST', 'GET'])
def heatmap_view_init():
    selected_data = request.json['selectedData']
    sub_path = 'title' + str(int(selected_data))
    # read data/vis_mat.csv using numpy
    # vis_mat = np.loadtxt('data/vis_mat.csv', delimiter=',')
    vis_mat = np.loadtxt(os.path.join(path, sub_path, 'vis_mat.csv'), delimiter=',')
    # absolute value of vis_mat
    vis_mat = np.abs(vis_mat)
    # caculate the min and max of vis_mat
    vis_mat_min = np.min(vis_mat)
    vis_mat_max = np.max(vis_mat)
    with open(os.path.join(path, sub_path, 'laneroad_with9road.geojson')) as f:
        laneroad_with9road = json.load(f)
    laneroad_with9road_features = laneroad_with9road['features']
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
                  '#未识别', # 0
                  '#小型车辆',
                  '#行人',
                  '#非机动车',
                  '#卡车',
                  '#厢式货车、面包车', # 5
                  '#客车',
                  '#静态物体',
                  '#路牙', # 8
                  '#锥桶', # 9
                  '#手推车、三轮车',
                  '#信号灯', # 11
                  '#门、阀门、闸机、出入口',
                  '#停止车辆',
                  '#慢行车辆',
                  '#超速车辆',
                  '平均车速',
                  '交通参与者运动方向方差',
                  '交通参与者车头朝向方差',]
    fid = str(request.json['fid'])
    selected_data = request.json['selectedData']
    sub_path = 'title' + str(int(selected_data))
    situation = np.load(os.path.join(path, sub_path, 'situation', 'situation_' + fid + '.npy'))
    ret = [[feat_names[j], i, situation[i, j]] 
           for i in range(situation.shape[0]) 
           for j in range(situation.shape[1])]

    n = len(feat_names)

    return jsonify({'situation': ret,
                    'n': n})


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
        filtered = filter_func(area_b.is_in_area, length_lower_bound, length_upper_bound)
    elif area_id == 3:
        filtered = filter_func(area_c.is_in_area, length_lower_bound, length_upper_bound)
    return filtered


@app.route('/outliers/auto', methods=['GET'])
def get_outliers_auto():
    global outliers
    global kmeans_dis_min
    global kmeans_dis_max
    global ids
    global distances
    global auto_filter_params
    global filtered_trajectories
    area_id = int(request.args.get('area_id', 1))
    length_lower_bound = int(request.args.get('length_lower_bound', 5))
    length_upper_bound = int(request.args.get('length_upper_bound', 10))
    cluster = int(request.args.get('cluster', 10))
    outlier_threshold = float(request.args.get('outlier_threshold', 1))

    if [area_id, length_lower_bound, length_upper_bound, cluster] != auto_filter_params:
        filtered_trajectories = filter_by_area_and_length(filterer.filter_trajectory, area_id, length_lower_bound,
                                                          length_upper_bound)
        if filtered_trajectories is None:
            filtered_trajectories = {}

        interpolation(filtered_trajectories, length_upper_bound + 1)
        slopes = slope(filtered_trajectories, length_upper_bound)
        ids, distances = find_distances(slopes, cluster, outlier_threshold)
        kmeans_dis_min = np.min(distances[0])
        kmeans_dis_max = np.max(distances[0])

    auto_filter_params = [area_id, length_lower_bound, length_upper_bound, cluster]

    outliers = [ids[i] for i, dist in enumerate(distances[0]) if dist > outlier_threshold]

    if len(outliers) > 50:
        return {"error": 1, "data": []}
    elif len(outliers) == 0:
        return {"error": 2, "data": []}
    else:
        return {"error": 0, "data": pack_data(outliers, data, filtered_trajectories.keys())}


@app.route('/outliers/auto/distance_range', methods=['GET'])
def get_distance_range():
    print(kmeans_dis_min, kmeans_dis_max)
    return [float(kmeans_dis_min), float(kmeans_dis_max)]


@app.route('/outliers/manual/acceleration', methods=['GET'])
def get_acceleration_auto():
    area_id = int(request.args.get('area_id', 1))
    threshold = float(request.args.get('threshold', 0.5))
    length_lower_bound = int(request.args.get('length_lower_bound', 5))
    length_upper_bound = int(request.args.get('length_upper_bound', 10))

    filtered_velocity = filter_by_area_and_length(filterer.filter_velocity, area_id, length_lower_bound,
                                                  length_upper_bound)
    acceleration= calculate_acceleration(filtered_velocity)

    outliers = sharp_change_accelerate(acceleration, threshold)

    if len(outliers) > 50:
        return {"error": 1, "data": []}
    elif len(outliers) == 0:
        return {"error": 2, "data": []}
    else:
        return {"error": 0, "data": pack_data(outliers ,data, filtered_velocity.keys())}


@app.route('/outliers/manual/heading', methods=['GET'])
def get_heading_auto():
    area_id = int(request.args.get('area_id', 1))
    threshold = float(request.args.get('threshold', 0.5))
    length_lower_bound = int(request.args.get('length_lower_bound', 5))
    length_upper_bound = int(request.args.get('length_upper_bound', 10))

    filtered_heading = filter_by_area_and_length(filterer.filter_heading, area_id, length_lower_bound,
                                                  length_upper_bound)
    heading_change = calculate_heading_change(filtered_heading)

    outliers = sharp_change_heading(heading_change, threshold)

    print(outliers)

    if len(outliers) > 50:
        return {"error": 1, "data": []}
    elif len(outliers) == 0:
        return {"error": 2, "data": []}
    else:
        return {"error": 0, "data": pack_data(outliers ,data, filtered_heading.keys())}


index_of_ID = 2


@app.route('/MetricView', methods=['POST', 'GET'])
def Metric_view_init():
    # read data
    parameter = pd.read_csv('data/Parameter.csv')
    id = str(parameter['id'][index_of_ID])  #int类型会报错
    mean_velocity = parameter['mean_velocity'][index_of_ID]
    max_velocity = parameter['max_velocity'][index_of_ID]
    sd_velocity = parameter['sd_velocity'][index_of_ID]
    per_time_in_0_10 = parameter['per_time_in_0_10'][index_of_ID]
    per_time_in_10_20 = parameter['per_time_in_10_20'][index_of_ID]
    per_time_in_20_30 = parameter['per_time_in_20_30'][index_of_ID]
    per_time_in_30_ = parameter['per_time_in_30_'][index_of_ID]
    mean_acceleration = parameter['mean_acceleration'][index_of_ID]
    std_acceleration = parameter['std_acceleration'][index_of_ID]
    quick_acceleration = str(parameter['quick_acceleration'][index_of_ID])
    quick_deceleration = str(parameter['quick_deceleration'][index_of_ID])

    return jsonify({'id': id, 'mean_velocity': mean_velocity, 'max_velocity': max_velocity,
                    'sd_velocity': sd_velocity, 'per_time_in_0_10': per_time_in_0_10,
                    'per_time_in_10_20': per_time_in_10_20, 'per_time_in_20_30': per_time_in_20_30,
                    'per_time_in_30_': per_time_in_30_, 'mean_acceleration': mean_acceleration,
                    'std_acceleration': std_acceleration, 'quick_acceleration': quick_acceleration,
                    'quick_deceleration': quick_deceleration})


@app.route('/HistoryView', methods=['POST', 'GET'])
def Hitory_view_init():
    velocity = pd.read_csv('data/Velocity.csv')
    id = str(velocity['id'][index_of_ID])
    vplot = velocity['vplot'][index_of_ID]
    vtime = velocity['vtime'][index_of_ID]
    aplot = velocity['aplot'][index_of_ID]
    orientation = velocity['orientation'][index_of_ID]

    return jsonify({'id': id, 'vplot':vplot, 'vtime':vtime, 'aplot':aplot
                    , 'orientation':orientation})


if __name__ == '__main__':
    path = 'data'
    app.run(host="localhost", debug='True')
