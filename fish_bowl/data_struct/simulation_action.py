import enum


class AuditAction(enum.Enum):
    Move = 1
    Eat = 2
    Breed = 3
    Die = 4

class SimulationAction(object):
    """
    Data struct to record actions of the simulation which we can serialise/persist to a datastore
    Use for audit purposes
    """
    start_action_id = 0

    # action like move, eat, breed, die
    def __init__(self, sid, oid):
        self._action_id = SimulationAction.start_action_id
        SimulationAction.start_action_id += 1


class MoveSimulationAction(object):

    def __init__(self, sid, oid, animal_oid, start_coord, target_coord):
        super().__init__(sid, oid)
        self._action_type = AuditAction.Move
        self._animal_oid = animal_oid
        self._start_coord = start_coord
        self._target_coord = target_coord

