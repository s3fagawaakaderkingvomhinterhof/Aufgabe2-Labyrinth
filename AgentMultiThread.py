

import threading
from Labyrinth import *


class AgentMultiThread:
    labyrinth_object = None

    def __init__(self, labyrinth_object, current_pos):
        self.labyrinth_object = labyrinth_object
        self.current_pos = current_pos
        self.end_point = [-1, -1]

    def set_end(self, x, y):
        self.end_point[1] = y
        self.end_point[0] = x

    def get_neighbors_of_coord(self):
        neighbors_of_current_pos = []
        up = [self.current_pos[0], self.current_pos[1] - 1]         # 0 = x_coord, 1 = y_coord
        down = [self.current_pos[0], self.current_pos[1] + 1]
        left = [self.current_pos[0] - 1, self.current_pos[1]]
        right = [self.current_pos[0] + 1, self.current_pos[1]]

        if self.labyrinth_object.get_field_value(self.current_pos[1] - 1,  # old 1st: y_coord
                                                 self.current_pos[0]) == 0 \
                and up not in self.labyrinth_object.get_visited_list():
            neighbors_of_current_pos.append(up)
        if self.labyrinth_object.get_field_value(self.current_pos[1] + 1,
                                                 self.current_pos[0]) == 0 \
                and down not in self.labyrinth_object.get_visited_list():
            neighbors_of_current_pos.append(down)
        if self.labyrinth_object.get_field_value(self.current_pos[1],
                                                 self.current_pos[0] - 1) == 0 \
                and left not in self.labyrinth_object.get_visited_list():
            neighbors_of_current_pos.append(left)
        if self.labyrinth_object.get_field_value(self.current_pos[1],
                                                 self.current_pos[0] + 1) == 0 \
                and right not in self.labyrinth_object.get_visited_list():
            neighbors_of_current_pos.append(right)
        return neighbors_of_current_pos

    def solve_multi_thread(self):
        if self.current_pos not in self.labyrinth_object.get_visited_list():
            if self.current_pos == self.end_point:
                print('found destination ', self.current_pos)
                return

            self.labyrinth_object.append_position_to_visited_list(self.current_pos)
            neighbors_of_coord = self.get_neighbors_of_coord()
            if len(neighbors_of_coord) == 0:
                return
            elif len(neighbors_of_coord) == 1:
                self.current_pos = neighbors_of_coord[0]
                self.solve_multi_thread()
            elif len(neighbors_of_coord) > 1:
                print(neighbors_of_coord)
                for i in range(0, len(neighbors_of_coord) - 1):
                    agent = AgentMultiThread(self.labyrinth_object, neighbors_of_coord[i])
                    agent.set_end(self.end_point[0], self.end_point[1])
                    t = threading.Thread(target=agent.solve_multi_thread)
                    t.start()
                self.current_pos = neighbors_of_coord[len(neighbors_of_coord) - 1]
                self.solve_multi_thread()
