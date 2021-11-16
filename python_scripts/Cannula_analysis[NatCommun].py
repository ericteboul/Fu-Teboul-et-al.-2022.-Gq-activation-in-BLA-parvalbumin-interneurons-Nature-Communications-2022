# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 05:32:10 2021

@author: Eric Teboul

The following script analyzes in vivo field data for cannula infusion experiments.  
To utilize this script, simply update the filepath with the folder to be analyzed 
and the savepath with the folder to save the post-processed data to, then press run. 
"""


from scipy.io import loadmat 
import numpy as np 
import pandas as pd 


frequency_bands = np.array(['2-6', '6-12', '15-30', '40-70', '70-120'])

filepath = 'C:/Users/Eric Teboul/Desktop/WB4101 natcom temp/analysis_bla/exported/' # path to folder containing exported .mat files from MatWAND
savepath = 'C:/Users/Eric Teboul/Desktop/WB4101 natcom temp/analysis_bla/' # path to folder where post-processed data will be saved 

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
        
# restructure data into 4 treatments 
    
    powerarea = x['power_area']     
    
    base = {} # Baseline 
    inj1 = {} # Saline 
    inj2 = {} # Saline or Antagonist (depending on the experiment being analyzed)
    inj3 = {} # Drug or Drug w/ Antagonist (depending on the experiment being analyzed)
    power_area = {} 
    
    for i in range(powerarea.shape[0]) :
        power_area[str(i)] = powerarea[i][:]
        power_area[str(i)] = np.reshape(power_area[str(i)], (4, int(len(power_area[str(i)])/4))) 
        base[str(i)] = power_area[str(i)][0]
        inj1[str(i)] = power_area[str(i)][1]
        inj2[str(i)] = power_area[str(i)][2]
        inj3[str(i)] = power_area[str(i)][3]

# Normalize to baseline and restructure into 1 minute bins   
        
    base_norm = {} 
    for key, value in base.items(): 
        base_norm[str(key)] = value/np.mean(value) 
        base_norm[str(key)] = np.mean(base_norm[str(key)].reshape(-1,24), axis = 1) 
        
    inj1_norm = {} 
    for (key, value), (k, v) in zip(inj1.items(), base.items()): 
        inj1_norm[str(key)] = value/np.mean(v) 
        inj1_norm[str(key)] = np.mean(inj1_norm[str(key)].reshape(-1,24), axis = 1)
    
    inj2_norm = {} 
    for (key, value), (k, v) in zip(inj2.items(), base.items()): 
        inj2_norm[str(key)] = value/np.mean(v) 
        inj2_norm[str(key)] = np.mean(inj2_norm[str(key)].reshape(-1,24), axis = 1)
    
    inj3_norm = {} 
    for (key, value), (k, v) in zip(inj3.items(), base.items()): 
        inj3_norm[str(key)] = value/np.mean(v) 
        inj3_norm[str(key)] = np.mean(inj3_norm[str(key)].reshape(-1,24), axis = 1) 

    # export normalized timeseries data to excel 
    
    base_norm = pd.DataFrame(base_norm) 
    base_norm.to_excel(savepath + 'base_'+g+'.xlsx') 
    
    inj1_norm = pd.DataFrame(inj1_norm) 
    inj1_norm.to_excel(savepath + 'inj1_'+g+'.xlsx') 
    
    inj2_norm = pd.DataFrame(inj2_norm) 
    inj2_norm.to_excel(savepath + 'inj2_'+g+'.xlsx')  
    
    inj3_norm = pd.DataFrame(inj3_norm) 
    inj3_norm.to_excel(savepath + 'inj3_'+g+'.xlsx') 
    
# Get average first 10 mins values for Two-Way ANOVA w/ multiple comparisons * [normalized data] *  
     
    base_mc = np.array([]) 
    for key, value in base_norm.items(): 
        base_mc = np.append(base_mc, np.mean(value[:(int(len(value)/6))]))
    
    inj1_mc = np.array([])  
    for key, value in inj1_norm.items(): 
        inj1_mc = np.append(inj1_mc, np.mean(value[:(int(len(value)/6))]))
    
    inj2_mc = np.array([])  
    for key, value in inj2_norm.items(): 
        inj2_mc = np.append(inj2_mc, np.mean(value[:(int(len(value)/6))]))
    
    inj3_mc = np.array([]) 
    for key, value in inj3_norm.items(): 
        inj3_mc = np.append(inj3_mc, np.mean(value[:(int(len(value)/6))])) 
    
    if g == '2-6' : 
        slow_theta = np.concatenate(([base_mc], [inj1_mc], [inj2_mc], [inj3_mc]), axis=0) 
    elif g == '6-12' : 
        fast_theta = np.concatenate(([base_mc], [inj1_mc], [inj2_mc], [inj3_mc]), axis=0)  
    elif g == '15-30' : 
        beta = np.concatenate(([base_mc], [inj1_mc], [inj2_mc], [inj3_mc]), axis=0) 
    elif g == '40-70' : 
        slow_gamma = np.concatenate(([base_mc], [inj1_mc], [inj2_mc], [inj3_mc]), axis=0) 
    elif g == '70-120' : 
        fast_gamma = np.concatenate(([base_mc], [inj1_mc], [inj2_mc], [inj3_mc]), axis=0) 
        
# Export average normalized first 10 mins values to excel  
    
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









