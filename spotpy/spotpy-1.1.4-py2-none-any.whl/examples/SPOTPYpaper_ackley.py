# -*- coding: utf-8 -*-
'''
Copyright 2015 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).

:author: Tobias Houska

This class holds the example code from the ackley tutorial web-documention.
'''

import spotpy
from spot_setup_ackley import spot_setup


#Create samplers for every algorithm:
results=[]
dim=50


spot_setup=spot_setup(dim=dim)
rep=15000

#sampler=spotpy.algorithms.mc(spot_setup,    dbname=str(dim)+'ackleyMC',    dbformat='csv')
#sampler.sample(rep)
#results.append(sampler.getdata())
##
#sampler=spotpy.algorithms.lhs(spot_setup,   dbname=str(dim)+'ackleyLHS',   dbformat='csv')
#sampler.sample(rep)
#results.append(sampler.getdata())
#
#sampler=spotpy.algorithms.mle(spot_setup,   dbname=str(dim)+'ackleyMLE',   dbformat='csv')
#sampler.sample(rep)
#results.append(sampler.getdata())
#
#sampler=spotpy.algorithms.mcmc(spot_setup,  dbname=str(dim)+'ackleyMCMC',  dbformat='csv')
#sampler.sample(rep)
#results.append(sampler.getdata())
#
#sampler=spotpy.algorithms.sceua(spot_setup, dbname=str(dim)+'ackleySCEUA', dbformat='csv')
#sampler.sample(rep,ngs=2)
#results.append(sampler.getdata())

#sampler=spotpy.algorithms.sa(spot_setup,    dbname=str(dim)+'ackleySA',    dbformat='csv')
#sampler.sample(rep,Tini=30,Ntemp=30,alpha=0.99)
#results.append(sampler.getdata())
#
#sampler=spotpy.algorithms.demcz(spot_setup, dbname=str(dim)+'ackleyDEMCz', dbformat='csv')
#sampler.sample(rep,nChains=30)
#results.append(sampler.getdata())
##
#sampler=spotpy.algorithms.rope(spot_setup,  dbname=str(dim)+'ackleyROPE',  dbformat='csv')
#sampler.sample(rep)
#results.append(sampler.getdata())

from spotpy import analyser

reps=[2,3,5,10,20,30,50]
algorithms=['MC','LHS','MLE','MCMC','SCEUA','SA','DEMCz','ROPE']
fig=plt.figure(figsize=(19,16))
font = {'family' : 'calibri',
        'weight' : 'normal',
        'size'   : 20}
plt.rc('font', **font) 
for r in range(len(reps)):
    #ax=plt.subplot(len(reps))
    results=[]
    for algorithm in algorithms:
        results.append(spotpy.analyser.load_csv_results(str(reps[r])+'ackley'+algorithm))

    
    xticks=[5000,10000]
    
    for i in range(len(results)):
        ax  = plt.subplot(len(reps),len(results),i+1+(len(results))*r)
        likes=[]
        sim=spotpy.analyser.get_modelruns(results[i])
        for s in sim:
            likes.append(spotpy.likelihoods.rmse(list(s),[0]))        
        #likes=spotpy.analyser.calc_like(results[i],[0]*reps[r])  
        ax.plot(likes,'b-')
        ax.set_ylim(0,25)
        ax.set_xlim(0,len(results[0]))
        if r == len(reps)-1:
            ax.set_xlabel(algorithms[i])
            ax.xaxis.set_ticklabels(xticks)
        if not r == len(reps)-1:
            ax.xaxis.set_ticklabels([])
            
        ax.xaxis.set_ticks(xticks)
        if i==0:
            ax.set_ylabel('RMSE d='+str(reps[r]))
            ax.yaxis.set_ticks([0,10,20])   
        else:
            ax.yaxis.set_ticks([])        
        
plt.tight_layout()
fig.savefig('Fig9.tif',dpi=300)
#for i in range(len(results)):
#    results[i]['like'].tofile(str(dim)+'pars_with_'+algorithms[i]+'.csv',sep=',')


    
#evaluation = spot_setup.evaluation()

#spotpy.analyser.plot_likelihoodtraces(results,evaluation,algorithms)


