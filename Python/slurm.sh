#!/usr/bin/bash
#SBATCH --job-name=parallell
#SBATCH --array=1-5      # Creates 4 jobs, with `${SLURM_ARRAY_TASK_ID}` values from 1 to 4
#SBATCH --mem 2G
#SBATCH --output=parallell/%a/output.txt

# load modules
source ~/.bashrc
conda activate env39

srun python main3.py -c conf.yaml -w ${SLURM_ARRAY_TASK_ID} -o testslurm/${SLURM_ARRAY_TASK_ID} &