import pandas as pd


class SimulationEngine:
    """
    Interface that defines main simulation methods.
    Allows different implementations for comparison purposes
    """

    def get_simulation_grid_data(self) -> pd.DataFrame:
        pass

    def _check_simulation_ends(self):
        pass

    def play_turn(self):
        pass