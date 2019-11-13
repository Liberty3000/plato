from plato.entity import Entity

class Vehicle(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity_type = 'vehicle'
        self.domain = 'land'
        self.properties = dict(mobility=5, visibility=4, durability=5)
        self.weapons = [dict(weapon_range=3,
                             weapon_radius=1,
                             weapon_accuracy=0.8,
                             weapon_power=3,
                             ammo=64)]
        self.sensors = []
        self.cargo = [{'ammo':2**7,'fuel':2**14}]

        self.compile()
