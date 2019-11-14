import numpy as np
from plato.util import coverage

class EvadeObjective:
    def __init__(self, interval=[-np.inf, np.inf], targets=[]):
        self.obj_type = 'spatiotemporal'
        self.reward = 0
        # who
        self.eoi = targets # entity of interest
        # where
        self.aoi = None # area of interest
        # when
        self.ioi = interval # interval of interest
        # how
        self.criterion = None

    # what (condition)
    def __call__(self, entities, *args, **kwargs):
        self.reward = 0
        self.eoi = kwargs['enemies']

        cells = []
        for ent in self.eoi.values():
            for xy in coverage(ent.xy, ent.properties['visibility']):
                cells.append(xy)

        for xy in [ent.xy for ent in entities.values() if ent.entity_type not in ['drone']]:
            if xy in set(cells): self.reward -= 0.1

        if self.reward / 10 == len([ent for ent in entities.values() if ent.entity_type not in ['drone'] and ent.operational]):
            return True

        return False
