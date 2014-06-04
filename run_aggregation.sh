#!/bin/bash
#SBATCH --job-name=hd
#SBATCH --output=hd.out
#SBATCH --error=hd.err
#SBATCH --nodes=5
#SBATCH --account=cmsc12300
#SBATCH --reservation=cmsc12300lab

module load midway-hadoop

module load git
# Remove output directory if it exists

input_folder=$1
output_folder=$2
RES_FILE=$3

git pull

hdfs dfs -rm -r -f ${output_folder}

sh compile.sh aggregation aggregation.java

# Run Hadoop
hadoop jar aggregation.jar org.myorg.aggregation ${input_folder} ${output_folder}

rm -f ${RES_FILE}
#Blah
hdfs dfs -getmerge ${output_folder} ${RES_FILE}

