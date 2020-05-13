import logging
from typing import Dict, List, Tuple
import random
import pandas as pd

from fish_bowl.process.topology import SQUARE_NEIGH, TopologyError
from fish_bowl.process.utils import Animal

_logger = logging.getLogger(__name__)


class FishTank(object):
    """
    Fish tank will hold the state of the grid and provide helper methods
    """

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self._grid = {}
        self._shark_dict = {}
        self._fish_dict = {}

    def put_animal(self, coord, animal):
        """
        Place an animal into the fish tank grid
        :param coord: coordinate tuple
        :param animal: Animal to put in such as Fish and Shark
        """
        # _logger.debug("put_animal() - animal ({}) at [{}]".format(animal.oid, coord))
        self._grid[coord] = animal

    def move_animal(self, old_coord, animal, new_coord):
        """
        Move any animal
        :param old_coord: Start coordinates
        :param animal: Animal to move
        :param new_coord: Target coordinates to move to
        """
        move_animal = self._grid.pop(old_coord)
        if move_animal.oid != animal.oid:
            raise Exception("move_animal() - Request animal oid ({}) is not "
                            "the same oid as the current occupant ({})".format(animal.oid, move_animal.oid))
        self._grid[new_coord] = move_animal

    def get_grid(self):
        return self._grid

    def check_animal(self, coord):
        """
        Check if an animal exists in the coordinates
        :param coord: Coordinates to check
        :return: animal if found
        """
        if coord in self._grid:
            animal = self._grid[coord]
            return animal
        else:
            return None

    def get_current_number_sharks(self) -> int:
        """
        Count the current number of sharks in the Fish Tank
        """
        number_sharks = 0
        for coord, animal in self._grid.items():
            if animal.animal_type == Animal.Shark:
                number_sharks += 1
        return number_sharks

    def remove_starved_sharks(self, current_turn, shark_starving):
        """
        Remove starved sharks
        :param current_turn: The current simulation turn
        :param shark_starving: number of turns before a shark can starve (simulation param)
        """
        _logger.debug("remove_starved_sharks() - sim turn {}".format(current_turn))
        for coord, animal in self._grid.copy().items():
            if animal.animal_type == Animal.Shark:
                turns_not_fed = current_turn - animal.last_fed
                if turns_not_fed > shark_starving:
                    _logger.debug("remove_starved_sharks() - Removing shark ({}) at [{}]".format(animal.oid, coord))
                    self._grid.pop(coord, None)

    def get_current_sharks(self) -> List:
        """
        Get current list of sharks with coords
        :return: List of sharks and coordinates
        """
        # tuple of coord and animal
        current_sharks = []
        for coord, animal in self._grid.items():
            if animal.animal_type == Animal.Shark:
                current_sharks.append((coord, animal))
        return current_sharks

    def find_fish_to_eat(self, coord) -> Tuple:
        """
        Given a shark coordinate, return the first available fish and it's coordinate to eat
        :param coord: coordinates to start from
        :return: Tuple of coordinate and fish
        """
        startx, starty = coord
        for k, (x, y) in SQUARE_NEIGH.items():
            new_coord = self._generate_find_coordinate(startx, starty, x, y)
            if self.is_valid_grid_coord(coordinates=new_coord, raise_err=False):
                # normally this should be trace
                _logger.debug("find_fish_to_eat() - Looking for fish at : [{}]".format(new_coord))
                animal = self.check_animal(new_coord)
                if animal is None:
                    continue
                if animal.animal_type == Animal.Fish:
                    _logger.debug("find_fish_to_eat() - Found fish at : [{}]".format(new_coord))
                    return new_coord, animal

    def eat_fish(self, sim_turn, shark_coord, fish_coord):
        """
        A shark eats a fish given both coordinates
        :param sim_turn: current simulation turn
        :param shark_coord: shark coordinates
        :param fish_coord: fish coordinates
        """
        shark_eater = self._grid[shark_coord]
        fish_eaten = self._grid.pop(fish_coord)
        fish_eaten.alive = False

        self.move_animal(shark_coord, shark_eater, fish_coord)
        shark_eater.last_fed = sim_turn
        _logger.debug("eat_fish() - Shark {} has eaten fish {} at [{}]".format(shark_eater.oid, fish_eaten.oid,
                                                                               fish_coord))

    def _generate_find_coordinate(self, startx, starty, x, y) -> Tuple:
        """
        Generates next coordinate to look for cell evaluation
        created to allow different grid topologies
        """
        new_coord = (startx + x, starty + y)
        return new_coord

    def find_available_nearby_space(self, start_coordinate, shuffle: bool = True) -> List[Tuple]:
        """
        for a given coordinate, return all available neighbours
        :param start_coordinate: starting coordinate tuple
        :param shuffle: boolean to shuffle the return coordinates
        :return: List of free neighboring coordinates
        """
        available_neighbors = []
        startx, starty = start_coordinate
        for k, (x, y) in SQUARE_NEIGH.items():
            new_coord = self._generate_find_coordinate(startx, starty, x, y)
            if self.is_valid_grid_coord(coordinates=new_coord, raise_err=False):
                animal = self.check_animal(new_coord)
                if animal is None:
                    available_neighbors.append(new_coord)

        if shuffle:
            random.shuffle(available_neighbors)
        # _logger.debug("find_available_nearby_space() - {}".format(available_neighbors))
        return available_neighbors

    # is_valid_grid_coord (different shapes and/or pacman style)
    def is_valid_grid_coord(self, coordinates, raise_err: bool = True) -> bool:
        """
        Check coordinate are valid in a square grid
        :param coordinates: coordinate tuple to check
        :param raise_err: if an exception should be thrown
        :return: boolean if the coordinate is acceptable
        """
        x, y = coordinates
        err = []
        if x < 0:
            err.append("x coordinate must be positive")
        if y < 0:
            err.append("y coordinate must be positive")
        if x >= self.grid_size:
            err.append("x coordinate must be less than grid_size -1 = {}".format(self.grid_size - 1))
        if y >= self. grid_size:
            err.append("y coordinate must be less than grid_size -1 = {}".format(self.grid_size - 1))
        if len(err) > 0:
            if raise_err:
                raise TopologyError(', '.join(err))
            else:
                return False
        return True

    def print_output(self):
        """
        Simple debug output print of grid
        """
        print("")
        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                coord = (x, y)
                if coord in self._grid:
                    animal = self._grid[(x, y)]
                    print("{} ".format(animal), end='')
                else:
                    print("0000 ", end='')
            print("")

    def create_pandas_dataframe(self) -> pd.DataFrame:
        """
        Generate a Pandas dataframe representation
        """
        string_rep_list = []
        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                coord = (x, y)
                if coord in self._grid:
                    animal = self._grid[(x, y)]
                    string_rep_list.append("{}".format(animal))
                else:
                    string_rep_list.append("0000")
        grid_data_frame = pd.array(string_rep_list, dtype="string")
        return grid_data_frame

    def __repr__(self):
        str_repr = "\r\n"
        for y in range(0, self.grid_size):
            row_list = []
            for x in range(0, self.grid_size):
                coord = (x, y)
                if coord in self._grid:
                    animal = self._grid[(x, y)]
                    row_list.append("{}".format(animal))
                else:
                    row_list.append("0000")
            str_repr += " ".join(row_list) + "\r\n"
        return str_repr


class PacmanFishTank(FishTank):
    """
    Demonstrate how to allow pacman style grid topology
    """
    def __init__(self, grid_size):
        super().__init__(grid_size)

    def _generate_find_coordinate(self, startx, starty, x, y):
        """
        Pacman specific coordinate generator
        Allows movement beyond an edge to wrap around to the opposite edge for both x and y
        """
        newx = startx + x
        if newx < 0:
            newx = self.grid_size - 1
        elif newx > self.grid_size - 1:
            newx = newx - self.grid_size
        newy = starty + y
        if newy < 0:
            newy = self.grid_size - 1
        elif newy > self.grid_size - 1:
            newy = newy - self.grid_size
        new_coord = (newx, newy)
        return new_coord
