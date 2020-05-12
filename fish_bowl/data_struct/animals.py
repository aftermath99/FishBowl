from fish_bowl.process.utils import Animal


class Fish(object):

    start_oid = 1000

    def __init__(self, sim_id, spawn_turn):
        self.oid = Fish.start_oid
        Fish.start_oid += 1
        self.sim_id = sim_id
        self.spawn_turn = spawn_turn
        self.animal_type = Animal.Fish
        self.breed_count = 0
        self.last_breed = 0
        self.alive = True

    def __repr__(self):
        return "{}".format(self.oid)


class Shark(Fish):
    start_oid = 2000

    def __init__(self, sim_id, spawn_turn):
        super().__init__(sim_id, spawn_turn)
        self.oid = Shark.start_oid
        Shark.start_oid += 1
        self.animal_type = Animal.Shark
        # turn of last fed same as spawn at construction
        self.last_fed = spawn_turn

    # oid =
    # sim_id =
    # animal_type =
    # spawn_turn =
    # breed_count =
    # last_breed =
    # last_fed =
    # alive =
    # coord_x =
    # coord_y =