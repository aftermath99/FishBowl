from typing import Dict, List, Tuple

import random
import logging
import pandas as pd

from fish_bowl.process.simulation_engine import SimulationEngine
from fish_bowl.data_struct.fish_tank import FishTank, PacmanFishTank
from fish_bowl.data_struct.animals import *

from fish_bowl.dataio.threaded_persistence import PersistenceClient, get_database_string, Animals

_logger = logging.getLogger(__name__)


class SimpleSimulationEngine(SimulationEngine):
    start_sid = 1

    def __init__(self, simulation_parameters: Dict, use_pacman=False):
        """
        Create a simulation and link to its persistence
        :param simulation_parameters:
        """
        self._sid = SimpleSimulationEngine.start_sid
        SimpleSimulationEngine.start_sid += 1
        self._sim_turn = 0
        self._init_simulation(**simulation_parameters)
        self._simulation_parameters = simulation_parameters
        if use_pacman:
            self._fish_tank = PacmanFishTank(self._grid_size)
        else:
            self._fish_tank = FishTank(self._grid_size)
        self._spawn()
        self.sim_ended = False

        self._fish_eaten_total = 0
        self._fish_breed_total = 0
        self._shark_breed_total = 0

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
        _logger.info("\r\nDisplay grid, turn {}".format(self._sim_turn))
        _logger.info(self._fish_tank)

    def get_simulation_parameters(self, sim_id: int = None) -> Dict:
        return self._simulation_parameters

    def get_simulation_grid_data(self) -> pd.DataFrame:
        grid_data_frame = self._fish_tank.create_pandas_dataframe()
        return grid_data_frame

    def _check_simulation_ends(self):
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

    def print_stats(self):
        """
        Print accumulated stats
        """
        _logger.info('print_stats() - sharks bred: {}, fish bred: {}, fish eaten: {}'.format(self._shark_breed_total,
                                                                                             self._fish_breed_total,
                                                                                             self._fish_eaten_total))

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
        fed_sharks_oid_dict = self._feed_sharks()
        fed_and_moved_oid_list = self._breed_animals(fed_sharks_oid_dict=fed_sharks_oid_dict)
        self._move_remaining_animals(already_moved_oid_list=fed_and_moved_oid_list)

        _logger.debug('********************END TURN: {:<3}*******************'.format(self._sim_turn))
        self.sim_ended = self._check_simulation_ends()
        if self.sim_ended:
            self.persist_to_db()

    def _remove_dead_sharks(self, sim_turn):
        self._fish_tank.remove_starved_sharks(self._sim_turn, self._shark_starving)

    def _feed_sharks(self):
        fed_sharks_oid_dict = {}
        current_sharks_tuple_list = self._fish_tank.get_current_sharks()
        for shark_coord, shark in current_sharks_tuple_list:
            _logger.debug("_feed_sharks() - Looking for fish around shark ({}) : [{}]".format(shark.oid, shark_coord))
            fish_tuple = self._fish_tank.find_fish_to_eat(shark_coord)
            if fish_tuple is None:
                pass
            else:
                fish_coord, fish_to_eat = fish_tuple
                self._fish_tank.eat_fish(self._sim_turn, shark_coord, fish_coord)
                self._fish_eaten_total += 1
                fed_sharks_oid_dict[shark.oid] = shark_coord
        return fed_sharks_oid_dict

    def _move_remaining_animals(self, already_moved_oid_list):
        fish_tank_grid = self._fish_tank.get_grid()
        for coord, animal in fish_tank_grid.copy().items():
            if animal.oid not in already_moved_oid_list:
                _logger.debug("_move_remaining_animals() - looking at animal ({}) in [{}]".format(animal.oid, coord))
                available_neighbors = self._fish_tank.find_available_nearby_space(coord)
                if len(available_neighbors) > 0:
                    move_coord = available_neighbors[0]
                    self._fish_tank.move_animal(coord, animal, move_coord)
                    _logger.debug("_move_remaining_animals() - move animal ({}) to [{}]".format(animal.oid, move_coord))

    def _breed_animals(self, fed_sharks_oid_dict):
        """
        Breed animals where possible
        Sharks first, but must check if they have fed (which indicates movement)
        :param fed_sharks_oid_dict: dict of shark oid to original coords in turn. Tracks already moved animals.
        """
        already_moved_animals = fed_sharks_oid_dict
        fish_tank_grid = self._fish_tank.get_grid()
        for coord, animal in fish_tank_grid.copy().items():
            if animal.animal_type == Animal.Shark:
                self._breed_shark(animal, coord, already_moved_animals)
        for coord, animal in fish_tank_grid.copy().items():
            if animal.animal_type == Animal.Fish:
                self._breed_fish(animal, coord, already_moved_animals)
        return already_moved_animals
        # TODO collect Audit actions

    def _breed_fish(self, animal, coord, already_moved_animals):
        if (self._sim_turn - animal.spawn_turn) >= self._fish_breed_maturity:
            # fish can breed
            if random.randint(0, 100) <= self._fish_breed_probability:
                # always use the underlying grid to check availability and for puts
                available_neighbors = self._fish_tank.find_available_nearby_space(coord)
                if len(available_neighbors) > 0:
                    baby_fish = Fish(self._sid, self._sim_turn)
                    move_parent_coord = available_neighbors[0]
                    self._fish_tank.move_animal(coord, animal, move_parent_coord)
                    _logger.debug("_breed_fish() - move parent fish ({}) to [{}]".format(animal.oid, move_parent_coord))
                    already_moved_animals[animal.oid] = coord
                    self._fish_tank.put_animal(coord, baby_fish)
                    _logger.debug("_breed_fish() - new fish ({}) at [{}]".format(baby_fish.oid, coord))
                    self._fish_breed_total += 1

    def _breed_shark(self, animal, coord, already_moved_animals):
        if (self._sim_turn - animal.spawn_turn) >= self._shark_breed_maturity:
            # shark can breed
            if random.randint(0, 100) <= self._shark_breed_probability:
                if animal.oid in already_moved_animals:
                    animal.breed_count += 1
                    animal.last_breed = self._sim_turn
                    baby_shark = Shark(self._sid, self._sim_turn)
                    # use original coord
                    breed_coord = already_moved_animals[animal.oid]
                    self._fish_tank.put_animal(breed_coord, baby_shark)
                    _logger.debug(
                        "_breed_shark() - new shark ({}) to [{}] from parent ({})".format(baby_shark.oid, breed_coord,
                                                                                          animal.oid))
                    self._shark_breed_total += 1

                else:
                    available_neighbors = self._fish_tank.find_available_nearby_space(coord)
                    if len(available_neighbors) > 0:
                        animal.breed_count += 1
                        animal.last_breed = self._sim_turn
                        baby_shark = Shark(self._sid, self._sim_turn)
                        move_parent_coord = available_neighbors[0]
                        self._fish_tank.move_animal(coord, animal, move_parent_coord)
                        _logger.debug(
                            "_breed_shark() - move parent shark ({}) to [{}]".format(animal.oid, move_parent_coord))
                        already_moved_animals[animal.oid] = coord
                        self._fish_tank.put_animal(coord, baby_shark)
                        _logger.debug("_breed_shark() - new shark ({}) at [{}]".format(baby_shark.oid, coord))
                        self._shark_breed_total += 1

    @property
    def sim_turn(self):
        return self._sim_turn

    @property
    def max_turns(self):
        return self._max_turns

    def persist_to_db(self):
        """
        Persist all audit actions to database
        TODO Should accumulate audit actions within the simulation engine and call this method with a batch of items
        rather than single calls to the database for each object
        """
        client = PersistenceClient(get_database_string())
        sim_params = self._simulation_parameters
        sim_params["sid"] = self._sid
        client.save_sim_params(**sim_params)
        fish_tank_grid = self._fish_tank.get_grid()
        for coord, animal in fish_tank_grid.items():
            x, y = coord
            client.save_animal(animal.oid, self._sid, animal.animal_type, animal.spawn_turn,
                               animal.breed_count, animal.last_breed, animal.last_fed, animal.alive, x, y)
