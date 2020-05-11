cd /scratch/midway2/bchamberlain/bigdata-2020-project/
git pull
rm -R log
mkdir log
sbatch tocsv.sbatch -N1 -n1

# aliases we can use.
alias err='cat /scratch/midway2/bchamberlain/bigdata-2020-project/log/edf2csv.err'  
alias out='cat /scratch/midway2/bchamberlain/bigdata-2020-project/log/edf2csv.out'
alias csv='ls -ls /scratch/midway2/bchamberlain/bigdata-2020-project/csv'  
alias done='ls /scratch/midway2/bchamberlain/bigdata-2020-project/csv | grep "done"'

watch squeue -u bchamberlain

# clear output:
# rm -R /scratch/midway2/bchamberlain/bigdata-2020-project/csv

cd /scratch/midway2/bchamberlain/bigdata-2020-project/
git pull
sbatch fileinfo.sbatch
watch squeue -u bchamberlain
