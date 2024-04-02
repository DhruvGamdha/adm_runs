# bash script to run post processing on the output of the simulation to create plots
# exe run command: mpirun -n 8 <path_to_exe_dir>/adm 2>&1 | tee output.log

# Check if no arguments were passed
if [ $# -eq 0 ]; then
    echo "Error: No time step and material (abs or pekk) arguments supplied."
    echo "Usage: $0 <argument1> [argument2] ..."
    exit 1
fi

dt=$1
material=$2

python generate_pvd.py
pvpython probTempSave.py
python allData_csvClearning.py $dt $material
pdflatex -interaction=nonstopmode plot.tex
pdflatex -interaction=nonstopmode fullPlot.tex