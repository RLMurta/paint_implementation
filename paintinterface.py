from utils import *

class PaintInterface:
    # Initilize the window and the canvas
    def __init__(self):
        # Create a 2D array to store the state of each pixel (on/off)
        self.pixels = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        # Saves the points, lines and circles positions
        self.line_algorithm = DDA
        self.point_list = []
        self.line_list = []
        self.circle_list = []
        self.window = Tk()
        self.window.title("Paint")
        self.canvas = Canvas(self.window, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()
        self.functions = Functions()
        # Create a variable to store the position of the last 2 clicks
        self.pointa = None
        self.pointb = None

        # Create a menu bar
        self.menubar = Menu(self.window)

        # Create a transformations menu and add it to the menu bar
        transformations_menu = Menu(self.menubar, tearoff=0)
        transformations_menu.add_command(label="Line Translation", command=self.line_translation)
        transformations_menu.add_command(label="Rotation", command=self.rotation)
        transformations_menu.add_command(label="Scale", command=self.scale)
        transformations_menu.add_command(label="Reflection X", command=self.reflection_x)
        transformations_menu.add_command(label="Reflection Y", command=self.reflection_y)
        transformations_menu.add_command(label="Reflection XY", command=self.reflection_xy)
        self.menubar.add_cascade(label="Transformations", menu=transformations_menu)

        # Create a rasterization menu and add it to the menu bar
        rasterization_menu = Menu(self.menubar, tearoff=0)
        rasterization_menu.add_command(label="DDA Line", command=self.dda)
        rasterization_menu.add_command(label="Bresenham Line", command=self.bresenham)
        rasterization_menu.add_command(label="Bresenham Circle", command=self.circle)
        self.menubar.add_cascade(label="Rasterization", menu=rasterization_menu)

        # Create a cutout menu and add it to the menu bar
        cutout_menu = Menu(self.menubar, tearoff=0)
        cutout_menu.add_command(label="Cohen-Sutherland", command=self.cohen_sutherland)
        cutout_menu.add_command(label="Liang-Barsky", command=self.liang_barsky)
        self.menubar.add_cascade(label="Cutout", menu=cutout_menu)

        # Display the menu
        self.window.config(menu=self.menubar)

        # Bind the click event to the canvas
        self.canvas.bind("<Button-1>", self.click)

        # Draw the initial grid
        self.draw_grid()

        mainloop()

    # Clear the pixel matrix and redraw the grid
    def clear_pixel_matrix(self):
        self.pixels = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.draw_grid()

    # Draw the grid with all the points which are set on as black
    def draw_grid(self):
        for i in range(ROWS):
            for j in range(COLS):
                color = 'black' if self.pixels[i][j] else 'white'
                x0, y0 = OFFSET + j*PIXEL_SIZE, OFFSET + i*PIXEL_SIZE
                x1, y1 = OFFSET + (j+1)*PIXEL_SIZE, OFFSET + (i+1)*PIXEL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        # Draw horizontal lines
        for i in range(ROWS + 1):
            self.canvas.create_line(OFFSET, OFFSET + i*PIXEL_SIZE, OFFSET + COLS*PIXEL_SIZE, OFFSET + i*PIXEL_SIZE, fill='black')

        # Draw vertical lines
        for i in range(COLS + 1):
            self.canvas.create_line(OFFSET + i*PIXEL_SIZE, OFFSET, OFFSET + i*PIXEL_SIZE, OFFSET + ROWS*PIXEL_SIZE, fill='black')

    # Sets the grid with the current state of the points, lines and circles
    def color_grid(self, points=None, lines=None, circles=None):
        if not points:
            points = self.point_list
        if not lines:
            lines = self.line_list
        if not circles:
            circles = self.circle_list
        self.clear_pixel_matrix()
        for point in points:
            x, y = point
            if 0 <= x < COLS and 0 <= y < ROWS:
                self.pixels[y][x] = 1
        for line in lines:
            x1, y1 = line[0]
            x2, y2 = line[1]
            if self.line_algorithm == DDA:
                points = self.functions.dda(x1, y1, x2, y2)
            elif self.line_algorithm == BRESENHAM:
                points = self.functions.bres(x1, y1, x2, y2)
            for point in points:
                x, y = point
                if 0 <= x < COLS and 0 <= y < ROWS:
                    self.pixels[y][x] = 1
        for circle in circles:
            x1, y1 = circle[0]
            x2, y2 = circle[1]
            distance = self.functions.distance(x1, y1, x2, y2)
            points = self.functions.circle(x1, y1, distance)
            for point in points:
                x, y = point
                if 0 <= x < COLS and 0 <= y < ROWS:
                    self.pixels[y][x] = 1
        self.draw_grid()

    # Change the state of the pixel where the click occurred
    def click(self, event):
        # Calculate the position of the pixel where the click occurred
        x, y = (event.x - OFFSET) // PIXEL_SIZE, (event.y - OFFSET) // PIXEL_SIZE
        if 0 <= x < COLS and 0 <= y < ROWS:
            # Change the state of the pixel to off if it is on
            if self.pixels[y][x] == 1:
                self.pixels[y][x] = 0
                if (x, y) in self.point_list:
                    self.point_list.remove((x, y))
            # Change the state of the pixel to on if it is off
            else:
                self.pixels[y][x] = 1
                self.point_list.append((x, y))
                self.pointb = self.pointa
                self.pointa = (x, y)
        # Redraw the grid
        self.draw_grid()

    # Here starts the functions that are called when a button in a menu is pressed

    def line_translation(self):
        p = PopupWindow(self.window, "Line Translation", "Enter the translation factor in X,Y, and select which line to move", self.line_list)
        self.window.wait_window(p.popup)
        user_input, line_chosen = p.get_user_input()
        if user_input and line_chosen:
            dx, dy = map(int, user_input.replace(" ", "").split(","))
            self.clear_pixel_matrix()
            new_line = []
            for point in line_chosen:
                x, y = point
                x, y = self.functions.move(x, y, dx, dy)
                new_line.append((x, y))
            self.line_list.remove(line_chosen)
            self.line_list.append((new_line[0], new_line[1]))
        self.color_grid()

    def rotation(self):
        p = PopupWindow(self.window, "Line Rotation", "Enter the rotation angle in degrees, and select which line to rotate", self.line_list)
        self.window.wait_window(p.popup)
        user_input, line_chosen = p.get_user_input()
        if user_input and line_chosen:
            self.clear_pixel_matrix()
            angle = int(user_input)
            xm, ym = self.functions.midpoint(line_chosen[0][0], line_chosen[0][1], line_chosen[1][0], line_chosen[1][1])        
            point1, point2 = line_chosen
            # Makes the midpoint the (0,0)
            x1 = point1[0] - xm
            y1 = point1[1] - ym
            x2 = point2[0] - xm
            y2 = point2[1] - ym
            x1, y1 = self.functions.rotate(x1, y1, angle)
            x2, y2 = self.functions.rotate(x2, y2, angle)
            # Returns to the original way
            x1 = x1 + xm
            y1 = y1 + ym
            x2 = x2 + xm
            y2 = y2 + ym
            new_line = ((x1, y1),(x2, y2))
            self.line_list.remove(line_chosen)
            self.line_list.append(new_line)
        self.color_grid()

    def scale(self):
        p = PopupWindow(self.window, "Line Scale", "Enter the scale factor in X,Y, and select which line to scale", self.line_list)
        self.window.wait_window(p.popup)
        user_input, line_chosen = p.get_user_input()
        if user_input and line_chosen:
            scale_x, scale_y = map(float, user_input.replace(" ", "").split(","))
            self.clear_pixel_matrix()
            xm, ym = self.functions.midpoint(line_chosen[0][0], line_chosen[0][1], line_chosen[1][0], line_chosen[1][1])
            point1, point2 = line_chosen
            # Makes the midpoint the (0,0)
            x1 = point1[0] - xm
            y1 = point1[1] - ym
            x2 = point2[0] - xm
            y2 = point2[1] - ym
            x1, y1 = self.functions.resize(x1, y1, scale_x, scale_y)
            x2, y2 = self.functions.resize(x2, y2, scale_x, scale_y)
            # Returns to the original way
            x1 = x1 + xm
            y1 = y1 + ym
            x2 = x2 + xm
            y2 = y2 + ym
            new_line = ((x1, y1),(x2, y2))
            self.line_list.remove(line_chosen)
            self.line_list.append(new_line)
        self.color_grid()

    def reflection_x(self):
        new_points = []
        new_line_list = []
        new_circle_list = []
        self.clear_pixel_matrix()
        for point in self.point_list:
            x, y = point
            x, y = self.functions.to_cartesian_plane(x, y)
            x, y = self.functions.reflex(x, y, "x")
            new_points.append((x, y))
        for line in self.line_list:
            x1, y1 = line[0]
            x2, y2 = line[1]
            x1, y1 = self.functions.to_cartesian_plane(x1, y1)
            x2, y2 = self.functions.to_cartesian_plane(x2, y2)
            x1, y1 = self.functions.reflex(x1, y1, "x")
            x2, y2 = self.functions.reflex(x2, y2, "x")
            new_line = ((x1, y1),(x2, y2))
            new_line_list.append(new_line)
        for circle in self.circle_list:
            x1, y1 = circle[0]
            x2, y2 = circle[1]
            x1, y1 = self.functions.to_cartesian_plane(x1, y1)
            x2, y2 = self.functions.to_cartesian_plane(x2, y2)
            x1, y1 = self.functions.reflex(x1, y1, "x")
            x2, y2 = self.functions.reflex(x2, y2, "x")
            new_circle = ((x1, y1),(x2, y2))
            new_circle_list.append(new_circle)
        self.point_list = new_points
        self.line_list = new_line_list
        self.circle_list = new_circle_list
        self.color_grid()

    def reflection_y(self):
        new_points = []
        new_line_list = []
        new_circle_list = []
        self.clear_pixel_matrix()
        for point in self.point_list:
            x, y = point
            x, y = self.functions.to_cartesian_plane(x, y)
            x, y = self.functions.reflex(x, y, "y")
            new_points.append((x, y))
        for line in self.line_list:
            x1, y1 = line[0]
            x2, y2 = line[1]
            x1, y1 = self.functions.to_cartesian_plane(x1, y1)
            x2, y2 = self.functions.to_cartesian_plane(x2, y2)
            x1, y1 = self.functions.reflex(x1, y1, "y")
            x2, y2 = self.functions.reflex(x2, y2, "y")
            new_line = ((x1, y1),(x2, y2))
            new_line_list.append(new_line)
        for circle in self.circle_list:
            x1, y1 = circle[0]
            x2, y2 = circle[1]
            x1, y1 = self.functions.to_cartesian_plane(x1, y1)
            x2, y2 = self.functions.to_cartesian_plane(x2, y2)
            x1, y1 = self.functions.reflex(x1, y1, "y")
            x2, y2 = self.functions.reflex(x2, y2, "y")
            new_circle = ((x1, y1),(x2, y2))
            new_circle_list.append(new_circle)
        self.point_list = new_points
        self.line_list = new_line_list
        self.circle_list = new_circle_list
        self.color_grid()

    def reflection_xy(self):
        new_points = []
        new_line_list = []
        new_circle_list = []
        self.clear_pixel_matrix()
        for point in self.point_list:
            x, y = point
            x, y = self.functions.to_cartesian_plane(x, y)
            x, y = self.functions.reflex(x, y, "xy")
            new_points.append((x, y))
        for line in self.line_list:
            x1, y1 = line[0]
            x2, y2 = line[1]
            x1, y1 = self.functions.to_cartesian_plane(x1, y1)
            x2, y2 = self.functions.to_cartesian_plane(x2, y2)
            x1, y1 = self.functions.reflex(x1, y1, "xy")
            x2, y2 = self.functions.reflex(x2, y2, "xy")
            new_line = ((x1, y1),(x2, y2))
            new_line_list.append(new_line)
        for circle in self.circle_list:
            x1, y1 = circle[0]
            x2, y2 = circle[1]
            x1, y1 = self.functions.to_cartesian_plane(x1, y1)
            x2, y2 = self.functions.to_cartesian_plane(x2, y2)
            x1, y1 = self.functions.reflex(x1, y1, "xy")
            x2, y2 = self.functions.reflex(x2, y2, "xy")
            new_circle = ((x1, y1),(x2, y2))
            new_circle_list.append(new_circle)
        self.point_list = new_points
        self.line_list = new_line_list
        self.circle_list = new_circle_list
        self.color_grid()

    def dda(self):
        if self.pointb:
            x1, y1 = self.pointa
            x2, y2 = self.pointb
            points = self.functions.dda(x1, y1, x2, y2)
            self.line_list.append((self.pointa, self.pointb))
            for point in points:
                x, y = point
                if 0 <= x < COLS and 0 <= y < ROWS:
                    self.pixels[y][x] = 1
            if self.pointa in self.point_list:
                self.point_list.remove(self.pointa)
            if self.pointb in self.point_list:
                self.point_list.remove(self.pointb)
            self.line_algorithm = DDA
            self.color_grid()
    
    def bresenham(self):
        if self.pointb:
            x1, y1 = self.pointa
            x2, y2 = self.pointb
            points = self.functions.bres(x1, y1, x2, y2)
            self.line_list.append((self.pointa, self.pointb))
            for point in points:
                x, y = point
                if 0 <= x < COLS and 0 <= y < ROWS:
                    self.pixels[y][x] = 1
            if self.pointa in self.point_list:
                self.point_list.remove(self.pointa)
            if self.pointb in self.point_list:
                self.point_list.remove(self.pointb)
            self.line_algorithm = BRESENHAM
            self.color_grid()

    def circle(self):
        if self.pointb:
            x1, y1 = self.pointa
            x2, y2 = self.pointb
            distance = self.functions.distance(x1, y1, x2, y2)
            points = self.functions.circle(x1, y1, distance)
            self.circle_list.append((self.pointa, self.pointb))
            for point in points:
                x, y = point
                if 0 <= x < COLS and 0 <= y < ROWS:
                    self.pixels[y][x] = 1
            if self.pointa in self.point_list:
                self.point_list.remove(self.pointa)
            if self.pointb in self.point_list:
                self.point_list.remove(self.pointb)
            self.color_grid()

    def cohen_sutherland(self):
        if self.pointb:
            new_line_list = []
            xa, ya = self.pointa
            xb, yb = self.pointb
            if xa < xb:
                x_min, x_max = xa, xb
            else:
                x_min, x_max = xb, xa
            if ya < yb:
                y_min, y_max = ya, yb
            else:
                y_min, y_max = yb, ya
            for line in self.line_list:
                x1, y1 = line[0]
                x2, y2 = line[1]
                new_line = self.functions.cohen_sutherland(x1, y1, x2, y2, x_min, y_min, x_max, y_max)
                if new_line:
                    new_line_list.append(new_line)
            if self.pointa in self.point_list:
                self.point_list.remove(self.pointa)
            if self.pointb in self.point_list:
                self.point_list.remove(self.pointb)
            self.color_grid(lines=new_line_list)

    def liang_barsky(self):
        if self.pointb:
            new_line_list = []
            xa, ya = self.pointa
            xb, yb = self.pointb
            if xa < xb:
                x_min, x_max = xa, xb
            else:
                x_min, x_max = xb, xa
            if ya < yb:
                y_min, y_max = ya, yb
            else:
                y_min, y_max = yb, ya
            for line in self.line_list:
                x1, y1 = line[0]
                x2, y2 = line[1]
                new_line = self.functions.liang_barsky(x1, y1, x2, y2, x_min, y_min, x_max, y_max)
                if new_line:
                    new_line_list.append(new_line)
            if self.pointa in self.point_list:
                self.point_list.remove(self.pointa)
            if self.pointb in self.point_list:
                self.point_list.remove(self.pointb)
            self.color_grid(lines=new_line_list)
