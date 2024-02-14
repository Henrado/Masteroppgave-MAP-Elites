#!/usr/bin/bash
# Array med alle configfilene 
array=( Z_TWoff_B_exLimit Z_TWoffFq_B_exLimit G_S_B_exLimit G_SUfq_B_exLimit G_T_B_exLimit G_TWoff_B_exLimit G_TWoffFq_B_exLimit T_S_B_exLimit T_SUfq_B_exLimit T_T_B_exLimit T_TWoff_B_exLimit T_TWoffFq_B_exLimit )
count_ex=100
eksperiment_navn="Determ"
echo ${array[0]}
for i in "${array[@]}";
do
        if [[ $i == $array ]]
        then
                jobstr=$(bash slurm.sh $i $count_ex '${SLURM_ARRAY_TASK_ID}' $eksperiment_navn)
        else
                jobstr=$(bash slurm.sh $i $count_ex '${SLURM_ARRAY_TASK_ID}' $eksperiment_navn "SBATCH --dependency=aftercorr:${jobstr##* }")
        fi
        echo $jobstr
done