import json
import datetime


def load_data():
    # read the the json files
    data: list = []
    for i in range(0, 1):
        with open(f'data/{i}.json', 'r') as f:
            # read the file line by line and append to data
            while True:
                line = f.readline()
                if not line:
                    break
                data.append(json.loads(line))
    data.sort(key=lambda x: x['time_meas'])
    return data


def pack_data(outliers:list, data:list):
    packed_data = []
    for i in outliers:
        scenario_start = -1
        scenario_end = -1
        for j in range(0, len(data)):
            if data[j]['id'] == i and scenario_start == -1:
                scenario_start = j
            if data[j]['id'] == i and j > scenario_end:
                scenario_end = j
        if scenario_start == -1 or scenario_end == -1:
            return None
        packed_data.append([i, data[scenario_start:scenario_end+1]])
    print(len(packed_data))
    return packed_data