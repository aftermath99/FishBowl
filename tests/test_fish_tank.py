import pytest
import logging

from fish_bowl.data_struct.fish_tank import FishTank, PacmanFishTank
from fish_bowl.data_struct.animals import Shark, Fish

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d:%(message)s")
_logger = logging.getLogger(__name__)


class TestFishTank:

    def test_insert_and_move_fish(self):

        grid_size = 10
        fish_tank = FishTank(grid_size)

        coord1 = (0, 1)
        fish1 = Fish(0, 1)
        fish_tank.put_animal(coord1, fish1)

        coord2 = (1, 1)
        fish2 = Fish(0, 1)
        fish_tank.put_animal(coord2, fish2)

        fish_tank.print_output()

        coord3 = (2, 2)
        fish_tank.move_animal(coord2, fish2, coord3)

        fish_tank.print_output()
        fish_tank_grid = fish_tank.get_grid()
        assert fish_tank_grid[coord3] == fish2

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

    def test_add_1_fish_2_sharks(self):
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
        assert len(nearby_space) == 7

        fish_tank.print_output()

        current_sharks_tuple = fish_tank.get_current_sharks()
        assert len(current_sharks_tuple) == 2

        sim_turn = 1
        for shark_coord, shark in current_sharks_tuple:
            _logger.info("Looking for fish around shark : [{}]".format(shark_coord))
            fish_tuple = fish_tank.find_fish_to_eat(shark_coord)
            _logger.info(type(fish_tuple))
            if fish_tuple is None:
                pass
            else:
                fish_coord, fish_to_eat = fish_tuple
                if shark == shark1:
                    assert fish_to_eat is not None
                fish_tank.eat_fish(1, shark_coord, fish_coord)
                if shark == shark1:
                    assert shark.last_fed == 1

        fish_tank.print_output()

    def test_get_dataframe(self):
        grid_size = 10
        fish_tank = FishTank(grid_size)

        coord1 = (0, 1)
        animal1 = "1200"
        fish_tank.put_animal(coord1, animal1)

        coord2 = (1, 1)
        animal2 = "1400"
        fish_tank.put_animal(coord2, animal2)

        pandas_df = fish_tank.create_pandas_dataframe()
        _logger.info(pandas_df.shape)
        _logger.info("dataframe: \r\n{}".format(pandas_df))

    # TODO need negative test

    def test_pacman_fishtank(self):
        grid_size = 10
        fish_tank = PacmanFishTank(grid_size)

        # add one fish at (0,0)
        fish_coord1 = (0, 0)
        fish1 = Fish(0, 1)
        fish_tank.put_animal(fish_coord1, fish1)

        # put a shark at 0,9
        shark_coord1 = (0, 9)
        shark1 = Shark(0, 1)
        fish_tank.put_animal(shark_coord1, shark1)

        fish_tuple = fish_tank.find_fish_to_eat(shark_coord1)

        _logger.info(fish_tuple)

        assert fish_tuple is not None

        coord, fish_to_eat = fish_tuple
        x, y = coord
        assert x == 0
        assert y == 0

