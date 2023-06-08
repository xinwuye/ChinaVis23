import numpy as np


def calculate_acceleration(velocity:dict):
    acceleration = dict()
    for i in velocity.keys():
        acceleration[i] = []
        for j in range(1, len(velocity[i])):
            if velocity[i][j][0] - velocity[i][j - 1][0] == 0:
                acceleration[i].append(0)
                continue
            acceleration[i].append((velocity[i][j][1] - velocity[i][j - 1][1])/(velocity[i][j][0] - velocity[i][j - 1][0]))
    return acceleration


def sharp_change_accelerate(acceleration:dict, threshold:float):
    outliers = []
    for id_obj in acceleration.keys():
        abs_acceleration = [abs(num) for num in acceleration[id_obj]]
        if max(abs_acceleration) > threshold:
            outliers.append(id_obj)
    return outliers
