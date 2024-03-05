from .settings import *
import math

class Functions:
    def __init__(self):
        pass

    def move(self, points, dx, dy):
        new_points = []
        for (x, y, color) in points:
            new_points.append((x + dx, y + dy, color))
        return new_points

    def rotate(self, points, angle):
        new_points = []
        for (x, y, color) in points:
            new_x = x * math.cos(angle) - y * math.sin(angle)
            new_y = x * math.sin(angle) + y * math.cos(angle)
            new_points.append((new_x, new_y, color))
        return new_points

    def resize(self, points, scale_x, scale_y):
        new_points = []
        for (x, y, color) in points:
            new_points.append((x * scale_x, y * scale_y, color))
        return new_points

    def reflex(self, points, axis):
        cartesian_points = self.to_cartesian_plane(points)
        new_points = []
        if axis == "x":
            for (x, y, color) in cartesian_points:
                new_points.append((-x - 1, y, color))
        elif axis == "y":
            for (x, y, color) in cartesian_points:
                new_points.append((x, -y - 1, color))
        else:
            return points
        return self.to_screen_plane(new_points)

    def dda(self, x1, y1, x2, y2, color):
        points = []
        dx, dy = x2 - x1, y2 - y1

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        x_inc, y_inc = dx / steps, dy / steps
        x, y = x1, y1
        points.append((x, y, color))
        for _ in range(steps):
            x += x_inc
            y += y_inc
            points.append((round(x), round(y), color))
        return points

    def bres(self, x1, y1, x2, y2, color):
        points = []
        dx, dy = x2 - x1, y2 - y1

        if dx >= 0:
            incrx = 1
        else:
            incrx = -1
            dx = -dx
        
        if dy >= 0:
            incry = 1
        else:
            incry = -1
            dy = -dy

        x, y = x1, y1
        points.append((x, y, color))

        if dx > dy:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for _ in range(dx):
                x += incrx
                if p < 0:
                    p += const1
                else:
                    y += incry
                    p += const2
                points.append((x, y, color))
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for _ in range(dy):
                y += incry
                if p < 0:
                    p += const1
                else:
                    x += incrx
                    p += const2
                points.append((x, y, color))
        return points

    def cohen_sutherland(self, pointa, pointb, x_min, y_min, x_max, y_max):
        x1, y1, colora = pointa
        x2, y2, colorb = pointb
        acept, done = False, False
        while not done:
            c1 = self.region_code(x1, y1, x_min, y_min, x_max, y_max)
            c2 = self.region_code(x2, y2, x_min, y_min, x_max, y_max)
            if c1 == 0 and c2 == 0:
                acept, done = True, True
            elif c1 & c2 != 0:
                done = True
            else:
                if c1 != 0:
                    c_out = c1
                else:
                    c_out = c2
                if c_out & 1:
                    xint = x_min
                    yint = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                elif c_out & 2:
                    xint = x_max
                    yint = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                elif c_out & 4:
                    yint = y_min
                    xint = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                elif c_out & 8:
                    yint = y_max
                    xint = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                if c_out == c1:
                    x1, y1 = xint, yint
                else:
                    x2, y2 = xint, yint
        if acept:
            return [(int(x1), int(y1), colora), (int(x2), int(y2), colorb)]
        return None

    def liang_barsky(self, pointa, pointb, x_min, y_min, x_max, y_max):
        x1, y1, colora = pointa
        x2, y2, colorb = pointb
        u1, u2 = 0, 1
        dx, dy = x2 - x1, y2 - y1
        clip_test, u1, u2 = self.clip_test(-dx, x1 - x_min, u1, u2)
        if clip_test:
            clip_test, u1, u2 = self.clip_test(dx, x_max - x1, u1, u2)
            if clip_test:
                clip_test, u1, u2 = self.clip_test(-dy, y1 - y_min, u1, u2)
                if clip_test:
                    clip_test, u1, u2 = self.clip_test(dy, y_max - y1, u1, u2)
                    if clip_test:
                        if u2 < 1:
                            x2 = x1 + u2 * dx
                            y2 = y1 + u2 * dy
                        if u1 > 0:
                            x1 = x1 + u1 * dx
                            y1 = y1 + u1 * dy
                        return [(int(x1), int(y1), colora), (int(x2), int(y2), colorb)]

    def clip_test(self, p, q, u1, u2):
        result = True
        if p < 0:
            r = q / p
            if r > u2:
                result = False
            elif r > u1:
                u1 = r
        elif p > 0:
            r = q / p
            if r < u1:
                result = False
            elif r < u2:
                u2 = r
        elif q < 0:
            result = False
        return result, u1, u2

    def region_code(self, x, y, x_min, y_min, x_max, y_max):
        code = 0
        if x < x_min:
            code += 1
        elif x > x_max:
            code += 2
        if y < y_min:
            code += 4
        elif y > y_max:
            code += 8
        return code

    def circle(self, xc, yc, r, color):
        points = []
        x, y, p = 0, r, 3 - 2*r
        points += self.get_circle_points(xc, yc, x, y, color)
        while x <= y:
            if p < 0:
                p += 4*x + 6
            else:
                y -= 1
                p += 4*(x - y) + 10
            x += 1
            points += self.get_circle_points(xc, yc, x, y, color)
        return points

    def get_circle_points(self, xc, yc, x, y, color):
        points = []
        points.append((xc + x, yc + y, color))
        points.append((xc - x, yc + y, color))
        points.append((xc + x, yc - y, color))
        points.append((xc - x, yc - y, color))
        points.append((xc + y, yc + x, color))
        points.append((xc - y, yc + x, color))
        points.append((xc + y, yc - x, color))
        points.append((xc - y, yc - x, color))
        return points

    def to_cartesian_plane(self, points):
        new_points = []
        for (x, y, color) in points:
            new_points.append((int(x - COLS/2), int(y - ROWS/2), color))
        return new_points
    
    def to_screen_plane(self, points):
        new_points = []
        for (x, y, color) in points:
            new_points.append((int(x + COLS/2), int(y + ROWS/2), color))
        return new_points
    
    def check_point(self, point, points):
        target_col, target_row = point[0], point[1]
        return [(col, row, color) for (col, row, color) in points if col == target_col and row == target_row]
    
    def distance(self, point1, point2):
        return int(math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2))
