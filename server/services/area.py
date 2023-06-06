import numpy as np


class CutLine:
    def __init__(self, point1: list, point2: list):
        self.point1 = np.array(point1)
        self.point2 = np.array(point2)
        self.k = (self.point2[1] - self.point1[1]) / (self.point2[0] - self.point1[0])
        self.b = self.point1[1] - self.k * self.point1[0]


class Area:
    def __init__(self, cut_lines: list, area_id: int):
        self.cut_lines = cut_lines
        self.area_id = area_id

    def is_in_area(self, point: list):
        pass


class OneLineDividedArea(Area):
    def __init__(self, cut_lines: list, area_id: int, up_line=False):
        super().__init__(cut_lines, area_id)
        self.up_line = up_line

    def is_in_area(self, point: list):
        if not self.up_line and self.cut_lines[0].k * point[0] + self.cut_lines[0].b >= point[1]:
            return True
        if self.up_line and self.cut_lines[0].k * point[0] + self.cut_lines[0].b <= point[1]:
            return True
        return False


class TwoLinesDividedArea(Area):
    def __init__(self, cut_lines: list, area_id: int):
        super().__init__(cut_lines, area_id)

    def is_in_area(self, point: list):
        upper_bound = self.cut_lines[0].k * point[0] + self.cut_lines[0].b >= point[1]

        lower_bound = self.cut_lines[1].k * point[0] + self.cut_lines[1].b <= point[1]

        if upper_bound and lower_bound:
            return True
        return False


class ClosedArea(Area):
    def __init__(self, cut_lines: list, area_id: int):
        super().__init__(cut_lines, area_id)

    def is_in_area(self, point: list):
        upper_bound = self.cut_lines[0].k * point[0] + self.cut_lines[0].b >= point[1]

        lower_bound = self.cut_lines[1].k * point[0] + self.cut_lines[1].b <= point[1]

        left_and_right_bound = (self.cut_lines[2].k * point[0] + self.cut_lines[2].b - point[1]) * (self.cut_lines[3].k * point[0] + self.cut_lines[3].b - point[1]) <= 0

        if upper_bound and lower_bound and left_and_right_bound:
            return True
        return False

