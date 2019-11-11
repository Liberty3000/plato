import numpy as np
from plato.util import coverage

class ControlObjective:
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
        self.criterion = 10

    # what (condition)
    def __call__(self, entities, timer, *args, **kwargs):
        if any([ent.xy in coverage(self.aoi['xy'],self.aoi['radius']) for ent in entities.values()]):
            self.reward = 1
        else:
            self.reward = 0

        if self.reward > self.criterion: return True
        else: return False
