import numpy as np
from .get_hosps import get_hosps
from .get_omi import get_omi
def get_real_data(dois,w=None,byage=False,omi=False):
    real_data=get_hosps(dois,w=w)
    #real_data=get_hosps(dois,aggr=[[x] for x in range(10)],w=w)
    
    if omi:
        return(np.ravel(get_omi(dois,w=w)))      
                  
    elif byage:
        return np.ravel(real_data)
    else:
        return np.ravel((real_data[0]).sum(axis=0))