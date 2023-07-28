import numpy as np
def calc_implausibility(real_value,model_value,vo,vc,vs,vm=0.1,multidim=False):
    if multidim:
        return np.dot(np.dot((real_value-model_value),np.linalg.inv(np.diag(np.ravel(vo))+np.diag(vc)+
                                                                 np.diag(vs)+np.diag(real_value.shape[0]*[vm]))),(real_value-model_value).T)
    else:
        return np.abs(real_value-model_value)/np.sqrt((vo+vc+vs+vm).astype(np.float32))