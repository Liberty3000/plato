import random, numpy as np
from plato.util import coverage

default_actions = [
'move_N',
'move_S',
'move_E',
'move_W',
'move_NE',
'move_NW',
'move_SE',
'move_SW'
]

directional_actions = {
'move_N': np.asarray([ 0, 1]),
'move_S': np.asarray([ 0,-1]),
'move_E': np.asarray([ 1, 0]),
'move_W': np.asarray([-1, 0]),
'move_NE':np.asarray([ 1, 1]),
'move_NW':np.asarray([-1, 1]),
'move_SE':np.asarray([ 1,-1]),
'move_SW':np.asarray([-1,-1]),
}

def attack(entity, action, damage_map, verbose=False):
    idx = entity.attack_actions.index(action)

    weapon_model = entity.weapons[0]
    cells = coverage(entity.xy, weapon_model['weapon_range'], damage_map.shape)

    try:
        if len(cells) < action:
            ij = random.choice(cells)
        else:
            ij = cells[action]

            for (x,y) in coverage(ij, weapon_model['weapon_radius'], damage_map.shape):
                if verbose: print('before', damage_map[x,y])
                if weapon_model['weapon_accuracy'] < np.random.random():
                    damage_map[x,y] += weapon_model['weapon_power']
    except: pass

    return damage_map

def patrol(entity, action, terrain, verbose=False):
    idx = entity.patrol_actions.index(action)
    cells = coverage(entity.xy, entity.properties['mobility'], terrain[0].shape)

    try:
        cell = cells[idx]
    except:
        cell = entity.xy if not len(cells) else cells[0]

    return cell
