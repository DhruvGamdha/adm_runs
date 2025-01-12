#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Frontera CLX nodes
#
#   *** MPI Job in Normal Queue ***
# 
# Last revised: 20 May 2019
#
# Notes:
#
#   -- Launch this script by executing
#      "sbatch clx.mpi.slurm" on a Frontera login node.
#
#   -- Use ibrun to launch MPI codes on TACC systems.
#      Do NOT use mpirun or mpiexec.
#
#   -- Max recommended MPI ranks per CLX node: 56
#      (start small, increase gradually).
#
#   -- If you're running out of memory, try running
#      fewer tasks per node to give each task more memory.
#
#----------------------------------------------------

#SBATCH -J 3DBenchy_64R    # Job name
#SBATCH -o 3DBenchy_64R.o%j# Name of stdout output file
#SBATCH -e 3DBenchy_64R.e%j# Name of stderr error file
#SBATCH -p normal          # Queue (partition) name
#SBATCH -N 3               # Total # of nodes 
#SBATCH -n 128             # Total # of mpi tasks
#SBATCH -t 12:00:00        # Run time (hh:mm:ss)
#SBATCH --mail-type=all    # Send email at begin and end of job
#SBATCH -A NAIRR240115     # Project/Allocation name (req'd if you have more than 1)
#SBATCH --mail-user=dgamdha@iastate.edu

# Activate the Python virtual environment
source /work2/09374/dgamdha/frontera/venv/gen/bin/activate

# Launch MPI code... 
# python convergencet.py printCorrected_3DBenchy_128R.csv 2 frontera
# python convergencet.py printCorrected_3DBenchy_64R.csv 2 frontera
# python convergencet.py printCorrected_3DBenchy_32R.csv 2 frontera
python convergencet.py printCorrected_3DBenchy_128R.csv 5 frontera

# python convergencet.py bunny_128_zeroSparsity.csv 2 frontera
# python convergencet.py bunny_64_zeroSparsity.csv 2 frontera
# python convergencet.py bunny_32_zeroSparsity.csv 2 frontera
# python convergencet.py bunny_128_zeroSparsity.csv 5 frontera

# python convergencet.py Moai_128_zeroSparsity.csv 2 frontera
# python convergencet.py Moai_64_zeroSparsity.csv 2 frontera
# python convergencet.py Moai_32_zeroSparsity.csv 2 frontera
# python convergencet.py Moai_128_zeroSparsity.csv 5 frontera