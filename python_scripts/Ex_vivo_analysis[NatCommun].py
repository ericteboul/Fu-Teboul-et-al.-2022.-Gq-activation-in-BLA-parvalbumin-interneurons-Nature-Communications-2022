# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:48:53 2021

@author: etebou01

The following script analyzes ex vivo field data. 
The script is segmented into two sections: (1) analyzing regular (NE and CNO) experiments, (2) analyzing antagonist experiments. 
To utilize one or the other section, simply uncomment the necessary section and comment out the unnecessary section. 

To comment out or uncomment a section, highlight the code and press ctrl/cmd + 1. 
Alternatively, you can right-click the highlighted code and select 'Comment/Uncomment' from the dropdown. 

Additionally, the filepath and savepath need to be updated with the folder to be analyzed 
and the folder to save the post-processed data to before running. 
"""

from scipy.io import loadmat 
import numpy as np 
import pandas as pd 


filepath = 'INSERT FILEPATH' # path to folder containing exported .mat files from MatWAND 
savepath = 'INSERT SAVEPATH' # path to folder where post-processed data will be saved 

# load data 

x = loadmat(filepath) 
powerarea = x['power_area']     

# ----------- FOR REGULAR EXPERIMENTS -----------------     

# restructure data into 3 treatments 

base = {} # Baseline 
cno = {} # CNO or NE (depending on the experiment being analyzed) 
power_area = {} 

for i in range(powerarea.shape[0]) :
    power_area[str(i)] = powerarea[i][1:]
    power_area[str(i)] = np.reshape(power_area[str(i)], (2, int(len(power_area[str(i)])/2))) 
    base[str(i)] = power_area[str(i)][0]
    cno[str(i)] = power_area[str(i)][1] 

# Normalize to baseline and restructure into 1 minute bins 

base_norm = {} 
for key, value in base.items(): 
    base_norm[str(key)] = value/np.mean(value) 
    base_norm[str(key)] = np.mean(base_norm[str(key)].reshape(-1,24), axis = 1) 

cno_norm = {} 
for (key, value), (k, v) in zip(cno.items(), base.items()): 
    cno_norm[str(key)] = value/np.mean(v) 
    cno_norm[str(key)] = np.mean(cno_norm[str(key)].reshape(-1,24), axis = 1) 

# export normalized timeseries data to excel 
    
base_norm = pd.DataFrame(base_norm) 
base_norm.to_excel(savepath + 'base_.xlsx') 

cno_norm = pd.DataFrame(cno_norm) 
cno_norm.to_excel(savepath + 'cno_.xlsx') 

# Get average values from last 10th to 15th minute of baseline and 3rd to 8th minute of NE/CNO 
# for Two-Way ANOVA w/ multiple comparisons * [normalized data] * 

base_mc = np.array([]) 
for key, value in base_norm.items(): 
    base_mc = np.append(base_mc, np.mean(value[10:])) 

cno_mc = np.array([])  
for key, value in cno_norm.items(): 
    cno_mc = np.append(cno_mc, np.mean(value[3:8])) 
gamma = np.concatenate(([base_mc], [cno_mc]), axis=0) 

# Export average normalized values to excel  

gamma = pd.DataFrame(gamma) 
gamma.to_excel(savepath + 'gamma.xlsx')

# --------------- FOR WB4101 EXPERIMENTS ------------------------ 

# # restructure data into 3 treatments 

# base = {} # Baseline 
# wb = {} # WB4101 
# wbne = {} # WB4101 + NE 
# power_area = {} 

# for i in range(powerarea.shape[0]) :
#     power_area[str(i)] = powerarea[i][3:] # [3:] removes the excess 3 samples MATWAND gives for some reason (it's usually 1 extra sample) 
#     power_area[str(i)] = np.reshape(power_area[str(i)], (3, int(len(power_area[str(i)])/3))) 
#     base[str(i)] = power_area[str(i)][0]
#     wb[str(i)] = power_area[str(i)][1]
#     wbne[str(i)] = power_area[str(i)][2]  

# # Normalize to baseline and restructure into 1 minute bins 

# base_norm = {} 
# for key, value in base.items(): 
#     base_norm[str(key)] = value/np.mean(value) 
#     base_norm[str(key)] = np.mean(base_norm[str(key)].reshape(-1,24), axis = 1) 

# wb_norm = {} 
# for (key, value), (k, v) in zip(wb.items(), base.items()): 
#     wb_norm[str(key)] = value/np.mean(v) 
#     wb_norm[str(key)] = np.mean(wb_norm[str(key)].reshape(-1,24), axis = 1) 

# wbne_norm = {} 
# for (key, value), (k, v) in zip(wbne.items(), base.items()): 
#     wbne_norm[str(key)] = value/np.mean(v) 
#     wbne_norm[str(key)] = np.mean(wbne_norm[str(key)].reshape(-1,24), axis = 1) 

# # export normalized timeseries data to excel 

# base_norm = pd.DataFrame(base_norm) 
# base_norm.to_excel(savepath + 'base_.xlsx') 

# wb_norm = pd.DataFrame(wb_norm) 
# wb_norm.to_excel(savepath + 'wb_.xlsx') 

# wbne_norm = pd.DataFrame(wbne_norm) 
# wbne_norm.to_excel(savepath + 'wbne_.xlsx') 

# # Get average values from last 10th to 15th minute of baseline, 3rd to 8th minute of WB4101, 
# # and 3rd to 8th minute of WB4101 + NE for Two-Way ANOVA w/ multiple comparisons * [normalized data] * 

# base_mc = np.array([]) 
# for key, value in base_norm.items(): 
#     base_mc = np.append(base_mc, np.mean(value[10:])) 

# wb_mc = np.array([])  
# for key, value in wb_norm.items(): 
#     wb_mc = np.append(wb_mc, np.mean(value[3:8])) 

# wbne_mc = np.array([])  
# for key, value in wbne_norm.items(): 
#     wbne_mc = np.append(wbne_mc, np.mean(value[3:8])) 

# gamma = np.concatenate(([base_mc], [wb_mc], [wbne_mc]), axis=0) 

# # Export average normalized values to excel  

# gamma = pd.DataFrame(gamma) 
# gamma.to_excel(savepath + 'gamma.xlsx') 






















