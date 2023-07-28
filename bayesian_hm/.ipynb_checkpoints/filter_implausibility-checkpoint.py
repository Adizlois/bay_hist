from multiprocessing import Pool
import numpy as np
from .calc_implausibility import calc_implausibility

def filter_implausibility(x,emu_object_mean,vs,real_value,vo,vm,imp_threshold,emu_mask,nproces=None):
    #x= set of points to be filtered using the implausibility (array)
    #emu_object = object from "emulators" class
    #real_value = set of real values at the Day Of Interests
    #vs = list of stochastic noise to be applied at each DOI
    #vo = Observational error
    #vm = model error
    
    for i in range(len(emu_object_mean.emulators)):
        print("Output %d"%i)
                
        if emu_mask[i]:
            
            chunk_size = len(x) // nproces
            chunks = [(x[j:j+chunk_size],i) for j in range(0, len(x), chunk_size)]
            
            with Pool(processes=nproces) as pool:
                predictions_mean = pool.starmap(emu_object_mean.predict, chunks)
            
            
            
            imp=calc_implausibility(real_value=real_value[i],
                                    model_value=np.concatenate([z["mean"] for z in predictions_mean],axis=0),
                                    vo=vo[i],
                                    vc=np.concatenate([z["unc"] for z in predictions_mean],axis=0),
                                    vs=vs[i],
                                    vm=vm,
                                    multidim=False)
            x=x[imp<imp_threshold,:]
            #vs=vs[:,imp<imp_threshold]
            print("X output size: %d"%x.shape[0])
    
    return x
    