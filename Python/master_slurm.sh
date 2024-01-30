#!/usr/bin/bash
# Array med alle configfilene 
array=( Z_S_B_exLimit Z_SUfq_B_exLimit Z_T_B_exLimit T_TWoff_B_exLimit Z_TWoffFq_B_exLimit )
count_ex=100
echo ${array[0]}
for i in "${array[@]}";
do
        if [[ $i == $array ]]
        then
                jobstr=$(bash slurm.sh $i $count_ex '${SLURM_ARRAY_TASK_ID}')
        else
                jobstr=$(bash slurm.sh $i $count_ex '${SLURM_ARRAY_TASK_ID}' "SBATCH --dependency=aftercorr:${jobstr##* }")
        fi
        echo $jobstr
done