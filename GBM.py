import numpy as np
import pandas as pd
import Stock_Info as stocks

def model (num_dias,miu,sigma,s0):

    

    simulacion=np.zeros((10000,num_dias))
    simulacion[0]=s0
    dt=1/252
    for i in range(1,num_dias):
        e=np.random.standard_normal()
        simulacion[i]=simulacion[i-1]*np.exp((miu-0.5*sigma**2)*dt+sigma*e*np.sqrt(dt))

    return(simulacion)
