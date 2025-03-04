import numpy as np
def perturb_x(x,desired_samples=12000000,perturb_sd=0.20,int_index=4):
    if x.shape[0]>=desired_samples:
        perturb=np.random.normal(scale=perturb_sd, size=(x.shape[0],x.shape[1])).astype(np.float32)
        perturb[:,int_index]=np.round(perturb[:,int_index],0)
        return x+perturb
    else:
        exp_coef=np.ceil(desired_samples/x.shape[0]).astype(int)
        perturb=np.random.normal(scale=perturb_sd, size=(exp_coef,x.shape[0],x.shape[1])).astype(np.float32)
        perturb[:,:,int_index]=np.round(perturb[:,:,int_index],0)
        x2=np.array([perturb[i,:,:]+x for i in range(exp_coef)])
        x2=x2.reshape(-1, x2.shape[-1])
        return x2[np.random.choice(np.arange(x2.shape[0]),size=desired_samples),:]