from .settings import *

class Functions:
    def __init__(self):
        pass

    def move(self, points, dx, dy):
        new_points = []
        for (x, y, color) in points:
            new_points.append((x + dx, y + dy, color))
        return new_points

    def rotate(self, points, angle):
        pass

    def resize(self, points, scale_x, scale_y):
        pass

    def reflex(self, points, axis):
        cartesian_points = self.to_cartesian_plane(points)
        new_points = []
        if axis == "x":
            for (x, y, color) in cartesian_points:
                new_points.append((x, -y, color))
        elif axis == "y":
            for (x, y, color) in cartesian_points:
                new_points.append((-x, y, color))
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

    def cohen_sutherland(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
        pass

    def lian_barsky(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
        pass

    def circle(self, x, y, r):
        pass

    def to_cartesian_plane(self, points):
        new_points = []
        for (x, y, color) in points:
            new_points.append((x - COLS/2, y - ROWS/2, color))
        return new_points
    
    def to_screen_plane(self, points):
        new_points = []
        for (x, y, color) in points:
            new_points.append((x + COLS/2, y + ROWS/2, color))
        return new_points
