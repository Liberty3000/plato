from plato.entity import Entity

class Drone(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity_type = 'drone'
        self.domain = 'air'
        self.properties = dict(mobility=5, visibility=7, durability=3)
        self.weapons = []
        self.sensors = []
        self.cargo = []

        self.compile()
