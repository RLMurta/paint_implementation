class Functions:
    def __init__(self):
        pass

    def move(self, points, dx, dy):
        pass

    def rotate(self, points, angle):
        pass

    def resize(self, points, scale_x, scale_y):
        pass

    def reflex(self, points, axis):
        pass

    def dda(self, x1, y1, x2, y2, color):
        points = []
        dx = x2 - x1
        dy = y2 - y1

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

    def bres(self, x1, y1, x2, y2):
        pass

    def cohen_sutherland(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
        pass

    def lian_barsky(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
        pass

    def circle(self, x, y, r):
        pass
