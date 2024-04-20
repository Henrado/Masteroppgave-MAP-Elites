#!/usr/bin/bash
# Array med alle configfilene 
# array=( Z_S_B_exLimit )
# start=1
# stop=20

# array=( Z_SUfq_B_exLimit )
# start=21
# stop=40

# array=( Z_T_B_exLimit )
# start=41
# stop=60

# array=( Z_TWoff_B_exLimit )
# start=61
# stop=80

# array=( Z_TWoffFq_B_exLimit )
# start=81
# stop=100

# array=( G_S_B_exLimit )
# start=101
# stop=120

# array=( G_T_B_exLimit )
# start=121
# stop=140

# array=( T_TWoffFq_B_exLimit )
# start=141
# stop=160

# array=( Z_TWoff_B_CS0 )
# start=161
# stop=180

# array=( Z_TWoff_B_CS1 Z_TWoff_B_HCS1 )
# start=181
# stop=200

# array=( Z_TWoff_B_CS2 Z_TWoff_B_HCS2 )
# start=201
# stop=220

# array=( Z_TWoff_B_CS5 Z_TWoff_B_HCS5 )
# start=221
# stop=240

array=( T_S_B_exLimit )
start=241
stop=260

# array=( T_SUfq_B_exLimit )
# start=261
# stop=280

# array=( T_T_B_exLimit )
# start=281
# stop=300

# array=( T_TWoff_B_exLimit )
# start=301
# stop=320

# array=( G_TWoffFq_B_exLimit )
# start=321
# stop=340

# array=( G_SUfq_B_exLimit )
# start=341
# stop=360

# array=( G_TWoff_B_exLimit )
# start=361
# stop=380



eksperiment_navn="miljo_timescale"
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