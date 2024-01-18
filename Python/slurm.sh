#!/usr/bin/bash
#SBATCH --job-name=Z_S_B_exLimit
#SBATCH --array=1-100%50
#SBATCH --ntasks=1
#SBATCH --mem=2G
#SBATCH --cpus-per-task=2
#SBATCH --output=result/Z_S_B_exLimit/%a/output.txt

source ~/.bashrc
conda activate env39

srun python main3.py -c Z_S_B_exLimit.yaml -w ${SLURM_ARRAY_TASK_ID} -o Z_S_B_exLimit/${SLURM_ARRAY_TASK_ID}