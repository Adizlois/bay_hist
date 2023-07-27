def disc_samples(num,x,unif=False):
    if unif:
        return x[np.random.choice(range(x.shape[0]),size=num),:]
    else:
        output=[]
        probs=x.shape[0]*[1./x.shape[0]]
        for i in range(num):
            output.append(x[np.random.choice(range(x.shape[0]),p=probs),:])
            probs=get_probability(x,np.array(output))
        return np.array(output)