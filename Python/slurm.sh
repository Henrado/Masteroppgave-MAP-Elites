#!/usr/bin/bash
#SBATCH --job-name=testslurm
#SBATCH --array=1-20
#SBATCH --ntasks=1
#SBATCH --mem=2G
#SBATCH --output=result/testslurm/%a/output.txt

source ~/.bashrc
conda activate env39

srun python main3.py -c conf.yaml -w ${SLURM_ARRAY_TASK_ID} -o testslurm/${SLURM_ARRAY_TASK_ID}