#!/bin/sh

if [ $# -lt 2 ]; then
    echo "usage `basename $0` <Name> <Java file> [<Java file> ...]"
    exit 1
fi

set -e

NAME=$1
shift
FILES=$@
CLASS_DIR=${NAME}-classes
JAR_FILE=${NAME}.jar

module load midway-hadoop

mkdir -p ${CLASS_DIR} 

# Compile
javac -target 1.7 -source 1.7 -Xlint:deprecation -cp "${HADOOP_HOME}/*:${HADOOP}/parcels/CDH/lib/hadoop-mapreduce/*:${HADOOP}/parcels/CDH/lib/hadoop-fs/*:${HADOOP_HOME}/lib/*" -d ${CLASS_DIR} $FILES 

# Package
jar -cvf ${JAR_FILE} -C ${CLASS_DIR} .

echo "Saved ${JAR_FILE}"
