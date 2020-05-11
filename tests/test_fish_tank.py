import pytest
import logging

from fish_bowl.data_struct.fish_tank import FishTank
from fish_bowl.data_struct.animals import *

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d:%(message)s")
_logger = logging.getLogger(__name__)


class TestFishTank:

    def test_insert_and_get(self):

        grid_size = 10
        fish_tank = FishTank(grid_size)

        coord1 = (0, 1)
        animal1 = "012"
        fish_tank.put_animal(coord1, animal1)

        coord2 = (1, 1)
        animal2 = "014"
        fish_tank.put_animal(coord2, animal2)

        fish_tank.print_output()

        coord3 = (2, 2)
        fish_tank.move_animal(coord2, animal2, coord3)

        fish_tank.print_output()

    def test_nearby_space(self):
        _logger.info("\r\n")
        grid_size = 10
        fish_tank = FishTank(grid_size)

        # top left corner should have 3 available neighbors
        coord1 = (0, 0)
        nearby_space = fish_tank.find_available_nearby_space(coord1)
        assert len(nearby_space) == 3

        # next cell to the right should have 5 available neighbors
        coord2 = (1, 0)
        nearby_space = fish_tank.find_available_nearby_space(coord2)
        assert len(nearby_space) == 5

        # top right corner should have 3 available neighbors
        coord3 = (grid_size - 1, 0)
        nearby_space = fish_tank.find_available_nearby_space(coord3)
        assert len(nearby_space) == 3

    def test_add_1_fish(self):
        _logger.info("\r\n")
        grid_size = 10
        fish_tank = FishTank(grid_size)
        coord1 = (0, 0)

        # add one fish at (0,1) and re-test
        coord4 = (1, 0)
        fish1 = Fish(0, 1)
        fish_tank.put_animal(coord4, fish1)
        nearby_space = fish_tank.find_available_nearby_space(coord1)
        assert len(nearby_space) == 2

        fish_tank.print_output()

        shark1 = Shark(0, 1)
        shark1_coord = (1, 1)
        fish_tank.put_animal(shark1_coord, shark1)

        shark2 = Shark(0, 1)
        shark2_coord = (4, 1)
        fish_tank.put_animal(shark2_coord, shark2)

        nearby_space = fish_tank.find_available_nearby_space(shark1_coord)
        # assert len(nearby_space) == 2

        fish_tank.print_output()

    @pytest.mark.skip(reason="not implemented")
    def test_add_1_shark(self):
        _logger.info("\r\n")
        grid_size = 10
        fish_tank = FishTank(grid_size)
        coord1 = (0, 0)

        # add one fish at (0,1) and re-test
        coord4 = (1, 0)
        fish1 = Fish(0, 1)
        fish_tank.put_animal(coord4, fish1)
        nearby_space = fish_tank.find_available_nearby_space(coord1)
        assert len(nearby_space) == 2

