import Labyrinth
from AgentMultiThread import *
from AgentSingleThread import *

run_single_thread_example = False
run_multi_thread_example = True

##########################
# single thread solving  #
##########################

if run_single_thread_example:
    labyrinth_object = Labyrinth(3, 5)
    labyrinth_object.print_labyrinth()
    labyrinth_object.toggle_wall(1, 2)
    labyrinth_object.print_labyrinth()

    agent = AgentSingleThread(labyrinth_object.get_data_model(), [1, 1], 0)
    agent.set_start(1, 4)
    agent.set_end(1, 1)

    agent.solve_single_thread()
    agent.build_route_to_end()

########################
# multi thread solving #
########################

if run_multi_thread_example:
    labyrinth_object = Labyrinth(5, 5)
    labyrinth_object.print_labyrinth()
    # labyrinth_object.toggle_wall(1, 2)
    # labyrinth_object.print_labyrinth()

    agent = AgentMultiThread(labyrinth_object, [1, 1])
    agent.set_end(5, 4)

    agent.solve_multi_thread()
    print('visited list:', agent.labyrinth_object.get_visited_list())

#########
# Tests #
#########

# test_labyrinth = Labyrinth(3, 10)
