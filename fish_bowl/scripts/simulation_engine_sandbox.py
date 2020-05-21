import logging
import time

from fish_bowl.process.simple_simulation_engine import SimpleSimulationEngine
from fish_bowl.scripts.run_simple_simulation_engine import execute_simulation

_logger = logging.getLogger(__name__)

sim_config = {
  "grid_size": 20,
  "init_nb_fish": 150,
  "fish_breed_maturity": 2,
  "fish_breed_probability": 80,
  "fish_speed": 2,
  "init_nb_shark": 5,
  "shark_breed_maturity": 5,
  "shark_breed_probability": 30,
  "shark_speed": 4,
  "shark_starving": 4,
  'max_turns': 100
}

sim_config_empty = {
    'grid_size': 10,
    'init_nb_fish': 0,
    'fish_breed_maturity': 3,
    'fish_breed_probability': 80,
    'fish_speed': 2,
    'init_nb_shark': 0,
    'shark_breed_maturity': 5,
    'shark_breed_probability': 100,
    'shark_speed': 4,
    'shark_starving': 4,
    'max_turns': 2
}


def current_milli_time():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(filename)s:[%(lineno)d]: %(message)s")

    start_time = current_milli_time()
    execute_simulation(start_time, sim_config)
