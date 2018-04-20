__author__ = 'jarethmoyo'

import random


class Wall(object):
    def __init__(self, canvas, coord):
        self.canvas = canvas
        self.coord = coord

    def get_coord(self):
        return self.coord

    def create(self):
        self.canvas.create_line(self.coord, width=2, fill="black")


class Door(Wall):
    # class door extends wall
    def __init__(self, canvas, coord):
        super(Door, self).__init__(canvas, coord)

    def create(self):
        self.canvas.create_line(self.coord, width=2, fill="lightyellow", activefill="green")


class Room(object):

    def __init__(self, room_no):
        self.room_no = room_no
        self.sides = [None]*4  # array with 4 elements
        self.coord = None
        self.size = 90 # default size of room

    def set_size(self, size):
        self.size = size

    def set_side(self, direction, wall):
        self.sides[direction]= wall

    def set_coord(self, coord):
        self.coord = coord

    def get_side(self, direction):
        return self.sides[direction]

    def get_room_no(self):
        return self.room_no

    def get_coord(self):
        return self.coord

    def get_midpoint(self):
        return self.coord[0]+self.size/2, self.coord[1]+self.size/2

    def create(self):
        for wall in self.sides:
            wall.create()


class Maze(object):

    def __init__(self, canvas, offset=90):
        self.canvas=canvas
        self.offset = offset
        self.roomMapping = {}

    def add_room(self, room_no, coord):
        x,y = coord
        room = Room(room_no)
        room.set_side(0,Wall(self.canvas,(x,y,x+self.offset,y)))
        room.set_side(1,Wall(self.canvas,(x+self.offset,y,x+self.offset,y+self.offset)))
        room.set_side(2,Wall(self.canvas,(x,y+self.offset,x+self.offset,y+self.offset)))
        room.set_side(3,Wall(self.canvas,(x,y,x,y+self.offset)))
        room.set_coord(coord)
        room.set_size(self.offset)
        self.roomMapping[room_no]=room

    def add_room_label(self, room):
        coord = room.get_midpoint()
        room_no = room.get_room_no()
        self.canvas.create_text(coord, text=room_no, fill="gray")

    def add_door(self, room):
        x,y = room.get_coord()
        door_side = self.random_num_generator(x,y)  # random number to determine direction that the door is facing
        if door_side == 0:
            room.set_side(0,Door(self.canvas,(x,y,x+self.offset,y)).create())
        elif door_side == 1:
            room.set_side(1,Door(self.canvas,(x+self.offset,y,x+self.offset,y+self.offset)).create())
        elif door_side == 2:
            room.set_side(2,Door(self.canvas,(x,y+self.offset,x+self.offset,y+self.offset)).create())
        else:
            room.set_side(3,Door(self.canvas,(x,y,x,y+self.offset)).create())

    def get_room(self, room_no):
        return self.roomMapping[room_no]

    def random_num_generator(self, x,y):
        if x==10 and y==10:
            door_side=random.randint(1,2)
        elif x==10:
            door_side= random.randint(0,2)
        elif y==10:
            door_side= random.randint(1,3)
        else:
            door_side= random.randint(0,3)
        return door_side

    def create(self):
        for room in self.roomMapping.values():
            room.create()
        for room in self.roomMapping.values():
            self.add_door(room)
        for room in self.roomMapping.values():
            self.add_room_label(room)


class Mouse(object):
    def __init__(self, canvas, coord, size):
        self.canvas = canvas
        self.coord = coord
        self.size = size

    def create(self):
        x=self.coord[0]
        y=self.coord[1]
        radx = self.size/7
        rady = self.size/7
        self.my_mouse = self.canvas.create_oval([x-radx,y-rady,x+radx,y+rady],fill="darkgrey", outline="black")

