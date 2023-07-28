import statsmodels.api as sm
from multiprocessing import Pool
from sklearn.preprocessing import PolynomialFeatures
import mogp_emulator


class emulate():
    def __init__(self, inputs,outputs,output_set,max_degree=3,kernel="Matern52",nproces=None):
    
        #inputs=array (samples x parameters) 
        #outputs=array(samples x noutputs)
        #output_set -> A list of lists (size=noutputs) 
        #with the input columns to be used with each of the outputs in the emulators
        
        
        self.inputs = inputs
        self.outputs= outputs
        self.kernel=kernel
        self.max_degree=max_degree
        self.degrees=[]
        self.nprocess=nproces
        #self.pol_expansion=PolynomialFeatures(degree=self.degree)
        #self.link_func=link_func
        #self.nugget=nugget
        self.output_set=output_set
        self.mean_models=[self.get_mean_model(x) for x in range(outputs.shape[1])]
        if nproces:
            with Pool(processes=nproces) as pool:
                self.emulators=[x for x in pool.map(self.get_emulators,range(outputs.shape[1]))]
        else:
            self.emulators=[self.get_emulators(x) for x in range(outputs.shape[1])]
        self.emulators_index=[i for i, x in enumerate(self.emulators) if x!="0"]
        self.summary=[x.summary() for x in self.mean_models]
        
    

    
    def get_mean_model(self,nc):
        
        
        for i in range(1,self.max_degree+1):
            pol_expansion=PolynomialFeatures(degree=i)
            data = pol_expansion.fit_transform(self.inputs[:,self.output_set[nc]])
            #if self.link_func=="poisson":
            #    model=sm.GLM(self.outputs[:,nc],data, family=sm.families.Poisson()).fit()
            #elif self.link_func=="normal":
            model=sm.GLM(self.outputs[:,nc],data, family=sm.families.Gaussian()).fit()
            if model.pseudo_rsquared()>0.7:
                self.degrees.append(i)
                return model
        self.degrees.append(self.max_degree)
        return model
    
    def get_emulators(self,nc):
        try:
            priors=mogp_emulator.Priors.GPPriors(n_corr=len(self.output_set[nc]), nugget_type="adaptive")
            
            gp=mogp_emulator.GaussianProcess(self.inputs[:,self.output_set[nc]],
                                             self.outputs[:,nc]-self.mean_models[nc].predict(
                                                 PolynomialFeatures(degree=self.degrees[nc]).fit_transform(self.inputs[:,self.output_set[nc]])),kernel=self.kernel,
                                             priors=priors)
            mogp_emulator.fit_GP_MAP(gp)
            return gp
        except:
            return "0"
    
    
    def predict(self,newinputs,nc):#THE VARIABLES ARE SELECTED INSIDE THE FUNCTION
        data = PolynomialFeatures(degree=self.degrees[nc]).fit_transform(newinputs[:,self.output_set[nc]])
        output_mean=self.mean_models[nc].predict(data)
        output_emu=self.emulators[nc].predict(newinputs[:,self.output_set[nc]])
        output_emu["mean"]=output_emu["mean"]+output_mean
        return output_emu