import pytest
from fish_bowl.data_struct.fish_tank import FishTank


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
