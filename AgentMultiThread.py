import threading
import sys
from copy import deepcopy

from Labyrinth import *


class AgentMultiThread:
    labyrinth_object = None

    def __init__(self, labyrinth_object, current_pos, path):
        self.labyrinth_object = labyrinth_object
        self.current_pos = current_pos
        self.end_point = [-1, -1]
        self.path_to_current_pos = deepcopy(path)  # nochmal die Sache mit dem Pfad überdenken siehe Zettel
        self.distance = 0

    def set_start(self, x, y):
        self.current_pos = [x, y]

    def set_end(self, x, y):
        self.end_point[1] = y
        self.end_point[0] = x

    def add_pos_to_path(self, pos):
        self.path_to_current_pos.append(pos)

    def get_path_to_pos(self):
        return self.path_to_current_pos

    def get_neighbors_of_coord(self):
        neighbors_of_current_pos = []
        up = [self.current_pos[0], self.current_pos[1] - 1]  # definition of upper coord based from current position
        down = [self.current_pos[0], self.current_pos[1] + 1]  # definition of lower coord
        left = [self.current_pos[0] - 1, self.current_pos[1]]  # definition of left coord
        right = [self.current_pos[0] + 1, self.current_pos[1]]  # definition of right coord

        if self.labyrinth_object.get_field_value(self.current_pos[1] - 1,  # check if field can be visited
                                                 self.current_pos[0]) == 0 \
                and up not in self.labyrinth_object.get_visited_list():  # check if not visited yet
            neighbors_of_current_pos.append(up)  # if checks OKAY put it as neighbor in list
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

    def set_route_global(self):  # function of interest
        temp = self.get_path_to_pos()
        #temp.sort()
        #print('path to current position:', temp)
        self.labyrinth_object.set_route(temp)

    def solve_with_visitorlist(self):
        if self.current_pos in self.labyrinth_object.get_visited_list():
            return  # end other threads if position is in list
        if self.labyrinth_object.get_solved():
            return  # end thread if other thread found exit
        if self.current_pos == self.end_point:
            self.add_pos_to_path(self.current_pos)
            self.set_route_global()  # for testing route_function
            self.labyrinth_object.print_destination(self.current_pos)  # print route with labyrinth function
            self.labyrinth_object.append_position_to_visited_list(self.current_pos)
            #print('test arg:', self.path_to_current_pos) # print route if agent thread finds it
            return
        self.labyrinth_object.append_position_to_visited_list(self.current_pos)
        self.add_pos_to_path(self.current_pos)
        neighbors_of_coord = self.get_neighbors_of_coord()  # Gibt Liste die max. 4 Elemente haben kann.
        if len(neighbors_of_coord) == 0:
            return  # [-1]
        elif len(neighbors_of_coord) == 1:
            self.current_pos = neighbors_of_coord[0]
            self.solve_with_visitorlist()
        elif len(neighbors_of_coord) > 1:                   # wenn zu einer position mehr als ein Nachbar ermittelt wird
            # print('len of neighbors:',len(neighbors_of_coord))
            for i in range(0, len(neighbors_of_coord) - 1):
                # print(neighbors_of_coord[i])
                new_agent = AgentMultiThread(self.labyrinth_object, neighbors_of_coord[i], self.path_to_current_pos)
                new_agent.set_end(self.end_point[0], self.end_point[1])
                new_thread = threading.Thread(target=new_agent.solve_with_visitorlist)
                new_thread.start()
            self.current_pos = neighbors_of_coord[len(neighbors_of_coord) - 1]
            self.solve_with_visitorlist()

    def solve_with_visitorlabyrinth(self):
        if self.labyrinth_object.is_current_pos_visited([1, 1], [1, 1]):
            print('pos visited')
        else:
            print('pos not visited')

    def get_route_to_destination_mockup(self):
        return [[1, 1], [2, 1], [2, 2], [2, 3], [1, 3]]
