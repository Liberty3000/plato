
class Objective:
    def __init__(self, *args, **kwargs):
        self.obj_type = None
        # who
        self.eoi = None # entity of interest
        # where
        self.aoi = [] # area of interest
        # when
        self.ioi = [] # interval of interest

    # what (condition)
    def __bool__(self, *args, **kwargs):
        return True
