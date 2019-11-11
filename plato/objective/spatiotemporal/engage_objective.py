import numpy as np

class EngageObjective:
    def __init__(self, interval=[-np.inf, np.inf], target=None, radius=3):
        self.obj_type = 'spatiotemporal'
        self.reward = 0
        # who
        self.eoi = target # entity of interest
        # where
        self.aoi = {'xy':target.xy, 'radius':radius} # area of interest
        # when
        self.ioi = interval # interval of interest
        # how
        self.criterion = None

    # what (condition)
    def __call__(self, *args, **kwargs):
        if not self.eoi.operational and \
        kwargs['timer'] > self.ioi[0] and kwargs['timer'] <= self.ioi[1]:
            self.reward = 10
            return True
        else:
            self.reward = 0
            return False
