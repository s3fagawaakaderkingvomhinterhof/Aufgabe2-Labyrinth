

import threading


x_coord_index = 0
y_coord_index = 1

class Agent:

    def __init__(self, current_labyrinth, current_pos, distance_to_start):
        self.current_labyrinth = current_labyrinth
        self.current_pos = current_pos
        self.distance_to_start = distance_to_start
        self.start_point = [-1, -1]
        self.end_point = [-1, -1]
        self.solved = False

    def set_start(self, x, y):
        self.start_point[y_coord_index] = y
        self.start_point[x_coord_index] = x
        print('start from agent: ', self.start_point)

    def set_end(self, x, y):
        self.end_point[y_coord_index] = y
        self.end_point[x_coord_index] = x
        print('end from agent: ', self.end_point)

    def check_start_conditions(self, current_labyrinth):
        start_in_field = False
        end_in_field = False
        start_end_are_same = False
        start_not_on_wall = False
        end_not_on_wall = False

        cols = len(current_labyrinth)
        rows = len(current_labyrinth[0])

        if self.start_point[x_coord_index] > -1 and self.start_point[y_coord_index] > -1 \
                and self.start_point[x_coord_index] < cols and self.start_point[y_coord_index] < rows:
            start_in_field = True
        if self.end_point[x_coord_index] > -1 and self.end_point[y_coord_index] > -1 \
                and self.end_point[x_coord_index] < cols and self.end_point[y_coord_index] < rows:
            end_in_field = True

        if self.start_point[x_coord_index] != self.end_point[x_coord_index] or \
                self.start_point[y_coord_index] != self.end_point[y_coord_index]:
            start_end_are_same = True

        if current_labyrinth[self.start_point[y_coord_index]][self.start_point[x_coord_index]] != -1:
            start_not_on_wall = True
        if current_labyrinth[self.end_point[y_coord_index]][self.end_point[x_coord_index]] != -1:
            end_not_on_wall = True
        return start_in_field and end_in_field and start_end_are_same and start_not_on_wall and end_not_on_wall

    def get_neighbors_of_coord(self):                                                                                   # does work properly
        print('call get_neighbors of:' , self.current_pos)
        up = down = left = right = [-1, -1]
        valid_neighbors = []
        if self.current_labyrinth[self.current_pos[y_coord_index]-1][self.current_pos[x_coord_index]] == 0:             # 1st var y-coord, 2nd var x-coord
            up = [self.current_pos[x_coord_index], self.current_pos[y_coord_index]-1]                                   # valid neighbor up: 1st x-coord, 2nd y-coord
            valid_neighbors.append(up)
            print('up is', up)
        if self.current_labyrinth[self.current_pos[y_coord_index]+1][self.current_pos[x_coord_index]] == 0:
            down = [self.current_pos[x_coord_index], self.current_pos[y_coord_index]+1]
            valid_neighbors.append(down)
            print('down is', down)
        if self.current_labyrinth[self.current_pos[y_coord_index]][self.current_pos[x_coord_index]-1] == 0:
            left = [self.current_pos[x_coord_index]-1, self.current_pos[y_coord_index]]
            valid_neighbors.append(left)
            print('left is', left)
        if self.current_labyrinth[self.current_pos[y_coord_index]][self.current_pos[x_coord_index]+1] == 0:
            right = [self.current_pos[x_coord_index]+1, self.current_pos[y_coord_index]]
            valid_neighbors.append(right)
            print('right is', right)
        return valid_neighbors                                                                                          # example result: [[1,2],[2,1]]

    def visiting(self, neighbors):
        if self.distance_to_start == 0:
            print('x-value first coord:', neighbors[0][0][0])
            self.current_labyrinth[neighbors[0][0][1]][neighbors[0][0][0]] = self.distance_to_start
            self.distance_to_start += 1
        else:
            size = len(neighbors)
            print(neighbors)


    def solve(self):
        if self.check_start_conditions(self.current_labyrinth):
            visiting_in_next_step = []
            path = []
            # init algo
            if self.distance_to_start == 0:
                self.current_pos = self.start_point

                path.append([self.current_pos, self.distance_to_start])
                visiting_in_next_step = self.get_neighbors_of_coord()
                print('visiting_next:', visiting_in_next_step)
                self.visiting(path)


            while len(visiting_in_next_step) > 0 and not self.solved:
                self.visiting(visiting_in_next_step)

                # todo: thread variation
                self.solved = True

        else:                                                                                                           # if False start conditions
            print('start conditions wrong or incomplete')
