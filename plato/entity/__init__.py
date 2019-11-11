import random, numpy as np
from plato.util import coverage
from plato.actions import default_actions

waypoint = [245,150,235]
legend = {
('blacks','infantry'):[255,0,0],
('blacks','vehicle'):[255,140,0],
('blacks','drone'):[255,0,255],
('whites','infantry'):[0,0,255],
('whites','vehicle'):[0,128,255],
('whites','drone'):[128,128,255],
}

class Entity:
    def __init__(self, id='unknown', affiliation='white', xy=np.asarray([0,0]), route=[]):
        self.id, self.affiliation, self.xy = id, affiliation, xy
        self.operational = True
        self.properties = {}
        self.weapons = []
        self.sensors = []
        self.cargo = []

    def random_action(self):
        return np.random.randint(self.n_actions)

    def compile(self):
        # note: for now, only weapons define the entity's action space
        # note: for now, assets that a given entity can hold a single weapon
        self.action_space = []
        self.attack_action_space  = []
        self.patrol_action_space  = []
        self.attack_actions = []
        self.patrol_actions = []

        if len(self.weapons):
            # attack action map, constrained by the entity's weapon(s)
            attack_cells = coverage((10,10), self.weapons[0]['weapon_range'])
            self.attack_action_space = ['attack_{}x{}'.format(x,y) for (x,y) in attack_cells]
            self.attack_actions = list(range(0, len(attack_cells)))

        # patrol action map, constrained by the entity's properties
        patrol_cells = coverage((10,10), self.properties['mobility'])
        self.patrol_action_space = ['patrol_{}x{}'.format(x,y) for (x,y) in patrol_cells]
        self.patrol_actions = list(range(len(self.attack_actions), len(self.attack_actions) + len(patrol_cells)))

        self.action_space = self.attack_action_space + self.patrol_action_space
        self.n_actions = len(self.action_space)


callsigns = [
'ACORN',
'AMERICA',
'ANAHEIM',
'ATLANTA',
'AURORA',
'BERLIN',
'BISBEE',
'BOUGANSVILLE',
'BRAVO',
'BUFFALO',
'BUNKERHILL',
'CAIRO',
'CALEXICO',
'CHARLIE',
'CHICAGO',
'CHICKASAW',
'COLORADO',
'DENVER',
'ECHO',
'EUREKA',
'FLAGSTAFF',
'FOXTROT',
'GADSDEN',
'GIFFORDS',
'GONZALEZ',
'GUNSTONHALL',
'HIGGINS',
'HOLDFAST',
'HOLLYWOOD',
'HONOLULU',
'HOPE',
'HURRICANE',
'HYANNIS',
'INDEPENDENCE',
'INDIA',
'IPSWICH',
'LAGUNA',
'LEYTEGULF',
'LIMA',
'LITTLEROCK',
'LONDON',
'MAHAN',
'MARYLAND',
'MILWAUKEE',
'MONSOON',
'MONTANA',
'NEEDLES',
'NEWYORK',
'NOVEMBER',
'OCEANCITY',
'PHOENIX',
'PRESCOTT',
'QUEBEC',
'ROMEO',
'SEAGULL',
'SEARCY',
'SHELLDRAKE',
'SIERRA',
'SIOUXCITY',
'SPALDING',
'STOCKDALE',
'STILLWATER',
'STUTTGART',
'TEMPEST',
'THESULLIVANS',
'TOKYO',
'TOMBSTONE',
'TYPHOON',
'URBANA'
'WATERLOO',
'WHISKEY',
'WICHITA',
'WINSLOW',
'WYOMING',
'YANKEE',
'ZERO',
'ZUMWALT']
