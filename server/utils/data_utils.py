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
