# Python_Post-Processing_README 

This folder includes custom written python scripts for analyzing in vivo and ex vivo 
extracellular field data. The scripts include: 

1. 'Cannula_analysis[NatCommun].py'  
2. 'DREADD_injection_analysis[NatCommun].py' 
3. 'Ex_vivo_analysis[NatCommun].py' 

Note: 
The use of these three scripts should follow the MatWAND pre-processing and spectral analysis 
steps detailed in MatWAND_Pre-Processing&Spectral_analysis_ReadMe.txt. 

All three python scripts accept pre-processed MATLAB data [PSD parameters - time] exported from 
the MatWAND application as detailed in MatWAND_Pre-Processing&Spectral_analysis_ReadMe.txt. 
Each script includes detailed notes within describing the analysis processes. 

Python code standard operating procedure:
Operation of the three python scripts are largely identical. For all three scripts, the 
variables 'filepath' and 'savepath' need to be updated with the paths to the folder to be 
analyzed and the folder to save the post-processed data to, respectively. Once updated, the 
scripts can be executed and post-processed data will be saved as .xlsx files in the folder 
specified in the savepath variable. 

The only exception to the standard operating procedure detailed above exists in the 
'Ex_vivo_analysis[NatCommun].py' script. Here, the user is required to select whether the 
script will analyze 2 treatment (baseline, CNO/NE) or 3 treatment (baseline, WB4101, WB4101+NE) 
experiments. To select either analysis type, simply comment out the unnecessary analysis type 
and ensure the necessary analysis type is uncommented. Instructions to comment/uncomment either 
section are detailed in the script. 

Averaged values exported to .xlsx files are organized according to the following organization scheme: 
Columns = Subject IDs in ascending order of Subject Order value. 
Rows = Conditions in chronological order [condition titles not consistently labeled]. 

Exported timeseries files (titled [treatment]_[frequency_band].xlsx; ex: 'cno_15-30.xlsx') are 
organized according to the following organization scheme: 
Columns = Subject IDs in ascending order of Subject Order value. 
Rows = Time index. 

Values from exported .xlsx files can be copied into Graphpad Prism for statistical analysis 
and plotting


