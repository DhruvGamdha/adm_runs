""" 
This file is used to set the csv file in the correct format for the plotting script.
1. It reads the allData.csv file
2. It removes the initial rows for which the column 6 is zero
3. It adds a column adter column 2 with the value from column 2 multiplied with time step parameter
4. It adds a column after column 3 with the value from column 3 subtracted by the fist value of column 3
5. It saves the new csv file as allData_csvClearning.csv
"""

import pandas as pd
import os
import sys

def clean_and_save_csv(probe_file, exp_file, time_step, output_file, timeOffset):
    # 1. Reading the allData.csv file from the current directory
    startpath = os.path.dirname(os.path.realpath(__file__))
    df_probe = pd.read_csv(startpath + '/' + probe_file)

    # 2. Removing the initial rows for which the column 6 is zero
    df_probe = df_probe[df_probe.iloc[:, 5] != 0]
    df_probe.reset_index(drop=True, inplace=True)
    
    timeCount_col_ind = df_probe.columns.get_loc('Time')
    
    # Subtracting the time take to print the volume upto the probe location point (30, 0, 4.4), wall size (60, 1.25, 50)
    # Probe is at 6th layer, at the center of the wall, each layer is 0.8 mm tall, 1.25 mm wide, 60 mm long
    # volume of each layer = 1.25 * 0.8 * 60 = 60 mm^3
    # volume upto probe location point = 330 mm^3 ( 60 * 5 + 60 * 0.5)
    # Printer speed = 6.741 mm^3/s
    # Time taken to print upto probe location point = 330 / 6.741 = 48.954 s
    new_df = pd.DataFrame()
    new_df[''] = ''     # Add a empty 1st column to new_df 
    new_df['Time (s)'] = df_probe.iloc[:, timeCount_col_ind] * time_step + timeOffset
    new_df['Temp Sim (K)'] = df_probe.iloc[:, 5]
    new_df = pd.concat([pd.DataFrame([['', '', '']], columns=new_df.columns), new_df], ignore_index=True)   # Add a empty row at the top of new_df
    
    # open the output file (csv) and append the new data to it (column wise append)
    df_exp = pd.read_csv(startpath + '/' + exp_file)
    df_output = pd.concat([df_exp, new_df], axis=1)
    
    df_output.to_csv(startpath + '/' + output_file, index=False)

if __name__ == "__main__":
    
    dt = 0.7416
    material = 'abs'
    timeOffset = 48.954
    numTimestepPerVoxel = 4
    
    if len(sys.argv) > 3:
        dt = float(sys.argv[1])
        material = sys.argv[2]
        numTimestepPerVoxel = int(sys.argv[3])
    else:
        print("Please provide the time step, material (abs or pekk) and number of time steps per voxel as input arguments")
        sys.exit(1)
        
    probe_file='probeTemp_imple2.csv'
    
    if material == 'abs':
        exp_file='paperData_full.csv'
        timeOffset = 48.954
    elif material == 'pekk':
        exp_file='paperData_full_pekk.csv'
        timeOffset = 53.2962
    
    timeOffset = -timeOffset + numTimestepPerVoxel * dt
    
    output_file='result.csv'
    clean_and_save_csv(probe_file, exp_file, dt, output_file, timeOffset)