from typing import Dict, List, Tuple

import random
import logging
import pandas as pd

from fish_bowl.process.simulation_engine import SimulationEngine
from fish_bowl.data_struct.fish_tank import FishTank
from fish_bowl.data_struct.animals import *

_logger = logging.getLogger(__name__)

class SimpleSimulationEngine(SimulationEngine):
    start_sid = 1

    def __init__(self, simulation_parameters: Dict):
        """
        Create a simulation and link to its persistence
        :param simulation_parameters:
        """

        self._sid = SimpleSimulationEngine.start_sid
        SimpleSimulationEngine.start_sid += 1
        self._sim_turn = 0
        self._init_simulation(**simulation_parameters)
        self._simulation_parameters = simulation_parameters
        self._fish_tank = FishTank(self._grid_size)
        self._spawn()
        self.sim_ended = False

    def _init_simulation(self, grid_size, init_nb_fish, init_nb_shark, fish_breed_maturity, fish_breed_probability,
                         fish_speed, shark_breed_maturity, shark_breed_probability, shark_speed,
                         shark_starving, max_turns):
        """
        Initialize a simulation and return the sid
        :param grid_size:
        :param init_nb_fish:
        :param init_nb_shark:
        :param fish_breed_maturity:
        :param fish_breed_probability:
        :param fish_speed:
        :param shark_breed_maturity:
        :param shark_breed_probability:
        :param shark_speed:
        :param shark_starving:
        :param max_turns:
        """
        # first check some inputs
        if grid_size ** 2 < (init_nb_fish + init_nb_shark):
            raise ValueError('initial number of animals bigger than grid size....')
        assert fish_breed_maturity > 0, "fish_breed_maturity must be positive"
        assert fish_speed > 0, "fish_speed must be positive"
        assert shark_breed_maturity > 0, "shark_breed_maturity must be positive"
        assert shark_speed > 0, "shark_speed must be positive"
        assert shark_starving > 0, "shark_starving must be positive"
        # _logger.debug("init_simulation()")
        self._grid_size = grid_size
        self._init_nb_fish = init_nb_fish
        self._fish_breed_maturity = fish_breed_maturity
        self._fish_breed_probability = fish_breed_probability
        self._fish_speed = fish_speed
        self._init_nb_shark = init_nb_shark
        self._shark_breed_maturity = shark_breed_maturity
        self._shark_breed_probability = shark_breed_probability
        self._shark_speed = shark_speed
        self._shark_starving = shark_starving
        self._max_turns = max_turns

    def _spawn(self):
        """
        function to create the grid by spawning fishes and sharks initially (and only at start)
        :return:
        """
        # get simulation elements
        grid_size = self._grid_size
        coord_array = [(x, y) for x in range(grid_size) for y in range(grid_size)]
        random.shuffle(coord_array)
        # spawn fish and Sharks
        fishes = 0
        sharks = 0
        for coord in coord_array:
            if fishes < self._init_nb_fish:
                fish = Fish(self._sid, 0)
                self._fish_tank.put_animal(coord, fish)
                fishes += 1
            elif sharks < self._init_nb_shark:
                shark = Shark(self._sid, 1)
                self._fish_tank.put_animal(coord, shark)
                sharks += 1
            else:
                break
        return

    def display_simple_grid(self):
        self._fish_tank.print_output()

    def get_simulation_parameters(self, sim_id: int = None) -> Dict:
        return self._simulation_parameters

    def get_simulation_grid_data(self) -> pd.DataFrame:
        pass

    def check_simulation_ends(self):
        """
        Check if the simulation has completed. Either
        1) The max number of turns has been reached or
        2) There are no sharks in the tank
        """
        if self._sim_turn == self._max_turns:
            _logger.info('Simulation completed.  Max turns: {}'.format(self._max_turns))
            return True
            # raise Exception('Simulation completed.  Max turns: {}'.format(self._max_turns))
        elif self._fish_tank.get_current_number_sharks() == 0:
            _logger.info('Simulation completed.  No sharks remaining')
            # raise Exception('Simulation completed.  No sharks remaining')
            return True
        else:
            return False

    def play_turn(self):
        """
        Create a new turn,
        - load all animals
        check feeding -> animal dies
        shark eat
        check breading -> animal breed
        animal move (fish first then sharks)
        turn ends

        :return:
        """
        if self.sim_ended:
            # TODO throw exception
            return

        self._sim_turn += 1
        _logger.debug('********************TURN: {:<3}********************'.format(self._sim_turn))
        self._remove_dead_sharks(self._sim_turn)
        fed_sharks = self._feed_sharks()
        self._move_remaining_animals(already_moved=fed_sharks)

        _logger.debug('********************END TURN: {:<3}*******************'.format(self._sim_turn))
        self.sim_ended = self.check_simulation_ends()

    def _remove_dead_sharks(self, sim_turn):
        self._fish_tank.remove_starved_sharks(self._sim_turn, self._shark_starving)

    def _feed_sharks(self):
        pass

    def _move_remaining_animals(self, already_moved):
        pass


