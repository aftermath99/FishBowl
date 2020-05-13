import logging

from fish_bowl.common.config_reader import read_simulation_config, save_simulation_config

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d:%(message)s")
_logger = logging.getLogger(__name__)

test_config = {
  "grid_size": 20,
  "init_nb_fish": 38,
  "fish_breed_maturity": 2,
  "fish_breed_probability": 80,
  "fish_speed": 2,
  "init_nb_shark": 5,
  "shark_breed_maturity": 5,
  "shark_breed_probability": 30,
  "shark_speed": 4,
  "shark_starving": 4,
  "max_turns": 27
}


class TestConfigReader:
    """
    Test methods in config_reader
    """

    def test_write_read_config(self):
        save_simulation_config(test_config, "ftest", True)

        loaded_sim_config = read_simulation_config("ftest")

        assert loaded_sim_config["max_turns"] == 27


