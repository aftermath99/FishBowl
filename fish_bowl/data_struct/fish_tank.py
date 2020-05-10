

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




