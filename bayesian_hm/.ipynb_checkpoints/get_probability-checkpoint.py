import numpy as np
from scipy.spatial import cKDTree
def get_probability(x,samples):
    net = cKDTree(samples-x.min(axis=0)/(x.max(axis=0)-x.min(axis=0)))
    x=x-x.min(axis=0)/(x.max(axis=0)-x.min(axis=0))
    mindist, _ =net.query(x)
    mindist=np.abs(mindist)
    return mindist/np.sum(mindist)
    