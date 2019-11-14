import numpy as np
from plato.util import coverage

class OccupyObjective:
    def __init__(self, interval=[-np.inf, np.inf], area={'xy':[16,16], 'radius': 4}):
        self.obj_type = 'temporal'
        self.reward = 0
        # who
        self.eoi = None # entity of interest
        # where
        self.aoi = area # area of interest
        # when
        self.ioi = interval # interval of interest
        # how
        self.criterion = None

    # what (condition)
    def __call__(self, entities, timer, *args, **kwargs):
        enemies = kwargs['enemies']
        whites = [ent.xy in coverage(self.aoi['xy'],self.aoi['radius']) for ent in entities.values() if ent.operational]
        blacks = [ent.xy in coverage(self.aoi['xy'],self.aoi['radius']) for ent in enemies.values() if ent.operational]

        self.reward = len(whites) - len(blacks)

        return False
