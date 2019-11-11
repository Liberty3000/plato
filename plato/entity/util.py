import random, numpy as np
import matplotlib.pyplot as mp
from matplotlib.patches import Circle
from plato.entity.drone import Drone
from plato.entity.infantry import Infantry
from plato.entity.vehicle import Vehicle
from plato.entity import callsigns, legend
from plato.util import quantize_area

def randomize_entities(n_infantry, n_vehicle, n_drone, init_area, affiliation):
    entities = {}
    n = int(n_infantry + n_vehicle + n_drone)
    if affiliation == 'blacks':
        ids = ['unknown_{}'.format(i) for i in range(n)]
    if affiliation == 'whites':
        ids = list(np.random.choice(callsigns, size=n, replace=False))

    x = np.random.randint(*init_area[0], size=n)
    y = np.random.randint(*init_area[1], size=n)
    xy = list(zip(x,y))
    s = random.choice(xy)

    for _ in range(n_infantry):
        id_= ids.pop(0)
        entity = Infantry(id=id_, xy=xy.pop(0), affiliation=affiliation)
        entities[id_] = entity
    for _ in range(n_vehicle):
        id_= ids.pop(0)
        entity = Vehicle(id=id_, xy=xy.pop(0), affiliation=affiliation)
        entities[id_] = entity
    for _ in range(n_drone):
        id_= ids.pop(0)
        entity = Drone(id=id_, xy=xy.pop(0), affiliation=affiliation)
        entities[id_] = entity
    return entities

def place_entities(entities, affiliation):
    entity_types = {'infantry':Infantry, 'vehicle':Vehicle, 'drone':Drone}
    entities = []
    for ent in entities:
        entities.append(entity_types[ent['type']](xy=np.asarray(ent['xy']), affiliation=affiliation))
    return entities

def plot_entities(entities, canvas, ax, routes=False):
    if ax is None: fig,ax = mp.subplots(figsize=(10,10))

    patches = []

    for id,ent in entities.items():
        x,y = ent.xy

        pixel = legend[(ent.affiliation, ent.entity_type)]

        sensor_color = 'skyblue' if ent.affiliation == 'whites' else 'lightpink'
        weapon_color ='lavender' if ent.affiliation == 'whites' else 'lavenderblush'
        vision_color = 'green' if ent.affiliation == 'whites' else 'brown'

        vision_radius = Circle((y,x), radius=ent.properties['visibility'], alpha=0.15, color=vision_color)
        patch = ax.add_patch(vision_radius)
        patches.append(patch)

        for weapon in ent.weapons:
            weapon_radius = Circle((y,x), radius=weapon['weapon_range'], alpha=0.15, color=weapon_color)
            patch = ax.add_patch(weapon_radius)
            patches.append(patch)
        for sensor in ent.sensors:
            sensor_radius = Circle((y,x), radius=sensor['sensor_range'], alpha=0.15, color=sensor_color)
            patch = ax.add_patch(sensor_radius)
            patches.append(patch)

        canvas[x,y,:] = pixel
        if routes:
            for waypoint in ent.route:
                x,y = waypoint
                canvas[waypoint[0],waypoint[1],:] = [245,150,235]

    return canvas, ax, patches
