#!/usr/bin/bash
# Array med alle configfilene 
array=( Z_S_C_exLimit T_S_C_exLimit G_S_C_exLimit Z_SUfq_C_exLimit Z_T_C_exLimit Z_TWoff_C_exLimit Z_TWoffFq_C_exLimit G_SUfq_C_exLimit G_T_C_exLimit G_TWoff_C_exLimit G_TWoffFq_C_exLimit T_SUfq_C_exLimit T_T_C_exLimit T_TWoff_C_exLimit T_TWoffFq_C_exLimit )
start=1
stop=10
eksperiment_navn="Circle"
echo ${array[0]}
for i in "${array[@]}";
do
        if [[ $i == $array ]]
        then
                jobstr=$(bash slurm.sh $i $start $stop '${SLURM_ARRAY_TASK_ID}' $eksperiment_navn)
        else
                jobstr=$(bash slurm.sh $i $start $stop '${SLURM_ARRAY_TASK_ID}' $eksperiment_navn "SBATCH --dependency=aftercorr:${jobstr##* }")
        fi
        echo $jobstr
done