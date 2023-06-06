import numpy as np
import random


# transform the trajectories to the same length
def interpolation(trajectories: dict, length):
    for id_obj in trajectories.keys():
        if len(trajectories[id_obj]) < length:
            current_length = len(trajectories[id_obj])
            x = [i[0] for i in trajectories[id_obj]]
            y = [i[1] for i in trajectories[id_obj]]
            while current_length < length:
                index_to_insert = random.randint(1, current_length - 1)
                x.insert(index_to_insert, (x[index_to_insert - 1] + x[index_to_insert]) / 2)
                y.insert(index_to_insert, (y[index_to_insert - 1] + y[index_to_insert]) / 2)
                current_length += 1
            trajectories[id_obj] = [(x[i], y[i]) for i in range(0, length)]


# calculate the slope between two points
def slope(trajectories, length):
    slopes = dict()
    for id_obj in trajectories.keys():
        s = []
        x = [i[0] for i in trajectories[id_obj]]
        y = [i[1] for i in trajectories[id_obj]]
        for i in range(0, length):
            if x[i + 1] - x[i] == 0:
                s.append(0)
                continue
            s.append((y[i + 1] - y[i]) / (x[i + 1] - x[i]))
        slopes[id_obj] = s
    return slopes
