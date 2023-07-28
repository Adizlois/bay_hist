import pandas as pd
import numpy as np
def extract_days(data_dict,dois,input_names,params):
    alldata = pd.DataFrame(list(data_dict.keys()), columns =input_names)
    new_cols=[[x+"_mu-"+str(doi) for x in params]+[x+"_var-"+str(doi) for x in params] for doi in dois]
    new_cols=[item for doi in new_cols for item in doi]
    new_cols=pd.DataFrame({},columns=new_cols)
    for h in range(len(dois)):
        doi=dois[h]
        for i in range(len(data_dict)):
            outputs=pd.DataFrame()
            for v in data_dict[list(data_dict.keys())[i]].values():
                #outputs=pd.concat([outputs,v.loc[[doi]]], ignore_index=True)
                outputs=pd.concat((outputs,v.loc[[doi],params]), axis=0)
            new_cols.loc[i,[x+"_mu-"+str(doi) for x in params]]=np.round(outputs.mean(axis=0).values,3)
            new_cols.loc[i,[x+"_var-"+str(doi) for x in params]]=np.round(np.var(outputs,axis=0).values,3)
    alldata=pd.concat((alldata,new_cols),axis=1)    
    return alldata