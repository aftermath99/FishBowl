import pytest
import logging

from fish_bowl.data_struct.fish_tank import FishTank
from fish_bowl.data_struct.animals import Shark, Fish
from fish_bowl.process.simple_simulation_engine import SimpleSimulationEngine

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d:%(message)s")
_logger = logging.getLogger(__name__)

sim_config = {
    'grid_size': 10,
    'init_nb_fish': 50,
    'fish_breed_maturity': 3,
    'fish_breed_probability': 80,
    'fish_speed': 2,
    'init_nb_shark': 5,
    'shark_breed_maturity': 5,
    'shark_breed_probability': 100,
    'shark_speed': 4,
    'shark_starving': 1,
    'max_turns': 4
}


class TestSimulationEngine:

    @pytest.mark.skip(reason="works")
    def test_simulation_init(self):
        simple_sim_engine = SimpleSimulationEngine(sim_config)
        simple_sim_engine.display_simple_grid()

    def test_shark_starvation(self):
        simple_sim_engine = SimpleSimulationEngine(sim_config)
        simple_sim_engine.display_simple_grid()

        for sim_turn in range(sim_config["max_turns"]):
            simple_sim_engine.play_turn()
            simple_sim_engine.display_simple_grid()
            if simple_sim_engine.sim_ended:
                break





