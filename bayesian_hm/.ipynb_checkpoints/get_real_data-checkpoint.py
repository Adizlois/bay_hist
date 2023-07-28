import numpy as np
from .get_hosps import get_hosps
def get_real_data(dois,w=None,byage=False):
    real_data=get_hosps(dois,w=w)
    #real_data=get_hosps(dois,aggr=[[x] for x in range(10)],w=w)
    if byage:
        return np.ravel(real_data)
    else:
        return np.ravel((real_data[0]).sum(axis=0))