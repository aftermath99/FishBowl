import pandas as pd
from fish_bowl.dataio.persistence import Simulation


class SimulationEngine:
    """
    Interface that defines main simulation methods.
    Allows different implementations for comparison purposes
    """

    def get_simulation_grid_data(self) -> pd.DataFrame:
        pass

    def check_simulation_ends(self):
        pass

    def play_turn(self):
        pass