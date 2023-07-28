import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
def plot_emulator(emulator_object,val_inputs,val_output,nc,title=None,sds=2,filename=None):
    predictions_map=emulator_object.predict(newinputs=val_inputs,nc=nc)
    yerr=sds*np.sqrt(predictions_map["unc"])
    plt.errorbar(val_output,predictions_map["mean"], yerr=yerr, fmt='.k')
    if title:
        plt.title(title)
    if filename:
        plt.savefig(filename)
    plt.close()
    slope, intercept, r_value, p_value, std_err = stats.linregress(val_output,predictions_map["mean"])
    #print("R² %.3f"%np.round(r_value**2,3))
    coverage=(val_output<=predictions_map["mean"]+yerr)&(val_output>=predictions_map["mean"]-yerr)
    #print("Coverage %.3f"%np.round(np.sum(coverage)/len(coverage),3))

    
    return(np.round(r_value**2,3),np.round(np.sum(coverage)/len(coverage),3))