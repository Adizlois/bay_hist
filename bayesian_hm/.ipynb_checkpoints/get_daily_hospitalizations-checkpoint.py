import pandas as pd
import os
def get_daily_hospitalizations(basename,basedir="../In_out"):
    #hospitalizations by age
    res=pd.read_table(os.path.join(basedir,basename,"national_cases.txt"))
    res=res[["cum_H","cum_H_omicron","cum_H_delta"]]
    res=res.diff().fillna(res[["cum_H","cum_H_omicron","cum_H_delta"]])
    res.columns=["hosps","omicron","delta"]
    res["cum_omi"]=res["omicron"].cumsum()
    return res