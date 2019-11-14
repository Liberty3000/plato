import numpy as np
from plato.util import coverage

class CaptureObjective:
    def __init__(self, area={'xy':[16,16], 'radius': 1}, targets=None):
        self.obj_type = 'spatial'
        self.reward = 0
        # who
        self.eoi = targets # entity of interest
        # where
        self.aoi = area # area of interest
        # when
        self.ioi = [-np.inf, np.inf] # interval of interest
        # how
        self.criterion = None

    # what (condition)
    def __call__(self, entities, *args, **kwargs):
        if any([ent.xy in coverage(self.aoi['xy'],self.aoi['radius']) for ent in entities.values()]):
            self.reward += 1
            return True
        return False
