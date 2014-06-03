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

hdfs dfs -rm -r output_aggregation

RES_FILE=results_aggregation.txt

sh compile.sh aggregation aggregation.java

# Run Hadoop
hadoop jar aggregation.jar org.myorg.aggregation input_aggregation output_aggregation

rm ${RES_FILE}

hdfs dfs -getmerge output_aggregation ${RES_FILE}

