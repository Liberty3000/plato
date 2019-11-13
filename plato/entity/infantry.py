from plato.entity import Entity

class Infantry(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity_type = 'infantry'
        self.domain = 'land'
        self.properties = dict(mobility=2, visibility=2, durability=3)
        self.weapons = [dict(weapon_range=3,
                             weapon_radius=1,
                             weapon_accuracy=0.9,
                             weapon_power=1,
                             ammo=64)]
        self.sensors = []
        self.cargo = {}

        self.compile()
