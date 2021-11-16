This read me file exists as a supplement to the published MatWAND 
instructions on the MatWAND website 
(https://pantelisantonoudiou.github.io/MatWAND/).

Installation instructions and general MatWAND operations are discussed 
in the published MatWAND documentation.The MatWAND procedure detailed 
below describes the application's intended use protocol for 
pre-processing and spectral analysis of LFP data collected for this 
manuscript.  Please read through the published MatWAND documentation, 
then this protocol before beginning. 

Note: 
The MatWAND MATLAB application accepts several raw data filetypes, 
however data collected for this manuscript was imported to MatWAND
from AD Instruments LabChart 8 (single channel) as a MATLAB filetype. 


Folder Organization: 
MatWAND utilizes an application-specific directory naming protocol to 
locate and import raw data files. 

Raw data exported from LabChart should be placed in a project subfolder
labeled 'raw_data' 

ex: C:\Users\ ... Example_data\raw_data\ 


File Naming: 
Raw data exported from LabChart should be named using the following
naming scheme: 
[Subject-ID]_[Subject-order]_[Condition].mat 

For simplicity, the condition name is kept consistent across 
experiments as 'wt.' 

Underscores (_) in the filename should be reserved 
for the positions denoted in the naming scheme above. All other text 
separations should use a hyphen (-). 

ex: Mouse1-hM3D-CNO_1_wt.mat 

The protocol that follows can be executed using the provided 
example DREADD injection data. A user can demo MatWAND using the 
provided data and copying the example inputs below when prompted. 

MatWAND protocol: 

1. Load raw data 

a. 	With the MatWAND application opened, load raw data by pressing the 
	'Raw data folder' button to the left of the application. 

b. 	Select file settings (consistent across experiments): 
	File Type = mat 
	Channel Structure = bla 	
	Channel Analyzed = bla 
	Select Enter 

c. 	Navigate to the appropriate raw_data folder in the MatWAND folder navigation 
	window, then press 'select window'
	ex: C:\Users\ ... \Example_data\raw_data\ 
	
2. Apply Fast Fourier transform on selected data 

a.  	On the MatWAND application homescreen, press on the 'Get FFT' 
	slider, then select 'Yes' when asked 'Separate Conditions?' 
	
	Note: The observation frequency range on the input window that 
	follows is purely for observation purposes only. The default 
	setting '2 - 80' can be kept. 

	Enter the conditions for the experiment 
	ex: base;veh;cno 

	select 'OK' 

b. 	A representative window displaying power area and peak frequency
	over time will appear. Use this opportunity to inspect the power
	area plot for irregularities attributable to experimental confounds. 

	If the power area plot is acceptable, input '1' under 'Save experiment.' 
	Otherwise, input '0' 

	'Conditions:' should display the previously input conditions. However, 
	if you would like to remove a condition presented in the power area 
	plot, simply input 'false' in the conditions field. 
	ex: 'base;false;cno' would remove the veh condition. 
	Since there is no reason to remove conditions from the example file, 
	the default inputs can be left alone. 

	select 'OK' when ready to proceed  

3. Select analysis windows 

a. 	When prompted with 'Time-Locked Separation? (Essential for time plots)' 
	select 'Yes' 

b. 	The following window displays experiment IDs along with recording durations. 
	Close this window to select the analysis windows. 
	
	Under 'Conditions,' organize the conditions chronologically, 
	separated by semicolons.  
	ex: wt_base;wt_veh;wt_cno 

	Under 'Condition duration min,' input time durations for each 
	condition, separated by spaces. 
	ex: -60 0 0 60 0 60 
	    This input selects the last 60 minutes of the baseline, 
	    first 60 minutes of vehicle, and the first 60 minutes of 
	    CNO.  

	select 'OK' when ready to proceed 

4. Power Spectral Density Processing 

a. 	With the FFT analysis completed, select 
	'Power Spectral Density processing...' on the MatWAND homescreen 

b. 	On the PSD Analysis - User Input window, a user can adjust certain
	parameters as well as apply data cleaning functions. 
	
	The following inputs were kept consistent across all experiments 
	in this manuscript: 
	
	Change Bin Size: no 
	Normalize?: no 
	Linearize?: no 
	Remove Noise?: yes 
		Band Freq.: 60 Hz 
		Band Width 1 Hz 
	Remove Outliers?: yes 
		3x Median 

c. 	Select 'Enter' to proceed to final condition naming 

d. 	Under 'Enter conditions,' reorganize the conditions in 
	chronological order 
	ex: wt_base;wt_veh;wt_cno 
	
	Select 'OK' when ready to proceed. 

PSD processing completed. 

5. Export power area. 
   With the PSD processing completed, we can now export power area values 
   for all included experiments. 

a. 	On the top menu of the MatWAND homepage, select 'Export Data' 

b. 	In the 'Export Data' dropdown, select 'MATLAB' --> 'PSD parameters - time'

c. 	Select the low and high frequency bounds of the frequency band to be exported. 
	ex: Low Frequency:  2 
	    High Frequency: 6 
	
	Do not select 'Normalize to baseline?' (This will be done later in Python) 
	Select 'Paired' (All extracellular field experiment designs here are paired) 

	Select 'OK' when ready to proceed. 

Note: 
Bandpass filtered power area data will be exported to a new project 
subfolder titled 'analysis_[Channel_Analyzed]' 
For this example protocol, the subfolder will be titled 'analysis_bla' 

Within the analysis folder, a subfolder titled 'exported' will contain 
the exported power area data as a .mat file 
ex: C:\Users\ ... \Example_data\analysis_bla\exported\bla_2_6 Hz_time.mat
	
Repeat these steps to get exported power area values for all frequency bands: 
2-6, 6-12, 15-30, 40-70, 70-120 

Direct the following post processing step described in 
'Python_Post-Processing_ReadMe.txt' towards this 'exported' folder 
to organize data for plotting and statistical analysis. 

**[<< Back to Main Page](/README.md)**
