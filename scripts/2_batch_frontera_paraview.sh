# Ways to use:
# Single job
    # 1. Start a ondemand job on: https://tap.tacc.utexas.edu/jobs/ 
    # 2. source ~/pvmodules.sh
    # 3. sh batch_frontera_paraview.sh

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_001/data
swr -p 1 pvbatch pvSaveAnimation.py abs

# cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_016/data
# swr -p 1 pvbatch pvSaveAnimation.py abs

