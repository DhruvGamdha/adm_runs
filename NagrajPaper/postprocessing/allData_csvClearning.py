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

def clean_and_save_csv(input_file, output_file, time_step=1):
    # 1. Reading the allData.csv file from the current directory
    # cwd = os.getcwd()
    startpath = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(startpath + '/' + input_file)

    # 2. Removing the initial rows for which the column 6 is zero
    df = df[df.iloc[:, 5] != 0]

    # Resetting index after removing rows
    df.reset_index(drop=True, inplace=True)
    
    timeCount_col_ind = df.columns.get_loc('Time')
    
    timeSec_col_name = 'Time(s)'
    timeSec_col_ind = timeCount_col_ind + 1
    
    timeOffset_col_name = 'Time offset'
    timeOffset_col_ind = timeSec_col_ind + 1
    
    # 3. Adding a column after column 2 with the value from column 2 multiplied with time step parameter
    df.insert(timeSec_col_ind, timeSec_col_name, df.iloc[:, timeCount_col_ind] * time_step)

    # 4. Adding a column after column 3 with the value from column 3 subtracted by the first value of column 3
    
    # Subtracting the time take to print the volume upto the probe location point (30, 0, 4.4), wall size (60, 1.25, 50)
    # Probe is at 6th layer, at the center of the wall, each layer is 0.8 mm tall, 1.25 mm wide, 60 mm long
    # volume of each layer = 1.25 * 0.8 * 60 = 60 mm^3
    # volume upto probe location point = 330 mm^3 ( 60 * 5 + 60 * 0.5)
    # Printer speed = 6.741 mm^3/s
    # Time taken to print upto probe location point = 330 / 6.741 = 48.954 s
    
    df.insert(timeOffset_col_ind, timeOffset_col_name, df.iloc[:, timeSec_col_ind] - 48.954)

    # 5. Saving the new csv file as allData_csvClearning.csv
    df.to_csv(startpath + '/' + output_file, index=False)

if __name__ == "__main__":
    
    # dt = 0.007714
    dt = 0
    if len(sys.argv) > 1:
        dt = float(sys.argv[1])
    else:
        print("Please provide the time step as an argument")
        sys.exit(1)
    input_file='probeTemp_imple2.csv'
    output_file='configured_probeTemp_imple2.csv'
    clean_and_save_csv(input_file, output_file, dt)