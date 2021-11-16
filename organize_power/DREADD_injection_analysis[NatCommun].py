# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 05:32:10 2021

@author: Eric Teboul

The following script analyzes in vivo field data for DREADD experiments.  
To utilize this script, simply update the filepath with the folder to be analyzed 
and the savepath with the folder to save the post-processed data to, then press run. 
"""


from scipy.io import loadmat 
import numpy as np 
import pandas as pd 


frequency_bands = np.array(['2-6', '6-12', '15-30', '40-70', '70-120'])

filepath = 'C:/Users/Eric Teboul/Desktop/NatCommun Revisions/CNO control/analysis_bla/exported/' # path to folder containing exported .mat files from MatWAND 
savepath = 'C:/Users/Eric Teboul/Desktop/NatCommun Revisions/CNO control/analysis_bla/' # path to folder where post-processed data will be saved 

# This code will iterate through each exported bandpass filtered .mat file in the folderpath and save the post-processed data across frequency bands in the savepath 
# This code accepts 60 minute long bandpass filtered data (5 second bins [2.5 second overlap] = 24 datapoints per minute) exported from MatWAND. 
# Importing data of a different duration or samplerate will result in misleading outputs. 

for g in frequency_bands: 

    if g == '2-6' : 
        x = loadmat(filepath + 'bla_2_6 Hz_time.mat') 
    elif g == '6-12' : 
        x = loadmat(filepath + 'bla_6_12 Hz_time.mat') 
    elif g == '15-30' : 
        x = loadmat(filepath + 'bla_15_30 Hz_time.mat') 
    elif g == '40-70' : 
        x = loadmat(filepath + 'bla_40_70 Hz_time.mat') 
    elif g == '70-120' : 
        x = loadmat(filepath + 'bla_70_120 Hz_time.mat') 

# restructure data into 3 treatments 
        
    powerarea = x['power_area']     
    
    base = {} # Baseline 
    veh = {} # Vehicle 
    cno = {} # CNO or Vehicle 2 (depending on the experiment being analyzed) 
    power_area = {} 
    
    for i in range(powerarea.shape[0]) :
        power_area[str(i)] = powerarea[i][:]
        power_area[str(i)] = np.reshape(power_area[str(i)], (3, int(len(power_area[str(i)])/3))) 
        base[str(i)] = power_area[str(i)][0]
        veh[str(i)] = power_area[str(i)][1]
        cno[str(i)] = power_area[str(i)][2] 
        
    # for i in powerarea

# Normalize to baseline and restructure into 1 minute bins 
        
    base_norm = {} 
    for key, value in base.items(): 
        base_norm[str(key)] = value/np.mean(value) 
        base_norm[str(key)] = np.mean(base_norm[str(key)].reshape(-1,24), axis = 1) 
        
    veh_norm = {} 
    for (key, value), (k, v) in zip(veh.items(), base.items()): 
        veh_norm[str(key)] = value/np.mean(v) 
        veh_norm[str(key)] = np.mean(veh_norm[str(key)].reshape(-1,24), axis = 1)
    
    cno_norm = {} 
    for (key, value), (k, v) in zip(cno.items(), base.items()): 
        cno_norm[str(key)] = value/np.mean(v) 
        cno_norm[str(key)] = np.mean(cno_norm[str(key)].reshape(-1,24), axis = 1) 

    # export normalized timeseries data to excel 
    
    base_norm = pd.DataFrame(base_norm) 
    base_norm.to_excel(savepath + 'base_'+g+'.xlsx') 
    
    veh_norm = pd.DataFrame(veh_norm) 
    veh_norm.to_excel(savepath + 'veh_'+g+'.xlsx') 
    
    cno_norm = pd.DataFrame(cno_norm) 
    cno_norm.to_excel(savepath + 'cno_'+g+'.xlsx')  

# Get average last 30 mins values for Two-Way ANOVA w/ multiple comparisons * [normalized data] *      
     
    base_mc = np.array([]) 
    for key, value in base_norm.items(): 
        base_mc = np.append(base_mc, np.mean(value[(int(len(value)/2)):]))
    
    veh_mc = np.array([])  
    for key, value in veh_norm.items(): 
        veh_mc = np.append(veh_mc, np.mean(value[(int(len(value)/2)):]))
    
    cno_mc = np.array([])  
    for key, value in cno_norm.items(): 
        cno_mc = np.append(cno_mc, np.mean(value[(int(len(value)/2)):]))
    
    if g == '2-6': 
        slow_theta = np.concatenate(([base_mc], [veh_mc], [cno_mc]), axis=0) 
    elif g == '6-12': 
        fast_theta = np.concatenate(([base_mc], [veh_mc], [cno_mc]), axis=0)  
    elif g == '15-30': 
        beta = np.concatenate(([base_mc], [veh_mc], [cno_mc]), axis=0) 
    elif g == '40-70': 
        slow_gamma = np.concatenate(([base_mc], [veh_mc], [cno_mc]), axis=0) 
    elif g == '70-120': 
        fast_gamma = np.concatenate(([base_mc], [veh_mc], [cno_mc]), axis=0) 

# Export average normalized last 30 mins values to excel 
    
slow_theta = pd.DataFrame(slow_theta) 
slow_theta.to_excel(savepath + 'slow_theta.xlsx')

fast_theta = pd.DataFrame(fast_theta) 
fast_theta.to_excel(savepath + 'fast_theta.xlsx')

beta = pd.DataFrame(beta) 
beta.to_excel(savepath + 'beta.xlsx')

slow_gamma = pd.DataFrame(slow_gamma) 
slow_gamma.to_excel(savepath + 'slow_gamma.xlsx')

fast_gamma = pd.DataFrame(fast_gamma) 
fast_gamma.to_excel(savepath + 'fast_gamma.xlsx')




