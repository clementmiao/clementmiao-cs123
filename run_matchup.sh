#!/bin/bash
#SBATCH --job-name=hd
#SBATCH --output=hd.out
#SBATCH --error=hd.err
#SBATCH --nodes=5
#SBATCH --account=cmsc12300
#SBATCH --reservation=cmsc12300lab

module load midway-hadoop

# Remove output directory if it exists
hdfs dfs -rm -r -f output_matchups

RES_FILE=results_matchups.txt

# Run Hadoop
hadoop jar matchup.jar org.myorg.matchup input/flat_games output_matchups

rm ${RES_FILE}

hdfs dfs -getmerge output ${RES_FILE}

