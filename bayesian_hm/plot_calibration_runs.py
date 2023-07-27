def plot_calibration_runs(allres,real_data,dois_to_include,filename,input_names,ndays=200):
    alldata_tra=extract_days(allres,np.arange(ndays).tolist(),input_names,["hosps"])
    fig,ax=plt.subplots()
    mus=[x for x in alldata_tra.columns if "_mu-" in x]
    alldata_tra[mus].T.plot(legend=False,ax=ax,alpha=0.4,title="Wave"+str(wave))
    ax.plot(mus,real_data,lw=2,c="blue")
    for xc in dois_to_include:
        ax.axvline(x=xc,linestyle="dotted",linewidth=2)
    labels = [item.get_text().split("-")[1] if item.get_text()!="" else "" for item in ax.get_xticklabels()]
    ax.set_xticklabels(labels)
    plt.savefig(filename)
    plt.show()