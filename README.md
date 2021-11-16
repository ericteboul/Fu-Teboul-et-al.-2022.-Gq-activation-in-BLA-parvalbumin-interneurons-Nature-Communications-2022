# Fu&Teboul-et-al.-Nature-Communications-Submission-Software-and-Code 

This repository includes the necessary files required to analyze acquired in vivo and ex vivo
extracellular field data, including example data and outcomes at all stages of the analysis protocol. 

Python version tested: 3.8.8 
Python IDE tested: Spyder 4.2.1 
MATLAB version tested: R2019b, R2021b

Python dependencies: 
numpy 
pandas 
scipy 

Non-standard hardware required? No 

Typical install time on a "normal" windows computer: plug and play MATLAB and Python code. No install time. 
Tested on a Dell XPS 15 running Windows 10 Home: 
	Processor - Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz   2.60 GHz 
	RAM - 16.0 GB (15.9 GB usable) 
	System type - 64-bit operating system, x64-based processor 
Tested on a Lenovo ThinkCentre running Windows 10 Enterprise 
	Processor - Intel(R) Core(TM) i5-7600T CPU @ 2.80 GHz   2.81GHz  
	RAM - 16.0 GB (15.9 GB usable) 
	System type - 64-bit operating system, x64-based processor 

Expected run time for demo on a "normal" desktop computer: 5-10 minutes including all steps

----- Standard Operating Procedure ------------- 

1. Export LFP data from LabChart File 
   (example exported LabChart data included in 'Example-Data' branch) 

2. Process exported LFP data in MatWAND. Export processed power area data for 
   post-processing in Python 

	a. 	See https://pantelisantonoudiou.github.io/MatWAND/ for installation and general 
		operation instructions. See 'MatWAND_Pre-Processing&Spectral_analysis_ReadMe.txt' for 
  	     	manuscript-specific MatWAND operation instructions included in 'MATLAB Scripts' branch. 

	b. 	See provided expected outcomes in 'Example-Data-and-Expected_Outcomes' branch.   

3a. Organize exported power area data in Python 

	a. 	See 'Python-Scripts' branch for experiment-specific analysis scripts 

	b. 	See Python_Post-Processing_ReadMe ('Python-Scripts/README.md') provided in 'Python-Scripts' branch for Python script operation instructions. 

	c. 	See Python_Post-Processing_ReadMe ('Python-Scripts/README.md') provided in 'Python-Scripts' branch for export instructions for analysis in GraphPad 		    Prism 

3b. Organize and analyze processed MatWAND data for distribution analysis in MATLAB 

	a. 	See main.m included in 'MATLAB Scripts' branch for analysis script with included instructions
	



