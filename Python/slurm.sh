#!/usr/bin/bash
sbatch<<EOT
#!/usr/bin/bash
#SBATCH -J $1 #job_name
#SBATCH --array=1-$2
#SBATCH --mem=2G
#SBATCH --ntasks=1
#SBATCH --output=result/$4/$1/%a/output.txt
#SBATCH --cpus-per-task=2
#$5

source ~/.bashrc
conda activate env39

srun python main3.py -c conf/$1.yaml -w $3 -o $4/$1/$3
sleep 60

EOT