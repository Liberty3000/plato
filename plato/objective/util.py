import numpy as np, matplotlib.pyplot as mp
from matplotlib.patches import Circle

def plot_objectives(objectives, canvas, ax, timer=None):
    patches = []

    for obj in objectives:
        alpha = 2e-1
        color = 'yellow'

        # the colors and alpha values can change if the objective is temporal or spatiotemporal
        if obj.obj_type in ['temporal','spatiotemporal']:
            beg,end = obj.ioi[0],obj.ioi[1]
            obj_frames = end - beg
            if timer < beg:
                color = 'white' # pre-activation
            if timer >= beg and timer <= end:
                alpha = np.linspace(0.15,7e-1, obj_frames)[(timer - beg)-1]
            if timer > end:
                color = 'gray'  # post-activation

        for obj in objectives:
            x,y = obj.aoi['xy']
            pixel = [235, 200, 50]
            circle= Circle((y,x), radius=obj.aoi['radius'], alpha=alpha, color=color)
            patch = ax.add_patch(circle)
            patches.append(patch)

            canvas[x,y,:] = pixel

    return canvas, ax, patches
