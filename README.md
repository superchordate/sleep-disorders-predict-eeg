This is code from a project I did during my Masters degree to predict sleep disorders from EEG data. We were able to predict Bruxism (teeth griding) with almost 100% accuracy. 

For the most part, you won't be able to run this code. You might find the pytorch scripts interesting though. If you would like to run this, let me know and I'll try to track the data down for you. 

# Reading Files

**.edf**

Reading the EEG signals is a bit tricky. Spark can't read them directly. There are 2 python packages that do an OK job: `mne` and `pyedflib`. `pyedflib` seems to be better, you'll probably need to use it to read the files, convert them to flat files, and then we can read them into spark or anywhere. 

Examples are provided here for each as Jupyter notebooks. To use them, download the referenced file to a data/folder and run them, or just view them on GitHub.

Some files may be corrupted. For example, I wasn't able to read `brux1.edf`. I suggest we drop any corrupted files. Files are much larger after reading (the file I read went from 484 Mb to 17 Gb) so we'll have plenty data left after removing anything that is problematic.

**.m**

.m files are Matlab scripts and .txt are events extracted. For simplicity, we have ignored these files and focus and built a CNN (Convolutional Neural Network) on the .edf files.

# Links

* [Data Source & Documentation](https://www.physionet.org/content/capslpdb/1.0.0/)
* [Google Drive](https://drive.google.com/drive/u/0/folders/18ekfirfShLYpxpLoBYhQiKe25c-XYSJO) (most people won't have access to this).

To load the data to HDFS (Hadoop), I used: `wget -r -N -c -np https://physionet.org/files/capslpdb/1.0.0/ | zcat | hdfs dfs -put -/user/$USER/data/sleep`

`tr -d '\\r' 'convert-to-csv.sbatch' 'convert-to-csv.sbatch'`

