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

hdfs dfs -rm -r -f output_aggregation_2

RES_FILE=results_aggregation_2.txt

sh compile.sh aggregation aggregation.java

# Run Hadoop
hadoop jar aggregation.jar org.myorg.aggregation input_aggregation_2/flat_games_all_2 output_aggregation_2

rm ${RES_FILE}

hdfs dfs -getmerge output_aggregation_2 ${RES_FILE}

