def process_params(samples,k=25,parallel_jobs=50,max_folders=200,basename="output_",ndays=182):
    'k= number of repetitions per combination of parameters'
    'samples=array(row=nsamples,col=nparams)'
    'parallel_jobs = maximum number of parallelized runs'
    'max_folders= maximum number of folder to be created at the same time'
    'basename= name of the folders with the results (an integer will be added)'
    'ndays= number of days to run'
    'params= list of params to keep in the results (e.g. [hosp_inc_0,hosp_inc_1])'
    
    
    if max_folders%k!=0:
        raise ValueError("The maximum number of folders should be a multiple of k (repetitions)")
    
    print("Cleaning folders..."),
    
    print("###################")
    
    #Build k copies of each combination
    alldata=[]
    for i in samples.tolist():
        alldata=alldata+[ele for ele in [i] for _ in range(k)]

    
    if len(alldata)<=max_folders:
        print("The total number of runs is {}".format(len(alldata)))
        print("###################")
        
    else:
        print("The total number of runs is {} . Processing in chunks...".format(len(alldata)))
        print("###################")
    
    #Nested list
    alldata=list(get_chunks(alldata,max_folders))
    
    all_results={}
    
    for j in range(len(alldata)):
        chunk=alldata[j]
        clean_dir(basename=basename)
        print("Processing chunk {}/{}".format(j+1,len(alldata)))
        print("###################")
        #Generate commands
        commands=[]
        for i in range(len(chunk)):
            commands.append(build_command(basename+str(i),chunk[i][0],chunk[i][1],chunk[i][2],chunk[i][3],
                                          chunk[i][4],chunk[i][5],chunk[i][6],chunk[i][7],chunk[i][8],chunk[i][9],
                                          chunk[i][10],chunk[i][11],chunk[i][12],chunk[i][13],
                                          ndays=ndays,seed=i%k))
            #commands.append(build_command(basename+str(i),chunk[i],ndays=ndays,seed=i%k))
        #print(" ".join(commands[0]))
        pull_run(parallel_jobs, commands)
        #Extract results
        z=[get_outputs(basename=x) for x in [basename+str(b) for b in range(len(chunk))]]
        #Add to nested dict-> (params){k{results}}
        i=0
        for h in np.arange(0,len(chunk),k):
            par={}
            for g in range(k):
                par[g]=z[i]
                i+=1
            all_results[(chunk[h][0],chunk[h][1],chunk[h][2],chunk[h][3],
                         chunk[h][4],chunk[h][5],chunk[h][6],chunk[h][7],chunk[h][8],chunk[h][9],
                         chunk[h][10],chunk[h][11],chunk[h][12],chunk[h][13])]=par    
            
        
    return all_results