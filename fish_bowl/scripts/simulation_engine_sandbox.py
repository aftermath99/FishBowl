import logging
import time

from fish_bowl.process.simple_simulation_engine import SimpleSimulationEngine

_logger = logging.getLogger(__name__)

sim_config = {
    'grid_size': 10,
    'init_nb_fish': 50,
    'fish_breed_maturity': 3,
    'fish_breed_probability': 80,
    'fish_speed': 2,
    'init_nb_shark': 5,
    'shark_breed_maturity': 5,
    'shark_breed_probability': 100,
    'shark_speed': 4,
    'shark_starving': 4,
    'max_turns': 2
}

sim_config_2 = {
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

    total_start_time = current_milli_time()
    simulation_engine = SimpleSimulationEngine(sim_config_2)
    simulation_engine.display_simple_grid()
    _logger.info('max_turns: {}'.format(simulation_engine.max_turns))

    for sim_turn in range(simulation_engine.max_turns):
        start_time = current_milli_time()
        _logger.info('Turn: {}'.format(simulation_engine.sim_turn))
        try:
            simulation_engine.play_turn()
            simulation_engine.display_simple_grid()
        except Exception as e:
            _logger.error(e)
            break
        end_time = current_milli_time()
        _logger.warning('Turn {} duration: {} ms'.format(sim_turn, (end_time - start_time)))
        if simulation_engine.sim_ended:
            _logger.warning("Simulation has ended")
            break

    total_end_time = current_milli_time()
    _logger.warning('Total duration: {} ms'.format(total_end_time - total_start_time))
    simulation_engine.print_stats()
