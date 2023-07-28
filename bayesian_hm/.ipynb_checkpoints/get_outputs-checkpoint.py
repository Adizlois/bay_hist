import pandas as pd
from .get_age_hospitalizations import get_age_hospitalizations
def get_outputs(basename,basedir="../In_out"):
    [hosp1,hosp2,hosp3,hosp4,hosp5,hosp6,hosp7,hosp8,hosp9]=get_age_hospitalizations(basename=basename,basedir=basedir,
                                                                                     aggr=[[x] for x in range(9)])
    
    return pd.concat([get_daily_hospitalizations(basename=basename,basedir=basedir),
                 pd.DataFrame({"hosp1":hosp1,"hosp2":hosp2,"hosp3":hosp3,
                               "hosp4":hosp4,"hosp5":hosp5,"hosp6":hosp6,
                               "hosp7":hosp7,"hosp8":hosp8,"hosp9":hosp9,
                              })],axis=1)
