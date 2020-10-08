import Labyrinth
from AgentMultiThread import *
from AgentSingleThread import *

run_single_thread_example = False
run_multi_thread_example = True
run_simple_tests = False

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
    labyrinth_object = Labyrinth(10, 10)
    labyrinth_object.print_labyrinth()
    # labyrinth_object.toggle_wall(1, 2)
    labyrinth_object.toggle_wall(3, 1)
    labyrinth_object.toggle_wall(3, 2)
    labyrinth_object.print_labyrinth()

    agent = AgentMultiThread(labyrinth_object, [1, 1], [])
    agent.set_end(4, 1)
    agent.solve_with_visitorlist()
    # = 0
    # while len(agent.labyrinth_object.get_route()) == 0:  # sometimes shit happens to get valid result
    #    i += 1
    #    print('i:', i)
    #    agent.solve_with_visitorlist()
    print('Test-Solver: get route:', agent.labyrinth_object.get_route())
    # print('visited list:', agent.labyrinth_object.get_visited_list()) # if all solve_multithread is sys.exit instead of return
    # this message can not be printed

#########
# Tests #
#########

# test_labyrinth = Labyrinth(3, 10)
if run_simple_tests:
    print()
    print('################### NEW TESTS ###################')
    print()
    neighbors = [[1, 2], [2, 1], [1, 0]]
    for i in range(0, len(neighbors) - 1):
        print('in loop:', neighbors[i])

    print('outside the loop:', neighbors[len(neighbors) - 1])
