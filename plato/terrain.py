import numpy as np
from plato.router import pathfinder

def lerp(a,b,x):
    return a + x * (b-a)

def fade(t):
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h % 4]
    return g[:,:,0] * x + g[:,:,1] * y

def perlin(gridx, gridy, extent=0.75, seed=0):
    np.random.seed(seed)

    xlin = np.linspace(0, extent, gridx, endpoint=False)
    ylin = np.linspace(0, extent, gridy, endpoint=False)

    x,y = np.meshgrid(xlin,ylin)

    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()

    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)

    x1 = lerp(n00,n10,u)
    x2 = lerp(n01,n11,u)
    return abs(lerp(x1,x2,v))

def default_terrain_model(*args, **kwargs):
    return perlin(*args, **kwargs)
