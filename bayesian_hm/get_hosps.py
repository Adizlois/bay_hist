def get_hosps(dois,filename="aldersAntallPerDag.csv",first_date="2021-09-27",w=None):
    #Aggr -> aggregates. List of lists e.g. [[0,1],[2,3,4,5][6,7,8]]
    
        
    real_data=pd.read_csv(os.path.join(realdatadir,filename),sep=";")
    real_data=real_data[sorted(real_data.columns)]
    real_data.columns=["dates"]+list(real_data.columns[1:])
    real_data.dates=pd.to_datetime(real_data.dates)
    real_data.index=real_data.dates
    real_data.drop(["dates"],axis=1,inplace=True)
    if w:
        real_data=real_data.rolling(window=w,center=True).mean().fillna(real_data)
    
    real_data=real_data.loc[[pd.to_datetime(first_date)+datetime.timedelta(days=x) for x in dois]]
    #real_data=[real_data.iloc[:,n].sum(axis=1).astype(np.float32) for n in aggr]
    return [real_data.iloc[:,:].T]