import logging

from fish_bowl.process.topology import *

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
        self._grid[coord] = animal
        # check using objects as keys in dict
        self._shark_dict[animal] = coord
        # TODO if animal is shark, elif, etc

    def move_animal(self, old_coord, animal, new_coord):
        animal_in_grid = self._grid.pop(old_coord, None)
        # should check old vs new animal
        self._grid[new_coord] = animal

    def get_grid(self):
        return self._grid

    def check_animal(self, coord):
        if coord in self._grid:
            animal = self._grid[coord]
            return animal
        else:
            return None

    def find_available_nearby_space(self, start_coordinate, shuffle: bool = True):
        """
        for a given coordinate, return all available neighbours
        :param start_coordinate: starting coordinate tuple
        :param shuffle: boolean to shuffle the return coordinates
        :return: List of free neighboring coordinates
        """
        # build coordinate
        # check if occupied
        available_neighbors = []
        startx, starty = start_coordinate
        for k, (x, y) in SQUARE_NEIGH.items():
            new_coord = (startx + x, starty + y)
            if self.is_valid_grid_coord(coordinates=new_coord, raise_err=False):
                animal = self.check_animal(new_coord)
                if animal is None:
                    available_neighbors.append(new_coord)

        if shuffle:
            random.shuffle(available_neighbors)
        _logger.debug("find_available_nearby_space() - {}".format(available_neighbors))
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
        print("")
        for x in range(0, self.grid_size - 1):
            for y in range(0, self.grid_size - 1):
                coord = (x, y)
                if coord in self._grid:
                    animal = self._grid[(x, y)]
                    print("{} ".format(animal), end='')
                else:
                    print("000 ", end='')
            print("")




