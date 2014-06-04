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

git pull
input_file=$1
output_file=$2
RES_FILE=$3
hdfs dfs -rm -r -f ${output_file}

sh compile.sh matchup matchup.java

# Run Hadoop
hadoop jar matchup.jar org.myorg.matchup ${input_file} ${output_file}

rm -f ${RES_FILE}

hdfs dfs -getmerge ${output_file} ${RES_FILE}

