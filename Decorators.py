__author__ = 'jarethmoyo'


class WallDecorator(object):
    # for decorating walls
    def __init__(self, canvas, wall):
        self.canvas = canvas
        self.wall = wall

    def create(self):
        coord = self.wall.get_coord()
        my_wall = self.canvas.create_line(coord, width=2, fill="black")
        self.set_active_dash(my_wall)

    def set_active_dash(self, x):
        self.canvas.itemconfig(x, fill="white",dash=(3,5))

class WallDecorator2(object):
    def __init__(self, canvas, wall):
        self.canvas = canvas
        self.wall = wall

    def create(self):
        coord = self.wall.get_coord()
        my_wall = self.canvas.create_line(coord, width=2, fill="black")
        self.set_active_dash(my_wall)

    def set_active_dash(self, x):
        self.canvas.itemconfig(x, fill="red")