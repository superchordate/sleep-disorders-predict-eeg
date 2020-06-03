# move CSVs to HDFS (should already be done).
hdfs dfs -put /project2/msca/bchamberlain/bigdata-2020-project/csv project
hdfs dfs -put /project2/msca/bchamberlain/bigdata-2020-project/out project

# list CSVs:
hdfs dfs -ls /user/bchamberlain/project/csv

# file size:
hdfs dfs -du -h /user/bchamberlain/project

