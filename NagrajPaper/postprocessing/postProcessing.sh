# bash script to run post processing on the output of the simulation to create plots
# exe run command: mpirun -n 8 <path_to_exe_dir>/adm 2>&1 | tee output.log

# Check if no arguments were passed
if [ $# -ne 3 ]; then
    echo "Error: Incorrect usage."
    echo "Usage: $0 <time step> <material (abs or pekk)> <number of time steps per voxel>"
    exit 1
fi

dt=$1
material=$2
numTimestepPerVoxel=$3

python generate_pvd.py
pvpython probTempSave.py $material
python allData_csvClearning.py $dt $material $numTimestepPerVoxel
pdflatex -interaction=nonstopmode plot.tex
pdflatex -interaction=nonstopmode fullPlot.tex