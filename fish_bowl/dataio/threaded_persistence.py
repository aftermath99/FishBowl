import logging
import os

from fish_bowl.dataio.database import SQLAlchemyQueries

from sqlalchemy import Column, DateTime, Float, ForeignKey, Enum, Boolean, Integer, String
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


class PersistenceClient(SQLAlchemyQueries):
    """
    The PersistenceClient offloads the persistence to storage (eg. Database)
    from the SimulationEngine
    It should use a queue and separate thread to run inserts and also use bulk inserts per simulation
    Note: SQLLite is not designed for performance
    """
    def __init__(self, database_url):
        super().__init__(database_url=database_url, declarative_base=Base, expire_on_commit=False)

    def save_tankgrid(self, sid, sim_turn, grid_str):
        _logger.debug("save_tankgrid")
        tank_grid = FishTankGrid(sid=sid, sim_turn=sim_turn, grid=grid_str)
        with self.session_scope() as s:
            s.add(tank_grid)
            s.flush()

    def get_tankgrid(self, sid: int, sim_turn: int) -> FishTankGrid:
        _logger.debug("get_tankgrid")
        with self.session_scope() as s:
            return s.query(FishTankGrid).filter(FishTankGrid.sid == sid, FishTankGrid.sim_turn == sim_turn).one()
