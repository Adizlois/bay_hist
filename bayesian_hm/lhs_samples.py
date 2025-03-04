from smt.sampling_methods import LHS
import numpy as np
def lhs_samples(num,ranges=np.array([[1.7,3.2],[1.1,2.7],[0.05,1.8],[0.5,1.],[1,61],
                                     [0.05,0.5],[0.1,0.7],[0.3,0.9],[0.3,0.9],[0.3,0.9],[0.3,0.9],
                                    [0.5,1],[0.5,1],[0.5,1],[0.1,1.0]])):
    sampling = LHS(xlimits=ranges)
    samp=sampling(num)
    samp[:,4]=np.floor(samp[:,4])
    return samp


