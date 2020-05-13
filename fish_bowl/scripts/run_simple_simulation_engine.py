import logging
import argparse
import time

from fish_bowl.process.simple_simulation_engine import SimpleSimulationEngine
from fish_bowl.common.config_reader import read_simulation_config

_logger = logging.getLogger(__name__)


def current_milli_time():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(filename)s:[%(lineno)d]: %(message)s")

    total_start_time = current_milli_time()
    cmd_parser = argparse.ArgumentParser()
    cmd_parser.add_argument('--config_name', default='simulation_config_1',
                            help='Simulation configuration file name')
    cmd_parser.add_argument('--max_turn', default=100, type=int, help='Maximum number of turns for the simulation')
    cmd_parser.add_argument('--config_path', default=None, type=str,
                            help="""
                            Configuration file path. If specified, configuration file will be loaded from this path
                            """)
    args = cmd_parser.parse_args()
    if args.config_path is not None:
        raise NotImplementedError('Code for directing to an alternative configuration'
                                  ' repository has not been implemented yet')
    # Load simulation configuration
    sim_config = read_simulation_config(args.config_name)

    simulation_engine = SimpleSimulationEngine(sim_config)
    simulation_engine.display_simple_grid()
    _logger.info('max_turns: {}'.format(simulation_engine.max_turns))

    for sim_turn in range(simulation_engine.max_turns):
        start_time = current_milli_time()
        _logger.info('Turn: {}'.format(simulation_engine.sim_turn))
        try:
            simulation_engine.play_turn()
            simulation_engine.display_simple_grid()
        except Exception as e:
            _logger.error(e)
            break
        end_time = current_milli_time()
        _logger.warning('Turn {} duration: {} ms'.format(sim_turn, (end_time - start_time)))
        if simulation_engine.sim_ended:
            _logger.warning("Simulation has ended")
            break

    total_end_time = current_milli_time()
    _logger.warning('Total duration: {} ms'.format(total_end_time - total_start_time))
    simulation_engine.print_stats()
