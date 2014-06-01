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

hdfs dfs -rm -r output_matchups

RES_FILE=results_matchups.txt

sh compile.sh matchup matchup.java

# Run Hadoop
hadoop jar matchup.jar org.myorg.matchup input/flat_games output_matchups

rm ${RES_FILE}

hdfs dfs -getmerge output_matchups ${RES_FILE}

