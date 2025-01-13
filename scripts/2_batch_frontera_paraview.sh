# Ways to use:
# Single job
    # 1. source ~/pvmodules.sh
    # 2. sh batch_frontera_paraview.sh

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_008/data
swr -p 1 pvbatch pvSaveAnimation.py abs

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_009/data
swr -p 1 pvbatch pvSaveAnimation.py abs

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_010/data
swr -p 1 pvbatch pvSaveAnimation.py abs

cd /scratch1/09374/dgamdha/projects/leaphi/adm_runs/tests/frontera_run_011/data
swr -p 1 pvbatch pvSaveAnimation.py abs

