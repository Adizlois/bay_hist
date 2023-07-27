def filter_dict(allres,k,ndays=200):
    non_valid=[]
    for ke in list(allres.keys()):
        for j in range(k):
            try:
                if allres[ke][j].loc[ndays-1]:
                    pass
            except:
                non_valid.append(ke)
    return list(set(non_valid))