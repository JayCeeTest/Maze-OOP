from MazeWidgets import *
from Decorators import *
from Graph import *
import Tkinter as tk
import time
# mapping 0-North 1-East 2-South 3-West


class MazeGame(object):
    point_of_origin = (10,10)  # origin point for any maze game created

    def __init__(self, master):
        master.title("Enter The Maze")
        top_frame = tk.Frame(master)
        top_frame.pack()
        setup_frame = tk.Frame(master)
        setup_frame.pack(anchor=tk.W)
        canvas_frame = tk.Frame(setup_frame)
        canvas_frame.pack(side=tk.RIGHT)
        # create canvas
        self.canvas = tk.Canvas(canvas_frame, width=800, height=600, bg="white")
        self.canvas.pack(anchor=tk.W)
        # maze config
        rooms_label = tk.Label(setup_frame, text="Enter number of rooms", font="Verdana 8 bold")
        rooms_label.pack()
        maze_width_label = tk.Label(setup_frame, text="Number of rows:", font="Verdana 8")
        maze_width_label.pack(anchor=tk.W)
        self.maze_width = tk.Text(setup_frame, width=10,height=1)
        self.maze_width.pack(anchor=tk.W,padx=3)
        maze_height_label = tk.Label(setup_frame, text="Number of columns:", font="Verdana 8")
        maze_height_label.pack(anchor=tk.W)
        self.maze_height = tk.Text(setup_frame, width=10,height=1)
        self.maze_height.pack(anchor=tk.W,padx=3)
        # room config
        room_size_label = tk.Label(setup_frame, text="Enter size of room:", font="Verdana 8 bold")
        room_size_label.pack(anchor=tk.W, pady=(15,0))
        self.room_size = tk.Text(setup_frame, width=10,height=1)
        self.room_size.pack(anchor=tk.W,padx=3)

        generate_button = tk.Button(setup_frame, text="Generate Maze", font="Times 10 bold", fg="blue",
                                    bg="yellow", command=self.maze_generator)
        generate_button.pack(anchor=tk.W, pady=(20,0),padx=3)

        mouse_label = tk.Label(setup_frame, text="Mouse starting point", font = "Verdana 8 bold")
        mouse_label.pack(anchor=tk.W, pady=(10,0))
        self.mouse_room = tk.Text(setup_frame, width=10, height=1)
        self.mouse_room.pack(anchor=tk.W, padx=3)
        mouse_button = tk.Button(setup_frame, text="Place Mouse", font="Times 8 bold", fg="blue",
                                    bg="yellow", command=self.place_mouse)
        mouse_button.pack(anchor=tk.W, pady=(10,0),padx=3)

        mouse_label2 = tk.Label(setup_frame, text="Mouse end point", font = "Verdana 8 bold")
        mouse_label2.pack(anchor=tk.W, pady=(10,0))
        self.mouse_room_dest = tk.Text(setup_frame, width=10, height=1)
        self.mouse_room_dest.pack(anchor=tk.W, padx=3)
        go_button = tk.Button(setup_frame, text="Go", font="Times 10 bold", fg="black",
                                    bg="green", width=4, command=self.navigate)
        go_button.pack(anchor=tk.W, pady=(10,0),padx=3)
        intermission = tk .Label(setup_frame, text="--"*15)
        intermission.pack(anchor=tk.W)

        wall_deco_label = tk.Label(setup_frame, text="Wall Decoration Config", font="Helvetica 10 bold italic",
                                   fg="blue")
        wall_deco_label.pack(anchor=tk.W, pady=(2,0))
        room_to_deco_label = tk.Label(setup_frame, text="Choose room to decorate:", font="Helvetica 10 italic",
                                      fg="black")
        room_to_deco_label.pack(anchor=tk.W)
        self.room_to_decorate = tk.Text(setup_frame, width=10, height=1)
        self.room_to_decorate.pack(anchor=tk.W, padx=3)
        wall_to_deco_label = tk.Label(setup_frame, text="Choose wall to decorate:", font="Helvetica 10 italic",
                                      fg="black")
        wall_to_deco_label.pack(anchor=tk.W)
        self.wall_to_decorate = tk.Text(setup_frame, width=10, height=1)
        self.wall_to_decorate.pack(anchor=tk.W, padx=3)

        decorate_button = tk.Button(setup_frame, text="Decorate", font="Times 10 bold", fg="white",
                                    bg="purple", command=self.decorate)
        decorate_button.pack(anchor=tk.W, pady=(10,0),padx=3)

    def create_maze(self, num_of_rooms,offset):
        m,n = num_of_rooms  # number of rows and columns in the maze
        if m<1 or n<1:
            raise Exception("Please enter valid number of rooms")

        # offset=90  # original size of each room
        self.maze = Maze(self.canvas, offset)

        # maze.add_room(0, self.point_of_origin)
        og_x, og_y = self.point_of_origin  # original coordinates
        x_offset = 0
        r_index = 0
        for i in range(n):
            y_offset=0
            for j in range(m):
                self.maze.add_room(r_index,(og_x+x_offset,og_y+y_offset))
                r_index+=1
                y_offset+=offset
            x_offset+=offset
        self.maze.create()
        a = self.maze.roomMapping[0]
        b = self.maze.roomMapping[1]
        c = self.maze.roomMapping[6]
        print a.sides
        print b.sides
        print c.sides

    def decorate(self):
        room_no = int(self.room_to_decorate.get('1.0','end-1c'))
        wall_dir = int(self.wall_to_decorate.get('1.0','end-1c'))
        room = self.maze.roomMapping[room_no]
        wall = room.get_side(wall_dir)
        decorated_wall=WallDecorator(self.canvas, wall)
        decorated_wall.create()

    def place_mouse(self):
        start_point = int(self.mouse_room.get('1.0', 'end-1c'))
        room=self.maze.get_room(start_point)
        room_coord = room.get_midpoint()
        room_size = int(self.room_size.get('1.0',tk.END))
        self.mouse = Mouse(self.canvas,room_coord,room_size)
        self.mouse.create()

    def maze_generator(self):
        self.canvas.delete("all")
        rows=int(self.maze_width.get('1.0',tk.END))
        columns=int(self.maze_height.get('1.0',tk.END))
        room_size = int(self.room_size.get('1.0',tk.END))
        self.create_maze((rows,columns),room_size)

    def navigate(self):
        rows=int(self.maze_width.get('1.0',tk.END))
        columns=int(self.maze_height.get('1.0',tk.END))
        start_point = int(self.mouse_room.get('1.0', 'end-1c'))
        end_point = int(self.mouse_room_dest.get('1.0','end-1c'))
        print self.maze
        graph = Graph(self.maze,(rows,columns),start_point, end_point)
        graph.breadth_first_search()
        path=graph.get_bfs_trace()
        print path
        agent = self.mouse.my_mouse
        self.move_on_path(path, agent)

    def move_on_path(self,path, agent):
        while len(path) !=1:
            p=path.pop(0)
            n=path[0]
            self.movement(p,n, agent)

    def move_x(self,dir, agent):
        # movement along x direction
        room_size = int(self.room_size.get('1.0',tk.END))
        try:
            for _ in range(room_size/2):
                time.sleep(0.02)
                self.canvas.move(agent,dir*2,0)
                self.canvas.update()
        except tk.TclError:
            pass

    def move_y(self,dir,agent):
        # movement along y direction
        room_size = int(self.room_size.get('1.0',tk.END))
        try:
            for _ in range(room_size/2):
                time.sleep(0.02)
                self.canvas.move(agent,0,dir*2)
                self.canvas.update()
        except tk.TclError:
            pass

    def movement(self, prev_state, next_state, agent):
        # this moves an agent from previous to next state
        move_on_y=next_state[0]-prev_state[0]
        move_on_x=next_state[1]-prev_state[1]
        if move_on_y:
            self.move_y(move_on_y, agent)
        elif move_on_x:
            self.move_x(move_on_x, agent)

if __name__ == "__main__":
    root=tk.Tk()
    root.resizable(0,0)
    MazeGame(root)
    root.mainloop()
