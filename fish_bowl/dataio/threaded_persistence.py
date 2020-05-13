import logging
import os
import datetime as dt

from fish_bowl.dataio.database import SQLAlchemyQueries
from fish_bowl.process.utils import ImpossibleAction, Animal

from sqlalchemy import Column, DateTime, Float, ForeignKey, Enum, Boolean, Integer, String
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base

_logger = logging.getLogger(__name__)

DB_LOC = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'simuldb.db'))

Base = declarative_base()
schema = 'main'  # in sqlite, schema is always main, in other db, look for the owner schema name


def get_database_string():
    return r'sqlite:///{}'.format(DB_LOC)


class FishTankGrid(Base):
    __tablename__ = 'FISHTANKGRID'
    tank_grid_id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(Integer)
    sim_turn = Column(Integer)
    grid = Column(String(500))

    __table_args__ = ({'schema': schema})


class Simulation(Base):
    __tablename__ = 'SIMULATIONS'
    int_sid = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(Integer)
    timestamp = Column(DateTime)
    grid_size = Column(Integer)
    init_nb_fish = Column(Integer)
    fish_breed_maturity = Column(Integer)
    fish_breed_probability = Column(Integer)
    fish_speed = Column(Integer)
    init_nb_shark = Column(Integer)
    shark_breed_maturity = Column(Integer)
    shark_breed_probability = Column(Integer)
    shark_speed = Column(Integer)
    shark_starving = Column(Integer)
    max_turns = Column(Integer)

    __table_args__ = ({'schema': schema})

    @validates('shark_breed_probability', 'fish_breed_probability')
    def validate_proba(self, key, value):
        if value < 0 or value > 100:
            raise ValueError('{} must be between 0 and 100, not {}'.format(key, value))
        else:
            return value


class Animals(Base):
    __tablename__ = 'ANIMALS'
    int_oid = Column(Integer, primary_key=True, autoincrement=True)
    oid = Column(Integer)
    sim_id = Column(ForeignKey("{}.{}.sid".format(schema, Simulation.__tablename__)))
    animal_type = Column(Enum(Animal))
    spawn_turn = Column(Integer)
    breed_count = Column(Integer)
    last_breed = Column(Integer)
    last_fed = Column(Integer)
    alive = Column(Boolean)
    coord_x = Column(Integer)
    coord_y = Column(Integer)

    __table_args__ = ({'schema': schema})

    def __repr__(self):
        if self.alive:
            type_display = self.animal_type.name
        else:
            type_display = 'Dead_{}'.format(self.animal_type.name)
        return "<oid={oid}: {type} :x={x:>3}, y={y:>3}".format(oid=self.oid, type=type_display, x=self.coord_x,
                                                               y=self.coord_y)


class PersistenceClient(SQLAlchemyQueries):
    """
    The PersistenceClient offloads the persistence to storage (eg. Database)
    from the SimulationEngine
    It should use a queue and separate thread to run inserts and also use bulk inserts per simulation
    Note: SQLLite is not designed for performance
    """

    def __init__(self, database_url):
        super().__init__(database_url=database_url, declarative_base=Base, expire_on_commit=False)

    def save_sim_params(self, sid, grid_size, init_nb_fish, init_nb_shark, fish_breed_maturity, fish_breed_probability,
                        fish_speed, shark_breed_maturity, shark_breed_probability, shark_speed,
                        shark_starving, max_turns):
        """
        Save simulation parameters for a given simulation
        """
        _logger.debug("save_sim_parmams")
        sim_params = Simulation(timestamp=dt.datetime.now(), sid=sid, grid_size=grid_size, init_nb_fish=init_nb_fish,
                                init_nb_shark=init_nb_shark, fish_breed_maturity=fish_breed_maturity,
                                fish_breed_probability=fish_breed_probability,
                                fish_speed=fish_speed, shark_breed_maturity=shark_breed_maturity,
                                shark_breed_probability=shark_breed_probability, shark_speed=shark_speed,
                                shark_starving=shark_starving, max_turns=max_turns)
        with self.session_scope() as s:
            s.add(sim_params)
            s.flush()

    def save_animal(self, oid, sim_id, animal_type, spawn_turn, breed_count, last_breed, last_fed, alive, coord_x,
                    coord_y):
        """
        Save last animal state at end of simulation
        """
        _logger.debug("save_animal")
        animal = Animals(oid=oid, sim_id=sim_id, animal_type=animal_type, spawn_turn=spawn_turn,
                         breed_count=breed_count, last_breed=last_breed, last_fed=last_fed, alive=alive,
                         coord_x=coord_x, coord_y=coord_y)
        with self.session_scope() as s:
            s.add(animal)
            s.flush()

    def save_tankgrid(self, sid, sim_turn, grid_str):
        """
        Capture the state of the tank as a string
        """
        _logger.debug("save_tankgrid")
        tank_grid = FishTankGrid(sid=sid, sim_turn=sim_turn, grid=grid_str)
        with self.session_scope() as s:
            s.add(tank_grid)
            s.flush()

    def get_tankgrid(self, sid: int, sim_turn: int) -> FishTankGrid:
        """
        Retrieve the state of the tank as a string
        """
        _logger.debug("get_tankgrid")
        with self.session_scope() as s:
            return s.query(FishTankGrid).filter(FishTankGrid.sid == sid, FishTankGrid.sim_turn == sim_turn).one()
