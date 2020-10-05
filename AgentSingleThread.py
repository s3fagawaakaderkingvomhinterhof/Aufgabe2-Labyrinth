x_coord_index = 0
y_coord_index = 1


class AgentSingleThread:

    def __init__(self, current_labyrinth, current_pos, distance_to_start):
        self.current_labyrinth = current_labyrinth
        self.first_run = True
        self.current_pos = current_pos
        self.neighbors = []  # every agent has own neighbors
        self.path_to_current_pos = []  # add member to labyrinth
        self.distance_to_start = distance_to_start
        self.previous_distance = 0
        self.start_point = [-1, -1]
        self.end_point = [-1, -1]
        self.solved = False

    def agent_clear(self):
        self.neighbors = []
        self.path_to_current_pos = []
        self.current_pos = self.start_point
        self.distance_to_start = 0
        self.previous_distance = 0
        self.first_run = True
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

    def get_neighbors_of_coord(self):
        valid_neighbors = []
        if self.current_labyrinth[self.current_pos[y_coord_index] - 1][self.current_pos[x_coord_index]] == 0 \
                and [self.current_pos[x_coord_index],
                     self.current_pos[y_coord_index] - 1] not in self.path_to_current_pos:
            up = [self.current_pos[x_coord_index], self.current_pos[y_coord_index] - 1]
            valid_neighbors.append([up, self.distance_to_start + 1])
        if self.current_labyrinth[self.current_pos[y_coord_index] + 1][self.current_pos[x_coord_index]] == 0 \
                and [self.current_pos[x_coord_index],
                     self.current_pos[y_coord_index] + 1] not in self.path_to_current_pos:
            down = [self.current_pos[x_coord_index], self.current_pos[y_coord_index] + 1]
            valid_neighbors.append([down, self.distance_to_start + 1])
        if self.current_labyrinth[self.current_pos[y_coord_index]][self.current_pos[x_coord_index] - 1] == 0 \
                and [self.current_pos[x_coord_index] - 1,
                     self.current_pos[y_coord_index]] not in self.path_to_current_pos:
            left = [self.current_pos[x_coord_index] - 1, self.current_pos[y_coord_index]]
            valid_neighbors.append([left, self.distance_to_start + 1])
        if self.current_labyrinth[self.current_pos[y_coord_index]][self.current_pos[x_coord_index] + 1] == 0 \
                and [self.current_pos[x_coord_index] + 1,
                     self.current_pos[y_coord_index]] not in self.path_to_current_pos:
            right = [self.current_pos[x_coord_index] + 1, self.current_pos[y_coord_index]]
            valid_neighbors.append([right, self.distance_to_start + 1])
        return valid_neighbors

    def is_in_current_path(self, neighbor_item):
        path_to_current_pos_size = len(self.path_to_current_pos)  # old: self.path_to_current_pos
        for i in range(0, path_to_current_pos_size):
            if self.path_to_current_pos[i][0] == neighbor_item[0]:  # old: self.path_to_current_pos
                return True
            else:
                return False

    def solve_single_thread(self):
        if self.first_run:
            if self.check_start_conditions(self.current_labyrinth):
                self.current_pos = self.start_point
                self.path_to_current_pos.append([self.current_pos, self.distance_to_start])
                self.first_run = False
                self.neighbors = self.get_neighbors_of_coord()
            else:
                print('ERROR: check settings!')
                return
            self.solve_single_thread()
            return self.path_to_current_pos
        else:
            self.distance_to_start = 1
            solved = False
            while len(self.neighbors) > 0 and not solved:
                search_state = self.neighbors.pop(0)
                if search_state[1] > self.distance_to_start:
                    self.distance_to_start += 1
                if not self.is_in_current_path(search_state):
                    self.current_pos = search_state[0]
                    if self.current_pos == self.end_point:
                        solved = True
                        self.path_to_current_pos.append([self.current_pos, self.distance_to_start])
                        return
                    self.path_to_current_pos.append([self.current_pos, self.distance_to_start])
                    neighbors = self.get_neighbors_of_coord()
                    neighbor_size = len(neighbors)
                    for i in range(0, neighbor_size):
                        if not self.is_in_current_path(neighbors[i]):
                            self.neighbors.append(neighbors[i])

    def build_route_to_end(self):
        path_start_to_end = self.path_to_current_pos
        path_start_to_end.reverse()
        position = 0
        distance = 1
        shortest_path = []
        if len(shortest_path) == 0:
            shortest_path.append(path_start_to_end.pop(0))
        while len(path_start_to_end) > 0:
            path_pos_and_dist = path_start_to_end.pop(0)
            current_distance_result = shortest_path[len(shortest_path) - 1][distance]
            if path_pos_and_dist[distance] == current_distance_result - 1:
                if sum(path_pos_and_dist[position]) == sum(shortest_path[len(shortest_path) - 1][position]) + 1:
                    if path_pos_and_dist[position][0] == shortest_path[len(shortest_path) - 1][position][0]:
                        shortest_path.append(path_pos_and_dist)
                    if path_pos_and_dist[position][1] == shortest_path[len(shortest_path) - 1][position][1]:
                        shortest_path.append(path_pos_and_dist)
                if sum(path_pos_and_dist[position]) == sum(shortest_path[len(shortest_path) - 1][position]) - 1:
                    if path_pos_and_dist[position][0] == shortest_path[len(shortest_path) - 1][position][0]:
                        shortest_path.append(path_pos_and_dist)
                    if path_pos_and_dist[position][1] == shortest_path[len(shortest_path) - 1][position][1]:
                        shortest_path.append(path_pos_and_dist)
        shortest_path.reverse()
        result = []
        while len(shortest_path) > 0:
            ele = shortest_path.pop(0)
            if ele not in result:
                result.append(ele)
        print(result)
