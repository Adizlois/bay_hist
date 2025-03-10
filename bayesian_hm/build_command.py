import os
import config
def build_command(outputfolder,b,new_beta,omicron_increase,trans_rate,omi_seed,
                  sus1,sus2,sus3,sus4,sus5,sus6,sus7,sus8,sus9,fihr,ndays=200,seed=10,i=0,v=-1):
    inout=config.inout
    abm_dir=config.abm_dir
    outputfolder=inout+"/"+outputfolder
    if (not os.path.isdir(outputfolder)):
        os.mkdir(outputfolder)
    comm=abm_dir+"ABM -e "+inout+" -sus1 %f -sus2 %f -sus3 %f -sus4 %f -sus5 %f -sus6 %f -sus7 %f -sus8 %f -sus9 %f -fIHR %f -maxT %s -o %s -i %s -bR %s -bH %s -bP %s -bS %s -NEW_BETA_DELTA %f -OMICRON_SEEDING %d -CHANGE_TRANS_RATE %f -OMICRON_BETA_INCREASE %f -s %s -v %i"%(sus1,
    sus2,sus3,sus4,sus5,sus6,sus7,sus8,sus9,fihr,str(ndays),outputfolder,str(i),str(b),str(b),str(b),str(b),new_beta,omi_seed,trans_rate,omicron_increase,str(seed),v)
    return comm.split()