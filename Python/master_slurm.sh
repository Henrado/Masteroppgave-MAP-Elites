#!/usr/bin/bash
# Array med alle configfilene 
array=( Z_S_B_exLimit T_S_B_exLimit )
start=1
stop=20

# array=( Z_SUfq_B_exLimit T_SUfq_B_exLimit  )
# start=21
# stop=40

# array=( Z_T_B_exLimit T_T_B_exLimit )
# start=41
# stop=60

# array=( Z_TWoff_B_exLimit T_TWoff_B_exLimit )
# start=61
# stop=80

# array=( Z_TWoffFq_B_exLimit G_TWoffFq_B_exLimit T_TWoffFq_B_exLimit )
# start=81
# stop=100

# array=( G_S_B_exLimit G_SUfq_B_exLimit )
# start=101
# stop=120

# array=( G_T_B_exLimit G_TWoff_B_exLimit )
# start=121
# stop=140

# array=( T_TWoffFq_B_exLimit )
# start=141
# stop=160

eksperiment_navn="kontrollers_timescale"
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