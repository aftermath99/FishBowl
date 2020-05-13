# Fish Bowl
A predator-prey simulator that aims to simulate very simple ecosystem.

## Setup
Use the attached simul-dev.txt file to create a conda environment for the simulation.
To run a demo simulation, use the simple_simulation.py in fish_bowl/scripts.

## Create a simulation config
New simulation configuration files can be added in fish_bowl/configuration folder. They must be '.json' files  with the below element specified:

{
  "grid_size": 20,
  "init_nb_fish": 150,
  "fish_breed_maturity": 2,
  "fish_breed_probability": 0.8,
  "fish_speed": 2,
  "init_nb_shark": 5,
  "shark_breed_maturity": 5,
  "shark_breed_probability": 0.8,
  "shark_speed": 4,
  "shark_starving": 4
}
### grid_size:
grids are squares with grid_size cell per side.
### init_nb_fish / sharks:
Specify the initial population for both fish and sharks
### fish/shark_breed_maturity:
Set number of turn from which fish/sharks can reproduce after they have spawn. From that moment, they can breed at any turn.
### fish/sharks_breed_probability:
If a shark or fish has reached the maturity to reproduce, then it can do so at each turn with this probability.
### fish/shark_speed:
How many cells a fish/shark can move at each turn (Not Implemented)
### shark_starving:
Number of turn a shark can live without feeding. Shark dies if they are not fed after this number of turns.
Note, fish do not starve.

## Simulation rules:
- Only a single living animal is allowed per cell at each turn
- Shark can eat any fish adjacent to its cell. Shark moves into the eaten fish cell.
- Shark dies of starvation at the beginning of the turn {shark_starving} turns after they last dinner.
- In order to breed, shark/fish need to have a free space around them. When breeding, parent move to the free cell and child spawn into original cell
- A shark can eat and breed(in the same turn). In this case, the spawning cell is the shark initial cell (before it had eaten)
- A shark that has eaten do not move (as he already has moved to the fish cell)
- Simulation ends when set number of turn have been performed of if there is no more sharks on the grid.

## Assignment:
* Is the code behaving like it should, reading the simulation rules
* Is the code sufficiently tested? If not, what is missing, add test with comments.
* The simulation code is quite slow. what can be done to speed it up?
* Implement the code change so we can have simulation run in around 1sec for a 20 sized grid on a normal PC. (we look for a 50x improvement in speed)
* Add action and stats recording to the simulation persistence for each turn.
* Make the simulation topology agnostic. Add infinite grid (pacman style) topology
* We would like to distribute these simulations to run 100 of them at the same time. What need to be changed in the code structure.

## Code tests pass

================================================== test session starts ==================================================
platform linux -- Python 3.7.4, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /opt/work/personal/FishBowl
collected 15 items                                                                                                      

test_base.py ....                                                                                                 [ 26%]
test_database_utils.py .                                                                                          [ 33%]
test_fish_tank.py .                                                                                               [ 40%]
test_persistence.py .....                                                                                         [ 73%]
test_topology.py ...                                                                                              [ 93%]
test_utils.py .                                                                                                   [100%]

================================================== 15 passed in 1.14s ===================================================

Test Coverage:
~86%


