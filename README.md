## Reading Files

### .edf

Reading the EEG signals is a bit tricky. Spark can't read them directly. There are 2 python packages that do an OK job: `mne` and `pyedflib`. 
Examples are provided here for each as Jupyter notebooks. To use them, download the referenced file to a data/folder and run them, or just view them on GitHub.

`pyedflib` seems to be better, we'll probably need to use it to read the files, convert them to flat files, and then we can read them into spark or anywhere. 

Some files may be corrupted. For example, I wasn't able to read `brux1.edf`. I suggest we drop any corrupted files. Files are much larger after reading though (the file I read went from 484 Mb to 17 Gb) so we'll have plenty data left after removing anything that is problematic.

### .edf.st

I'm not sure what these are. If you have time, please investigate this.

### Other Formats

.m are Matlab scripts and .txt are events extracted. For simplicity, I suggest we ignore these files and focus and building a CNN on the .edf files.

## Links

* [Files in Hue](https://hadoop.rcc.uchicago.edu:8888/hue/filebrowser/view=%2Fuser%2Fbchamberlain#/user/bchamberlain/sleep/files/capslpdb/1.0.0) (Requires VPN)
* [Data Source & Documentation](https://www.physionet.org/content/capslpdb/1.0.0/)
* [Google Drive](https://drive.google.com/drive/u/0/folders/18ekfirfShLYpxpLoBYhQiKe25c-XYSJO)

To load the data to HDFS, I used: `wget -r -N -c -np https://physionet.org/files/capslpdb/1.0.0/ | zcat | hdfs dfs -put -/user/$USER/data/sleep`
