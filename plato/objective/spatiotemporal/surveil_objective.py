import numpy as np
from plato.util import coverage

class SurveilObjective:
    def __init__(self, interval=[-np.inf, np.inf], targets=[]):
        self.obj_type = 'spatiotemporal'
        self.reward = 0
        # who
        self.eoi = targets # entity of interest
        # where
        self.aoi = [{'xy':target.xy, 'radius':1} for target in targets] # area of interest
        # when
        self.ioi = interval # interval of interest
        # how
        self.criterion = None

    # what (condition)
    def __call__(self, entities, *args, **kwargs):
        self.reward = 0
        self.eoi = kwargs['enemies']
        self.aoi = [{'xy':ent.xy, 'radius':1} for ent in self.eoi.values()]
        drones = [ent for ent in entities.values() if ent.entity_type == 'drone']
        for xy in [target.xy for target in self.eoi.values()]:
            for drone in drones:
                if xy in coverage(drone.xy, drone.properties['visibility']):
                    self.reward += 1
        return False
