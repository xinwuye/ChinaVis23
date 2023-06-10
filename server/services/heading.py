def calculate_heading_change(heading:dict):
    heading_change = dict()
    for i in heading.keys():
        heading_change[i] = []
        for j in range(1, len(heading[i])):
            if heading[i][j][0] - heading[i][j - 1][0] == 0:
                heading_change[i].append(0)
                continue
            heading_change[i].append((heading[i][j][1] - heading[i][j - 1][1])/(heading[i][j][0] - heading[i][j - 1][0]))
    return heading_change


def sharp_change_heading(heading_change:dict, threshold:float):
    outliers = []
    for id_obj in heading_change.keys():
        abs_heading_change = [abs(num) for num in heading_change[id_obj]]
        if max(abs_heading_change) > threshold:
            outliers.append(id_obj)
    return outliers
