import shutil
import os

def clean_dir(basedir="../In_out/",basename="output"):
    target=[x for x in os.listdir(basedir) if (basename in x)&("files" not in x)]
    if len(target)>0:
        [shutil.rmtree(os.path.join(basedir,x)) for x in target]
        print("Done")
    else:
        print("No result folder found")
        