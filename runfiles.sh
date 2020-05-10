cd /scratch/midway2/bchamberlain/bigdata-2020-project/
git pull
rm -R log
mkdir log
sbatch tocsv.sbatch
watch squeue -u bchamberlain

cat /scratch/midway2/bchamberlain/bigdata-2020-project/log/edf2csv.err 
cat /scratch/midway2/bchamberlain/bigdata-2020-project/log/edf2csv.out

ls /scratch/midway2/bchamberlain/bigdata-2020-project/csv

watch ls /scratch/midway2/bchamberlain/bigdata-2020-project/csv | grep 'done'

# clear output:
# rm -R /scratch/midway2/bchamberlain/bigdata-2020-project/csv

