import pandas as pd
import datetime
import os
import config
def get_omi(dois,filename="antall_per_dag_hele_landet_omikron_med_missing.csv",first_date="2021-09-27",
            w=None,cumulative=False):
    realdatadir=config.realdatadir
    real_data=pd.read_csv(os.path.join(realdatadir,filename),sep=";")
    real_data=real_data[sorted(real_data.columns)]
    real_data.columns=["dates"]+list(real_data.columns[1:])
    real_data.dates=pd.to_datetime(real_data.dates)
    real_data.index=[x.days for x in real_data.dates-pd.to_datetime(first_date)]
    real_data.drop(["dates","antall.innlagte"],axis=1,inplace=True)
    if w:
        real_data.iloc[:,0]=real_data.iloc[:,0].rolling(window=7,center=True).mean()
    
    if cumulative:
        real_data.iloc[:,0]=real_data.iloc[:,0].cumsum()
    return real_data.loc[dois].values
