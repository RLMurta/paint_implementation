from utils import *

class PaintInterface:
    def __init__(self):
        # Create a 2D array to store the state of each pixel (on/off)
        self.pixels = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        window = Tk()
        self.canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        # Create a menu bar
        self.menubar = Menu(window)

        # Create a transformations menu and add it to the menu bar
        transformations_menu = Menu(self.menubar, tearoff=0)
        transformations_menu.add_command(label="Translation", command=self.translation)
        transformations_menu.add_command(label="Rotation", command=self.rotation)
        transformations_menu.add_command(label="Scale", command=self.scale)
        transformations_menu.add_command(label="Reflection X", command=self.reflection_x)
        transformations_menu.add_command(label="Reflection Y", command=self.reflection_y)
        transformations_menu.add_command(label="Reflection XY", command=self.reflection_xy)
        self.menubar.add_cascade(label="Transformations", menu=transformations_menu)

        # Create a rasterization menu and add it to the menu bar
        rasterization_menu = Menu(self.menubar, tearoff=0)
        rasterization_menu.add_command(label="DDA Line", command=self.translation)
        rasterization_menu.add_command(label="Bresenham Line", command=self.rotation)
        rasterization_menu.add_command(label="Bresenham Circle", command=self.scale)
        self.menubar.add_cascade(label="Rasterization", menu=rasterization_menu)

        # Create a cutout menu and add it to the menu bar
        cutout_menu = Menu(self.menubar, tearoff=0)
        cutout_menu.add_command(label="Cohen-Sutherland", command=self.translation)
        cutout_menu.add_command(label="Liang-Barsky", command=self.rotation)
        self.menubar.add_cascade(label="Cutout", menu=cutout_menu)

        # Display the menu
        window.config(menu=self.menubar)

        # Bind the click event to the canvas
        self.canvas.bind("<Button-1>", self.click)

        # Draw the initial grid
        self.draw_grid()

        mainloop()

    def draw_grid(self):
        for i in range(ROWS):
            for j in range(COLS):
                color = 'black' if self.pixels[i][j] else 'white'
                self.canvas.create_rectangle(OFFSET + j*PIXEL_SIZE, OFFSET + i*PIXEL_SIZE, OFFSET + (j+1)*PIXEL_SIZE, OFFSET + (i+1)*PIXEL_SIZE, fill=color)

        # Draw horizontal lines
        for i in range(ROWS + 1):
            self.canvas.create_line(OFFSET, OFFSET + i*PIXEL_SIZE, OFFSET + COLS*PIXEL_SIZE, OFFSET + i*PIXEL_SIZE, fill='black')

        # Draw vertical lines
        for i in range(COLS + 1):
            self.canvas.create_line(OFFSET + i*PIXEL_SIZE, OFFSET, OFFSET + i*PIXEL_SIZE, OFFSET + ROWS*PIXEL_SIZE, fill='black')

    def click(self, event):
        # Calculate the position of the pixel where the click occurred
        x, y = (event.x - OFFSET) // PIXEL_SIZE, (event.y - OFFSET) // PIXEL_SIZE
        # Change the state of the pixel to on
        if 0 <= x < COLS and 0 <= y < ROWS:
            if self.pixels[y][x] == 1:
                self.pixels[y][x] = 0
                print(f"Pixel ({x}, {y}) is off")
            else:
                self.pixels[y][x] = 1
                print(f"Pixel ({x}, {y}) is on")
        # Redraw the grid
        self.draw_grid()

    def translation(self):
        print("Translation")

    def rotation(self):
        print("Rotation")

    def scale(self):
        print("Scale")

    def reflection_x(self):
        print("Reflection X")
    
    def reflection_y(self):
        print("Reflection Y")
    
    def reflection_xy(self):
        print("Reflection XY")

PaintInterface()