##
from bayesian_hm import *
import time
import config
import numpy as np
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22,'figure.figsize':(20,12)})
##


## REFERENCE FOLDERS 

#MODEL 
abm_dir="./1-main-ABM/src/"
#REALDATA
realdatadir="./0-pre-processing/hospital_data/"

#Make the variables available 
config.inout="./1-main-ABM/In_out"
config.abm_dir=abm_dir
config.realdatadir=realdatadir
config.agegroups=np.arange(0,90,10)

#CHANGE WORKING DIRECTORY
os.chdir(abm_dir)
#OUTPUT FOLDER
waves_folder=config.inout+"/waves/"

first_date="2021-09-27"
ndays=200 #From Sep 28th

# INPUT VARIABLES
input_names=["b","new_beta","om_inc","trans_rate","om_seed","sus1","sus2","sus3",
            "sus4","sus5","sus6",
            "sus7","sus8","sus9","fihr"]

# NUMBER OF SAMPLES TO BE USED PER WAVE
nsamples=[len(input_names)*15]+4*[len(input_names)*20]+4*[len(input_names)*30]+3*[len(input_names)*40]+[len(input_names)*50]+[len(input_names)*60]+[len(input_names)*70]


# Total number of waves
nwaves=15

# Number of validation runs
nval=20
# Number of repetitions per sample
k=3



start=time.time()


## TO BE USED ONLY IN CASE WE ARE RESUMING A PREVIOUS CALIBRATION AT A CERTAIN WAVE:
initial_wave=1
load_x=False
reuse_runs=False
reuse_vals=False
reuse_emu=False
##


#DOIS
dois_omi_cal=[90,110,130,150]
dois_hosps_cal=[25,35,50,60,75,90,110,130,150,170,194]


#Select active variables per DOI
output_set_cal=9*[
    [0,5,6,7,8,9,10,11,12,13,14],
    [0,4,5,6,7,8,9,10,11,12,13,14],
    [0,1,4,5,6,7,8,9,10,11,12,13,14],
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    #OMICAL
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    
]

#params=["H"+str(i) for i in agegroups]
params0=["hosp1"]
params1=["hosp2"]
#
params2=["hosp3"]
params3=["hosp4"]
params4=["hosp5"]
params5=["hosp6"]
params6=["hosp7"]
params7=["hosp8"]
params8=["hosp9"]
params9=["omicron"]

wave=initial_wave
parallel_jobs=120#Max number of workers to run ABM
parallel_jobs_emulators=120 #Number of parallel jobs to calibrate the emulators
max_folders=900 #Just in case there is some kind of error in the parametrization

if load_x:
    x=np.load(waves_folder+"wave"+str(initial_wave)+"/wave_"+str(initial_wave)+"_x.npy",allow_pickle='TRUE').item()["x"]

else:
    x=lhs_samples(10000000)

p_below=0.0

#standard deviation of the perturbation to be applied during the exploration step
sds=[0.2,0.15,0.15,0.1,0.1,0.07,0.07,0.05,0.05,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04,0.04]

#Implausibility thresholds to be applied at each wave
imp_thresholds=[4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]


while(wave <= nwaves):
    plots_folder=waves_folder+"wave"+str(wave)+"/plots"
    x=x.astype(np.float32)
    dois_hosps=dois_hosps_cal
    dois_omi=dois_omi_cal
    output_set=output_set_cal
    
    #Create folder for the results if doesn't exist
    
    if not os.path.exists(waves_folder+"wave"+str(wave)):
        os.mkdir(waves_folder+"wave"+str(wave))
    if not os.path.exists(plots_folder):
        os.mkdir(plots_folder)
    #Make the runs
    print("#######")
    print("#######")
    print("WAVE "+str(wave))
    print("#######")
    print("#######")

   
    end0=time.time()
    if (not reuse_runs):
        print("Sampling... ",)
        if wave==1:
            samples=lhs_samples(nsamples[wave-1])

        else:
            samples=disc_samples(nsamples[wave-1],x,unif=False)

    print("Done")
    end1=time.time()
    print("Time %.2f"%(end1-end0))
    if wave>1:
        print("Applying perturbation...",)
        x=perturb_x(x,perturb_sd=sds[wave-1])    
        x=x[(x[:,1]>0),:]
        x=x[(x[:,0]>0),:]
        x=x[(x[:,2]>0),:]
        x=x[(x[:,3]>0),:]
        #x=x[(x[:,3]<1),:]
        x=x[(x[:,5]>0),:]
        x=x[(x[:,6]>0),:]
        x=x[(x[:,7]>0),:]
        x=x[(x[:,8]>0),:]
        x=x[(x[:,9]>0),:]
        x=x[(x[:,10]>0),:]
        x=x[(x[:,11]>0),:]
        x=x[(x[:,12]>0),:]
        x=x[(x[:,13]>0),:]
        x=x[(x[:,14]>0.05),:]
        
        x=x[(x[:,4]<=60),:]
        x=x[(x[:,4]>=1),:]
        
        x=x[(x[:,5]<=1),:]
        x=x[(x[:,6]<=1),:]
        x=x[(x[:,7]<=1),:]
        x=x[(x[:,8]<=1),:]
        x=x[(x[:,9]<=1),:]
        x=x[(x[:,10]<=1),:]
        x=x[(x[:,11]<=1),:]
        x=x[(x[:,12]<=1),:]
        x=x[(x[:,13]<=1),:]
        x=x[(x[:,14]<1.1),:]
        print("Done")
    
    
    # SAVE THE SAMPLES
    wave_res={}          
    wave_res["x"]=x
    np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_x.npy", wave_res)
    print("#######")
    
    #if len([x for x in imp_modes if x in ["multi","uni"]])!=len(imp_modes):
    #    raise ValueError("Please choose between multi (dimensional) or uni (dimensional) implausibility")
    
    end2=time.time()

    if reuse_runs:
        print("Loading previous runs...",)
        prev=np.load(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_runs.npy",allow_pickle='TRUE').item()
        allres=prev["runs"]
        #alldata_tra=prev["alldata_tra"]
        #alldata_tra=load_all_tra(fromwave=5,towave=7)
        
    else:
        print("Making calibration runs...",)

        allres=process_params(samples,k=k,parallel_jobs=parallel_jobs,max_folders=max_folders,basename="output",ndays=ndays)

        non_valid=filter_dict(allres,k)
        if len(non_valid)>0:
            for a in non_valid:
                del allres[a]
        
        wave_res={}
        wave_res["runs"]=allres
        np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_runs.npy", wave_res)
        try:
            plot_calibration_runs(allres,real_data=get_real_data(np.arange(200).tolist(),w=None,byage=False),dois_to_include=dois_hosps,filename=plots_folder+"/calibration_runs.png",ndays=200,wave=wave,input_names=input_names)
        except:
            print("Error in the plotting function")
    

    
    alldata_tra_hosp1=extract_days(allres,dois_hosps,input_names,params0)
    alldata_tra_hosp2=extract_days(allres,dois_hosps,input_names,params1)
    alldata_tra_hosp3=extract_days(allres,dois_hosps,input_names,params2)
    alldata_tra_hosp4=extract_days(allres,dois_hosps,input_names,params3)
    alldata_tra_hosp5=extract_days(allres,dois_hosps,input_names,params4)
    alldata_tra_hosp6=extract_days(allres,dois_hosps,input_names,params5)
    alldata_tra_hosp7=extract_days(allres,dois_hosps,input_names,params6)
    alldata_tra_hosp8=extract_days(allres,dois_hosps,input_names,params7)
    alldata_tra_hosp9=extract_days(allres,dois_hosps,input_names,params8)
    #omicron
    alldata_tra_omi1=extract_days(allres,dois_omi,input_names,params9)
    #alldata_tra_cum2=extract_days(allres,dois_cum,input_names,params3)
    #alldata_tra_cum3=extract_days(allres,dois_cum,input_names,params4)
    alldata_tra=pd.concat([alldata_tra_hosp1,
                           alldata_tra_hosp2.drop(input_names,axis=1),
                           alldata_tra_hosp3.drop(input_names,axis=1),
                           alldata_tra_hosp4.drop(input_names,axis=1),
                           alldata_tra_hosp5.drop(input_names,axis=1),
                           alldata_tra_hosp6.drop(input_names,axis=1),
                           alldata_tra_hosp7.drop(input_names,axis=1),
                           alldata_tra_hosp8.drop(input_names,axis=1),
                           alldata_tra_hosp9.drop(input_names,axis=1),
                           alldata_tra_omi1.drop(input_names,axis=1),
                           
                          ],axis=1)
    wave_res={}
    wave_res["runs"]=allres
    wave_res["alldata_tra"]=alldata_tra
    wave_res["output_set_cal"]=output_set_cal
    np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_runs.npy", wave_res)
    
       
    print("Done")
   
    end3=time.time()
    print("Time %.2f"%(end3-end2))
    print("#######")
    
    if reuse_vals:
        print("Reusing validation runs...",)
        prev=np.load(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_vals.npy",allow_pickle='TRUE').item()
        allval=prev["runs_val"]
        #alldata_tra_val=load_all_tra_val(fromwave=5,towave=7)
    else:
        print("Making validation runs....",)
        if wave==1:
            samples_val=lhs_samples(nval)
        else:
            samples_val=disc_samples(nval,x)    
        allval=process_params(samples_val,k=k,parallel_jobs=parallel_jobs,max_folders=max_folders,basename="val",ndays=ndays)
        
        non_valid=filter_dict(allval,k)
        if len(non_valid)>0:
            for a in non_valid:
                del allval[a]
    
    
    alldata_tra_hosp1=extract_days(allval,dois_hosps,input_names,params0)
    alldata_tra_hosp2=extract_days(allval,dois_hosps,input_names,params1)
    alldata_tra_hosp3=extract_days(allval,dois_hosps,input_names,params2)
    alldata_tra_hosp4=extract_days(allval,dois_hosps,input_names,params3)
    alldata_tra_hosp5=extract_days(allval,dois_hosps,input_names,params4)
    alldata_tra_hosp6=extract_days(allval,dois_hosps,input_names,params5)
    alldata_tra_hosp7=extract_days(allval,dois_hosps,input_names,params6)
    alldata_tra_hosp8=extract_days(allval,dois_hosps,input_names,params7)
    alldata_tra_hosp9=extract_days(allval,dois_hosps,input_names,params8)
    alldata_tra_omi1=extract_days(allval,dois_omi,input_names,params9)
    alldata_tra_val=pd.concat([alldata_tra_hosp1,
                               alldata_tra_hosp2.drop(input_names,axis=1),
                               alldata_tra_hosp3.drop(input_names,axis=1),
                               alldata_tra_hosp4.drop(input_names,axis=1),
                               alldata_tra_hosp5.drop(input_names,axis=1),
                               alldata_tra_hosp6.drop(input_names,axis=1),
                               alldata_tra_hosp7.drop(input_names,axis=1),
                               alldata_tra_hosp8.drop(input_names,axis=1),
                               alldata_tra_hosp9.drop(input_names,axis=1),
                               alldata_tra_omi1.drop(input_names,axis=1),
                               ],axis=1)
   

    wave_res={}
    wave_res["runs_val"]=allval
    wave_res["alldata_tra_val"]=alldata_tra_val
    np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_vals.npy", wave_res)

    reuse_runs=False
    reuse_vals=False
    load_x=False
    print("Done")
    end4=time.time()
    print("Time %.2f"%(end4-end3))
    print("#######")

    alldata_tra=alldata_tra.astype(np.float32)
    
    mus=[x for x in alldata_tra.columns if "_mu-" in x]
    vars_=[x for x in alldata_tra.columns if "_var-" in x]

    print(mus)
        
    print("Training emulators...",)
    end5=time.time()
    if reuse_emu:
        emulators=np.load(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_emulators.npy",allow_pickle=True).item()["emulators"]
    else:
        emulators=emulate(inputs=alldata_tra[input_names].to_numpy(),outputs=alldata_tra[mus].to_numpy(),
                            output_set=output_set,max_degree=2,nproces=parallel_jobs_emulators)
        wave_res={}          
        wave_res["emulators"]=emulators
        np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_emulators.npy", wave_res)
    
    reuse_emu=False
      
    print("Done")
    
    end6=time.time()
    print("Time %.2f"%(end6-end5))
    print("#######")
    rs_m,coverages_m=check_emulators(alldata_tra_val=alldata_tra_val,
                                     emulators=emulators,
                                     outputs=mus,
                                     output_set=output_set,
                                     input_names=input_names,
                                 plots_folder=plots_folder)
    

    
    print("Rs ",)
    print(rs_m)
    print("Coverages ",)
    print(coverages_m)
    
    threshold_r=0.5
    threshold_coverage=0.8
    emu_mask=[(rs_m[i]>=threshold_r)&(coverages_m[i]>=threshold_coverage) for i in range(len(rs_m))]

    
    print("Number of emulators accepted ",sum(emu_mask))
    print("#######")
    end7=time.time()
    print("Exploring the parameters space and estimating Implausibility... ",)
    print("#######")
    before=x.shape[0]
    real_data=np.concatenate([get_real_data(dois_hosps,w=7,byage=True),get_real_data(dois_omi,w=7,omi=True)])
    print("real-> ",)
    print(real_data)
    
    vo=1.*real_data
    vo=vo*0.10
    vo[vo==0]=0.01
    imp_threshold=imp_thresholds[wave-1]
    
    vs=np.expand_dims(np.nanpercentile(alldata_tra[vars_],50,axis=0),axis=1)
    
    
    x=filter_implausibility(x=x,emu_object_mean=emulators,real_value=real_data,
                            vs=vs,vo=vo,vm=0.01,imp_threshold=imp_threshold,emu_mask=emu_mask,nproces=20)
    
    end8=time.time()
    print("Done")
    print("Time %.2f"%(end8-end7))
    p_below=np.round((1.*x.shape[0]/before),3)
    
    print("Proportion of samples below threshold:  %.4f"%(p_below))
    
    
    
    try:
        wave_res={}
        wave_res["x_filt"]=x
        np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_xfilt.npy", wave_res)      
    except:
        print("x_filt too big")
    wave_res={}      
    wave_res["p_below"]=p_below
    wave_res["rs_m"]=rs_m
    wave_res["coverages_m"]=coverages_m
    wave_res["emu_mask"]=emu_mask
    
    np.save(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_post.npy", wave_res)
          
          
          
    
    g=sns.pairplot(pd.DataFrame(data=x[np.random.choice(list(range(x.shape[0])),size=1000),:],columns=input_names),kind="kde")
    g.fig.suptitle("Wave "+str(wave), y=1.08)
    plt.savefig(waves_folder+"wave"+str(wave)+"/wave_"+str(wave)+"_xfilt.png")
    plt.show()
    
    
    wave+=1
    print("end of wave")
    print("Time %.2f"%(time.time()-end0))
        
    
completed=time.time()
print("#######")
print("#######")
print("Time %.2f"%(completed-start))
