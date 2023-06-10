import json
import datetime


def load_data():
    # read the the json files
    data: list = []
    for i in range(0, 1):
        with open(f'data/title1/{i}.json', 'r') as f:
            # read the file line by line and append to data
            while True:
                line = f.readline()
                if not line:
                    break
                data.append(json.loads(line))
    data.sort(key=lambda x: x['time_meas'])
    return data


def pack_data(outliers: list, data: list, filtered: list):
    packed_data = []
    print(f"number of outliers: {len(outliers)}")
    for i in outliers:
        scenario_start_index = -1
        scenario_end_index = -1
        scenario_start_time_meas = -1
        scenario_end_time_meas = -1
        for j in range(0, len(data)):
            if (scenario_end_time_meas - scenario_start_time_meas) / 1000000 > 120:
                break
            if data[j]['id'] == i and scenario_start_time_meas == -1:
                scenario_start_time_meas = data[j]['time_meas']
                scenario_start_index = j
            if data[j]['id'] == i and data[j]['time_meas'] > scenario_end_time_meas:
                scenario_end_time_meas = data[j]['time_meas']
                scenario_end_index = j
        if scenario_start_index == -1 or scenario_end_index == -1:
            return None
        filtered_data = [record for record in data[scenario_start_index:scenario_end_index + 1] if
                         record['id'] in filtered]
        packed_data.append([i, filtered_data])
    return packed_data
