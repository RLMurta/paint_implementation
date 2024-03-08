from .settings import *
import math

class Functions:
    def __init__(self):
        pass

    def move(self, x, y, dx, dy):
        return x + dx, y + dy

    def rotate(self, x, y, angle):
        new_x = x * math.cos(angle) - y * math.sin(angle)
        new_y = x * math.sin(angle) + y * math.cos(angle)
        return new_x, new_y

    def resize(self, x, y, scale_x, scale_y):
        return x * scale_x, y * scale_y

    def reflex(self, x, y, axis):
        new_x, new_y = self.to_cartesian_plane(x, y)
        if axis == "x":
                return self.to_screen_plane(-new_x - 1, new_y)
        elif axis == "y":
            return self.to_screen_plane(new_x, -new_y - 1)
        elif axis == "xy":
            return self.to_screen_plane(-new_x - 1, -new_y - 1)
        else:
            return x, y

    def dda(self, x1, y1, x2, y2):
        points = []
        dx, dy = x2 - x1, y2 - y1

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        x_inc, y_inc = dx / steps, dy / steps
        x, y = x1, y1
        points.append((x, y))
        for _ in range(steps):
            x += x_inc
            y += y_inc
            points.append((round(x), round(y)))
        return points

    def bres(self, x1, y1, x2, y2):
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
        points.append((x, y))

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
                points.append((x, y))
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
                points.append((x, y))
        return points

    def cohen_sutherland(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
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
            return [(int(x1), int(y1)), (int(x2), int(y2))]
        return None

    def liang_barsky(self, x1, y1, x2, y2, x_min, y_min, x_max, y_max):
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
                        return [(int(x1), int(y1)), (int(x2), int(y2))]

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

    def circle(self, xc, yc, r):
        points = []
        x, y, p = 0, r, 3 - 2*r
        points += self.get_circle_points(xc, yc, x, y)
        while x <= y:
            if p < 0:
                p += 4*x + 6
            else:
                y -= 1
                p += 4*(x - y) + 10
            x += 1
            points += self.get_circle_points(xc, yc, x, y)
        return points

    def get_circle_points(self, xc, yc, x, y):
        points = []
        points.append((xc + x, yc + y))
        points.append((xc - x, yc + y))
        points.append((xc + x, yc - y))
        points.append((xc - x, yc - y))
        points.append((xc + y, yc + x))
        points.append((xc - y, yc + x))
        points.append((xc + y, yc - x))
        points.append((xc - y, yc - x))
        return points

    def to_cartesian_plane(self, x, y):
        return int(x - COLS/2), int(y - ROWS/2)
    
    def to_screen_plane(self, x, y):
        return int(x + COLS/2), int(y + ROWS/2)
    
    def distance(self, x1, y1, x2, y2):
        return int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
