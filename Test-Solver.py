

from labyrinth import *
from agent import *

labyrinth = Labyrinth(2, 3)
labyrinth.print_labyrinth()
labyrinth.toggle_wall(1,2)
labyrinth.print_labyrinth()

agent = Agent(labyrinth.get_data_model(), [0,0], 0)
agent.set_start(1,1)
agent.set_end(1,3)

agent.solve()
