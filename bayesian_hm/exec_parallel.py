def exec_parallel(cmd):
    
    ret = subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    #useful-> ret.args,ret.returncode
    if ret.returncode== 0:
        #print("success")
        pass
        
    else:
        print("error")
    

