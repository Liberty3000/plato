import numpy as np

class EngageObjective:
    def __init__(self, interval=[-np.inf, np.inf], targets=[], radius=3):
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

        if kwargs['timer'] >= self.ioi[0] and kwargs['timer'] <= self.ioi[1]:
            for ent in self.eoi.values():
                if not ent.operational: self.reward += 1
        if self.reward == len(self.eoi): return True
        return False
