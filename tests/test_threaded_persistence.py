import logging
import pytest

from fish_bowl.dataio.threaded_persistence import PersistenceClient, get_database_string
from fish_bowl.data_struct.fish_tank import FishTank
from fish_bowl.data_struct.animals import Shark, Fish
from fish_bowl.process.utils import Animal

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(filename)s:[%(lineno)d]: %(message)s")
_logger = logging.getLogger(__name__)

sim_config = {
    'sid': 1,
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


class TestThreadedPersistence:
    """
    Tests for Threaded PersistenceClient
    Intended to create a multi threaded persistence client
    TODO incomplete
    """

    def test_persist_to_db(self):
        """
        Test the calls made in SimpleSimulationEngine.persist_to_db()
        """
        grid_size = 10
        fish_tank = FishTank(grid_size)
        simulation_id = 1

        coord4 = (1, 0)
        fish1 = Fish(simulation_id, 1)
        fish_tank.put_animal(coord4, fish1)

        shark1 = Shark(simulation_id, 1)
        shark1_coord = (1, 1)
        fish_tank.put_animal(shark1_coord, shark1)

        shark2 = Shark(simulation_id, 1)
        shark2_coord = (4, 1)
        fish_tank.put_animal(shark2_coord, shark2)
        shark_oid = shark2.oid

        # client = PersistenceClient(get_database_string())
        # use memory for unit tests
        client = PersistenceClient('sqlite:///:memory:')
        client.save_sim_params(**sim_config)
        fish_tank_grid = fish_tank.get_grid()

        for coord, animal in fish_tank_grid.items():
            x, y = coord
            client.save_animal(animal.oid, animal.sim_id, animal.animal_type, animal.spawn_turn,
                               animal.breed_count, animal.last_breed, animal.last_fed, animal.alive, x, y)

        animal_details = client.get_animal(shark_oid)
        assert animal_details.animal_type == Animal.Shark
        assert animal_details.sim_id == 1

    def test_persist_simstats(self):
        client = PersistenceClient('sqlite:///:memory:')
        client.save_simstats(2, 10, 8, 1, 5)

        sim_stats = client.get_simstats(2)
        assert sim_stats.fish_breed_total == 8
        assert sim_stats.shark_starved_total == 5

    @pytest.mark.skip(reason="Incomplete")
    def test_tank_functions(self):
        client = PersistenceClient(get_database_string())
        grid_string = "0000 1111 0000\r\n1112 0000 0000"
        client.save_tankgrid(1, 1, grid_string)

        grid_repr = client.get_tankgrid(1, 1)

        _logger.info("grid id: {}, grid: {}".format(grid_repr.tank_grid_id, grid_repr.grid))

