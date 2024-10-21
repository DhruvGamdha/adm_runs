# Ways to use:
# Single job
    # 1. sh batch_frameToVideo.sh
# Use GNU Parallel to run multiple jobs in parallel
    # sudo apt-get install parallel (for Ubuntu, if not installed)
    # module load gnuparallel (for Frontera)
    # 2. parallel --jobs 4 < batch_frameToVideo.sh

python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_006 --frameDirName temperature --framerate 15 --lastFrameCopyCount 10
python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_007 --frameDirName temperature
python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_009 --frameDirName temperature
python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_010 --frameDirName temperature
python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_011 --frameDirName temperature
python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_015 --frameDirName temperature
python frameToVideo.py --runDirPath /media/dgamdha/dataSSD/dhruv_ssd/ISU/PhD/Projects/LEAP_HI/runs/adm_runs/tests/frontera_run_020 --frameDirName temperature

