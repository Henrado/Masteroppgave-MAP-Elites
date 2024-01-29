#!/usr/bin/bash
#SBATCH --array=1-100
#SBATCH --ntasks=1
#SBATCH --mem=2G
#SBATCH --cpus-per-task=2

source ~/.bashrc
conda activate env39

srun python main3.py -c conf/$1.yaml -w ${SLURM_ARRAY_TASK_ID} -o $1/${SLURM_ARRAY_TASK_ID}

sleep 60