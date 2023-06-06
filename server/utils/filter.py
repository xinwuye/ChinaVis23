import json


class Filter:
    instance = None

    def __init__(self, data:list):
        if Filter.instance is None:
            instance = self
        else:
            self = Filter.instance
        self.data = data

    def filter_trajectory(self, is_in_area, lower_bound=10000, upper_bound=-1):
        trajectories = dict()
        for item in self.data:
            position = json.loads(item['position'])
            x = position['x']
            y = position['y']

            if is_in_area([x, y]) is False:
                continue

            if trajectories.get(item['id']) is None:
                trajectories[item['id']] = [(x, y)]
            else:
                trajectories[item['id']].append((x, y))

        filtered_trajectories = dict()
        for i in trajectories.keys():
            if len(trajectories[i]) > upper_bound or len(trajectories[i]) < lower_bound:
                continue
            filtered_trajectories[i] = trajectories[i]

        return filtered_trajectories

    def filter_velocity(self, is_in_area, lower_bound=10000, upper_bound=-1):
        if lower_bound <= 1:
            raise ValueError('lower_bound must be greater than 1')

        v = dict()
        for item in self.data:
            position = json.loads(item['position'])
            x = position['x']
            y = position['y']

            if is_in_area([x, y]) is False:
                continue

            if v.get(item['id']) is None:
                v[item['id']] = [(item['time_meas'] / 1000000, item['velocity'])]
            else:
                v[item['id']].append((item['time_meas'] / 1000000, item['velocity']))

        filtered_v = dict()
        for i in v.keys():
            if len(v[i]) > upper_bound or len(v[i]) < lower_bound:
                continue
            filtered_v[i] = v[i]

        return filtered_v
