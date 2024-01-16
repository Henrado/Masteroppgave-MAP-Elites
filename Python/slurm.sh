#!/bin/bash
jobname=$1
output_dir=$2
n_jobs=$3

#SBATCH --job-name $jobname
#SBATCH --output $output_dir/%j/output.txt
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=500M

# load modules
source ~/.bashrc
conda activate env39

for i in {1..$n_jobs}; do
    while [ "$(jobs -p | wc -l)" -ge "$SLURM_NTASKS" ]; do
        sleep 30
    done
    srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK bash -c 'echo hello "$i"' &
done
wait