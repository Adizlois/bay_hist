import os
import pandas as pd
import config


def get_age_hospitalizations(basename,basedir="../In_out",aggr=[[0,1],[2,3,4,5],[6,7,8]]):
    agegroups=config.agegroups
    #hospitalizations by age
    res=pd.read_table(os.path.join(basedir,basename,"national_cases.txt"))
    res=res[["cum_H_"+str(i) for i in range(101)]]
    res=res.diff().fillna(res[["cum_H_"+str(i) for i in range(101)]])
    for i in range(len(agegroups)):
        agegroup=agegroups[i]
        if i==len(agegroups)-1:
            res["cum_H_"+str(agegroup)]=res.iloc[:,i*10:101].sum(axis=1).values
        else:
            res["cum_H_"+str(agegroup)]=res.iloc[:,i*10:i*10+10].sum(axis=1).values

    res=res[["cum_H_"+str(agegroup) for agegroup in agegroups]]
    #res=res.cumsum(axis=0)#.div(res.cumsum(axis=0).sum(axis=1),axis=0)
    
    return [res.iloc[:,n].sum(axis=1).values for n in aggr]