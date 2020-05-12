import logging

from fish_bowl.dataio.threaded_persistence import PersistenceClient, get_database_string

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(filename)s:[%(lineno)d]: %(message)s")
_logger = logging.getLogger(__name__)


class TestThreadedPersistence:
    """
    Tests for Threaded PersistenceClient
    TODO incomplete
    """

    def test_tank_functions(self):
        client = PersistenceClient(get_database_string())
        grid_string = "0000 1111 0000\r\n1112 0000 0000"
        client.save_tankgrid(1, 1, grid_string)

        grid_repr = client.get_tankgrid(1,1)

        _logger.info("grid id: {}, grid: {}".format(grid_repr.tank_grid_id, grid_repr.grid))

