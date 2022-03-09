# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# create a map

def read_map(file):
    f = open(file, "r")
    direction_list = []
    colour_list = []
    start = ()
    end = ()
    n = f.readline()
    n = int(n)
    for i in range(n):
        direction_list[i] = 0
        colour_list[i] = 0

    for i in range(n):
        index = 0
        line = f.readline()
        split_line = line.split(" ")
        for j in range(n):
            if split_line[j][0] != "g":
                if split_line[j][0] == "s":
                    start = (i, j)
                    direction_list[index] = split_line[j][3:]
                elif split_line[j][0] == "r":
                    colour_list[index] = 1
                    direction_list[index] = split_line[j][2:]
                elif split_line[j][0] == "y":
                    colour_list[index] = -1
                    direction_list[index] = split_line[j][2:]
            else:
                end = (i, j)
                direction_list[index] = -1
            index += 1
            j += 1
        i += 1
    f.close()
    return [n, start, end, direction_list, colour_list]


# return the list of vertices
def create_vertices(n, content):
    lst = []
    for i in range(n * n):
        nested_lst = []
        for j in range(n - 1):
            nested_lst.append(content)
        lst.append(nested_lst)
    return lst


def coordinate_to_index(x, y, n):
    return x + y * n


# return the children of (x,y) given direction and speed. If children is out of
# bound, return None
def find_children(n, vertex, direction, arrow_color):
    x = vertex[0]
    y = vertex[1]
    speed = vertex[2]

    if direction == '1':
        y -= speed
    elif direction == '2':
        x += speed
        y -= speed
    elif direction == '3':
        x += speed
    elif direction == '4':
        x += speed
        y += speed
    elif direction == '5':
        y += speed
    elif direction == '6':
        x -= speed
        y += speed
    elif direction == '7':
        x -= speed
    elif direction == '8':
        x -= speed
        y -= speed

    if not (0 <= x <= n - 1 and 0 <= y <= n - 1):
        return None
    c_index = coordinate_to_index(x, y, n)
    c_speed = speed + arrow_color[c_index]
    if c_speed < 1 or c_speed > n - 1:
        return None
    return x, y, c_speed


def is_white(vertices, vertex, n):
    x = vertex[0]
    y = vertex[1]
    speed = vertex[2]
    index = coordinate_to_index(x, y, n)
    return vertices[index][speed - 1] == 'w'


def colour(vertices, vertex, colour):
    x = vertex[0]
    y = vertex[1]
    speed = vertex[2]
    index = coordinate_to_index(x, y, n)
    vertices[index][speed - 1] = colour


def update_parent(parent_lst, parent, children, n):
    x = children[0]
    y = children[1]
    speed = children[2]
    index = coordinate_to_index(x, y, n)
    parent_lst[index][speed - 1] = parent


def is_empty(direction_list, vertex, n):
    index = coordinate_to_index(vertex[0], vertex[1], n)
    return direction_list[index] == '-1'


def reach_goal(vertex, goal):
    return vertex[0] == goal[0] and vertex[1] == goal[1]


def update_distance(distance_lst, parent, children, n):
    p_index = coordinate_to_index(parent[0], parent[1], n)
    c_index = coordinate_to_index(children[0], children[1], n)
    distance_lst[c_index][children[2] - 1] = distance_lst[p_index][
                                                 parent[2] - 1] + 1


def find_parent(parent_lst, children):
    x = children[0]
    y = children[1]
    speed = children[2]
    index = coordinate_to_index(x, y, n)
    return parent_lst[index][speed - 1]


def find_path(parent_lst, goal):
    path = []
    p_len = 0
    path.insert(0, goal)
    parent = find_parent(parent_lst, goal)
    while parent is not None:
        p_len += 1
        path.insert(0, parent)
        parent = find_parent(parent_lst, parent)
    print(path)
    print(p_len)


def BFS(start, end, n, direction_list, arrow_color):
    s = coordinate_to_index(start[0], start[1], n)
    vertices = create_vertices(n, 'w')
    parent_lst = create_vertices(n, None)
    vertices[s][0] = 'G'
    queue = [(start[0], start[1], 1)]  # initialize an empty queue
    while len(queue) != 0:
        parent = queue.pop(0)
        p_index = coordinate_to_index(parent[0], parent[1], n)
        for direction in direction_list[p_index]:
            children = find_children(n, parent, direction, arrow_color)
            if children is not None and is_white(vertices, children, n):
                colour(vertices, children, 'G')
                update_parent(parent_lst, parent, children, n)
                if reach_goal(children, end):
                    find_path(parent_lst, children)
                    return 0
                if is_empty(direction_list, children, n):
                    continue
                queue.append(children)
        colour(vertices, parent, 'B')
    return 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_map('example_maze.txt')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
