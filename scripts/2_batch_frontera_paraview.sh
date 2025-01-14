# Ways to use:
# Single job
    # 1. source ~/pvmodules.sh
    # 2. sh batch_frontera_paraview.sh

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_015/data
swr -p 1 pvbatch pvSaveAnimation.py abs

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_016/data
swr -p 1 pvbatch pvSaveAnimation.py abs

