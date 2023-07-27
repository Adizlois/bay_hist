def check_emulators(alldata_tra_val,emulators,outputs,output_set,plots_folder=None):
    
    if not os.path.exists(plots_folder):
        os.mkdir(plots_folder)
    rs=[]
    coverages=[]
    
    
    for i in range(len(emulators.emulators)):
        if emulators.emulators[i]!="0":
            try:
                if plots_folder:
                    r,coverage=plot_emulator(emulators,alldata_tra_val[input_names].to_numpy(),
                         alldata_tra_val[outputs[i]].to_numpy().astype(np.float32),nc=i,
                         sds=2,title=outputs[i],filename=os.path.join(plots_folder,"emu_val_"+outputs[i]+".png"))
                else:
                    r,coverage=plot_emulator(emulators,alldata_tra_val[input_names].to_numpy(),
                         alldata_tra_val[outputs[i]].to_numpy().astype(np.float32),nc=i,
                         sds=2,title=outputs[i])
                
                rs.append(r)
                coverages.append(coverage)
            except:
                rs.append(2)
                coverages.append(2)
        else:
            rs.append(-1)
            coverages.append(-1)
    return rs,coverages