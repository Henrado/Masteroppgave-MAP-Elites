#!/usr/bin/bash
# Array med alle configfilene 
array=( Z_S_B_exLimit Z_SUfq_B_exLimit Z_T_B_exLimit T_TWoff_B_exLimit Z_TWoffFq_B_exLimit )
echo ${array[0]}
for i in "${array[@]}";
do
        if [[ $i == $array ]]
        then
                jobstr=$(sbatch slurm.sh $i --job-name=$i --output=result/$i/%a/output.txt)
        else
                jobstr=$(sbatch slurm.sh $i --job-name=$i --output=result/$i/%a/output.txt --dependency=aftercorr:${jobstr##* })
        fi
        echo $jobstr
done