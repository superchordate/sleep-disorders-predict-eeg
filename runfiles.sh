# convert to
alias err='cat /project2/msca/bchamberlain/bigdata-2020-project/log/edf2csv.err'  
alias out='cat /project2/msca/bchamberlain/bigdata-2020-project/edf2csv.out'
alias csv='ls -ls /project2/msca/bchamberlain/bigdata-2020-project/csv'  
alias done='ls /project2/msca/bchamberlain/bigdata-2020-project/csv | grep "done"'
alias run='
cd /project2/msca/bchamberlain/bigdata-2020-project/
git pull
rm -R log
mkdir log
sbatch tocsv/tocsv.sbatch -N1 -n1 -exclusive
watch squeue -u bchamberlain
'
run

# file info
# aliases we can use.
alias err='cat /project2/msca/bchamberlain/bigdata-2020-project/log/fileinfo.err'  
alias out='cat /project2/msca/bchamberlain/bigdata-2020-project/fileinfo.out'
alias run='
cd /project2/msca/bchamberlain/bigdata-2020-project/
git pull
rm -R log
mkdir log
sbatch fileinfo/fileinfo.sbatch -N1 -n1 -exclusive
watch squeue -u bchamberlain
'
run

# edfinfo 
alias err='cat /project2/msca/bchamberlain/bigdata-2020-project/log/edfinfo.err'  
alias out='cat /project2/msca/bchamberlain/bigdata-2020-project/edfinfo.out'
alias run='
cd /project2/msca/bchamberlain/bigdata-2020-project/
git pull
rm -R log
mkdir log
sbatch fileinfo/edfinfo.sbatch
watch squeue -u bchamberlain
'
run