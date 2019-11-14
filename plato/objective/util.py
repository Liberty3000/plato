import numpy as np, matplotlib.pyplot as mp
from matplotlib.patches import Circle
from plato.features import global_features
from plato.util import coverage

def plot_objectives(objectives, timer, canvas, ax):
    patches = []
    for obj in objectives:
        pixel,color,alpha = [235, 200, 50],'yellow',2e-1
        # the colors and alpha values can change if the objective is temporal or spatiotemporal
        if obj.obj_type in ['temporal','spatiotemporal'] and not any(np.isinf(obj.ioi)):
            beg,end = obj.ioi[0],obj.ioi[1]
            obj_frames = end - beg
            if timer < beg:
                color = 'white' # pre-activation
            if timer >= beg and timer <= end:
                alpha = np.linspace(0.15,7e-1, obj_frames)[(timer - beg)-1]
            if timer > end:
                color = 'gray'  # post-activation

        if isinstance(obj.aoi, list):
            for aoi in obj.aoi:
                x,y = aoi['xy']
                circle= Circle((y,x), radius=aoi['radius'], alpha=alpha, color=color)
                patch = ax.add_patch(circle)
                patches.append(patch)
                canvas[x,y,:] = pixel
        if not isinstance(obj.aoi, list) and obj.aoi:
            x,y = obj.aoi['xy']
            circle= Circle((y,x), radius=obj.aoi['radius'], alpha=alpha, color=color)
            patch = ax.add_patch(circle)
            patches.append(patch)
            canvas[x,y,:] = pixel

    return canvas, ax, patches

def filter_objectives(objectives):
    xys = []
    for obj in objectives:
        # if a single objective has multiple areas of interest
        if isinstance(obj.aoi, list):
            for aoi in obj.aoi:
                for xy in coverage(aoi['xy'], aoi['radius'], shape): xys += [xy]
        else:
            xys += [xy for xy in coverage(obj.aoi['xy'], obj.aoi['radius'], shape)]
    return xys

def encode_objectives(objectives, minimap, detections, shape):
    xys = {}
    for obj in objectives:
        # if a single objective has multiple areas of interest
        if isinstance(obj.aoi, list):
            for aoi in obj.aoi:
                for (x,y) in coverage(aoi['xy'], aoi['radius'], shape):
                    xys[(x,y)] = obj.obj_type
        if not isinstance(obj.aoi, list) and obj.aoi:
            xys = {(x,y):obj.obj_type for (x,y) in coverage(obj.aoi['xy'], obj.aoi['radius'], shape)}

        # only encode an aoi if it is not attached to an eoi that we have not detected
        if obj.eoi:
            for xy,obj_type in xys.items():
                if xy in [ent.xy for ent in detections]:
                    xys[xy] = obj_type

        for ((x,y),obj_type) in xys.items():
            minimap[global_features.index('{}_area_of_interest'.format(obj_type)),x,y] += 1

    return minimap
