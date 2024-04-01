
exe run command: ```mpirun -n 8 <path_to_exe_dir>/adm 2>&1 | tee output.log```

Steps after the simulation:
1. Run generate_pvd.py file
   1. ```python generate_pvd.py```
2. Extract temperature data at the probe location by running the probTempSave.py file using pvpython
   1. ```pvpython probTempSave.py```
3. Adjust the temperature data by running allData_cvsClearing.py file, this file requires timestep (dt) as command line argument and the comparison data file is hardcoded to be of **ABS material** (paperData_full.csv), to use for **PEKK material** (paperData_full_pekk.csv) change the file name. This will convert time in to seconds and subtract the print time upto the probe location from the time.
   1. ```python allData_csvClearning.py <dt>```
4. Run the plot.tex and fullPlot.tex files to generate the plots
   1. ```pdflatex plot.tex```
   2. ```pdflatex fullPlot.tex```