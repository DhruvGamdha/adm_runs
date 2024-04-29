# bash script to run post processing on the output of the simulation to create plots

# Check if no arguments were passed
if [ $# -ne 3 ]; then
    echo "Error: Incorrect usage."
    echo "Usage: $0 <time step> <material (abs or pekk)> <voxel dx>"
    exit 1
fi

dt=$1
material=$2
dx=$3

# exe run command: mpirun -n 8 <path_to_exe_dir>/adm 2>&1 | tee output.log
# mpirun -n 8 /media/dgamdha/data/Dhruv/ISU/PhD/Projects/LEAP_HI/software/admanufacturing/cmake-build-release/adm 2>&1 | tee output.log

# # Generate pvd file, which is used by Paraview to load the data
python generate_pvd.py

# Load the pvd file and save the temperature value at the probe location in a csv file (probeTemp_imple2.csv)
pvpython probTempSave.py $material $dx

# Below script does the following things:
# 1. Reads the probeTemp_imple2.csv file 
# 2. Removes the entries for which the probe location is not  printed.
# 3. Offsets the time by subracting the time at which the probe location is printed for the first time.
# 4. Merge our simulation data with the data shared by Nagraj( Experimental and simulation data)
# 5. Save the output as result.csv
python createResult.py $dt $material $dx

# Reads the result.csv file and creates the plot as a pdf file
pdflatex -interaction=nonstopmode plot.tex

# Reads the result.csv file and creates the full plot as a pdf file
pdflatex -interaction=nonstopmode fullPlot.tex