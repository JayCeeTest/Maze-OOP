

class Graph(object):
    def __init__(self, maze, num_of_rooms, start_point, end_point):
        # num_of_rooms should be a tuple of num rows and num columns
        self.maze = maze
        # self.roomMap = self.maze.roomMapping
        self.m = num_of_rooms[0]
        self.n = num_of_rooms[1]
        self.tuple_map, self.reversed_tuple_map = self.create_tuple_mapping()  # all tuples in the maze are here
        # self.start_point = start_point
        # self.end_point = end_point
        self.start_node = Node(self.tuple_map[start_point])
        self.end_node = Node(self.tuple_map[end_point])

    def create_tuple_mapping(self):
        # map each int room number to a coordinate tuple
        tuple_map = dict()
        reversed_tuple_map = dict()
        count = 0
        for i in range(self.n):
            for j in range(self.m):
                tuple_map[count] = (j,i)
                reversed_tuple_map[(j,i)] = count
                count+=1
        return tuple_map, reversed_tuple_map

    def find_all_children(self, node):
        raw_children = self.find_node_children(node.data)
        raw_children = filter(lambda x: x.data[0]>=0 and x.data[1]>=0, raw_children)
        raw_children = filter(lambda x: x.data[0]<self.m and x.data[1]<self.n, raw_children)
        children = self.remove_nodes_with_walls(node, raw_children)
        return children

    def remove_nodes_with_walls(self, node, children):
        result=[]
        children_data = map(lambda x: x.data, children)
        node_room_no = self.reversed_tuple_map[node.data]
        node_room = self.maze.roomMapping[node_room_no]
        node_room_sides = node_room.sides
        for i in range(len(node_room_sides)):
            if node_room_sides[i] is None:
                next_node = self.next_node_map(node.data, i)
                if next_node in children_data:
                    result.append(next_node)
        for child in children_data:
            child_room_no = self.reversed_tuple_map[child]
            child_room = self.maze.roomMapping[child_room_no]
            child_room_sides = child_room.sides
            if child == (node.data[0]+1, node.data[1]):
                if child_room_sides[0] is None:
                    result.append(child)
            elif child == (node.data[0], node.data[1]-1):
                if child_room_sides[1] is None:
                    result.append(child)
            elif child == (node.data[0]-1, node.data[1]):
                if child_room_sides[2] is None:
                    result.append(child)
            elif child == (node.data[0], node.data[1]+1):
                if child_room_sides[3] is None:
                    result.append(child)
        result = map(lambda x: Node(x), result)
        return result

    def next_node_map(self, node, dir):
        if dir == 0:
            return node[0]-1, node[1]
        elif dir == 1:
            return node[0], node[1]+1
        elif dir == 2:
            return node[0]+1, node[1]
        else:
            return node[0], node[1]-1

    def find_node_children(self, node_data):
        children = list()
        children.append((node_data[0]+1, node_data[1]))
        children.append((node_data[0]-1, node_data[1]))
        children.append((node_data[0], node_data[1]+1))
        children.append((node_data[0], node_data[1]-1))
        children=map(lambda x: Node(x),children)
        return children

    def breadth_first_search(self):
        self.expanded_nodes=[]
        repeated=[]  # tracking repeated states
        queue=[self.start_node]
        while len(queue)!=0:
            u=queue.pop(0)
            if u.data in repeated:
                continue  # we have seen these already
            self.expanded_nodes.append(u)
            repeated.append(u.data)
            children=self.find_all_children(u)
            for child in children:
                child.add_parent(u)
                queue.append(child)
            if u.data == self.end_node.data:
                break
        return self.expanded_nodes

    def get_bfs_trace(self):
        root=self.start_node
        # return the path that bfs followed
        goal=self.expanded_nodes[-1]
        trace=[]
        if goal.data!=self.end_node.data: return "No Valid Path Found"
        while goal.data != root.data:
            trace.append(goal.data)
            goal=goal.parent
        trace.append(root.data)  # we found the trace at this point
        return trace[::-1]


class Node(object):
    def __init__(self,data):
        self.data = data
        self.children=[]
        self.parent=None

    def add_child(self,child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parent=parent

# a = Graph(1,(4,4),1,8)
# a.breadth_first_search()
