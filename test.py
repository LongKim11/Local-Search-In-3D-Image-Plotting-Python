from search import *
from problem import *


p = Problem('monalisa.jpg')

# Test Random Restart Hill Climbing Algorithm
# rand_restart_hlb = LocalSearchStrategy()
# path = rand_restart_hlb.random_restart_hill_climbing(p, 11)
# p.show()
# p.draw_path(path)


# Test Simulated Annealing Search Algorithm
# sa = LocalSearchStrategy()
# schedule = sa.schedule()
# path = sa.simulated_annealing_search(p, schedule)

# p.show()
# p.draw_path(path)


# Test Local Beam Search Algorithm
lbs = LocalSearchStrategy()
path = lbs.local_beam_search(p, 3)

p.show()
p.draw_path(path)

