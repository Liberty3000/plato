import random, numpy as np, matplotlib.pyplot as mp
from matplotlib.patches import Circle

def in_range(entity, xy, radius, shape):
    return entity.xy in coverage(xy, radius, shape)

def coverage(xy, radius, shape=(100,100)):
    neighborhood = []
    X = int(radius)
    for i in range(-X, X + 1):
        Y = int(pow(radius * radius - i * i, 1/2))
        for j in range(-Y, Y + 1):
            xcell = np.clip((xy[0] + i), 0, shape[0]-1)
            ycell = np.clip((xy[1] + j), 0, shape[1]-1)
            neighborhood.append((xcell,ycell))
    return list(set(neighborhood))

def centroid(entities):
    x = [ent.xy[0] for ent in entities if ent.operational]
    y = [ent.xy[1] for ent in entities if ent.operational]
    return (int(sum(x) / len(entities)), int(sum(y) / len(entities)))

def quantize_area(region, shape):
    return {
    'W': [[0,shape[0]//2],[0,shape[1]//2]],

    'E': [[0,shape[0]],[shape[1]//2,shape[1]]],

    'S': [[shape[0]//2,shape[0]],[0,shape[1]]],

    'N': [[0,shape[0]//2],[0,shape[1]]],

    'NE':[[shape[0]//2,shape[0]],[0,shape[1]]],

    'SW':[[0,shape[0]//2],[shape[1]//2,shape[1]]],

    'SE':[[shape[0]//2,shape[0]],[shape[1]//2,shape[1]]],

    'NW':[[0,shape[0]//2],[0,shape[1]//2]],

    'random':[[0,shape[0]],[0,shape[1]]],
    }[region]
