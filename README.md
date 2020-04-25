## Links

* [Files in Hue](https://hadoop.rcc.uchicago.edu:8888/hue/filebrowser/view=%2Fuser%2Fbchamberlain#/user/bchamberlain/sleep/files/capslpdb/1.0.0) (Requires VPN)
* [Data Source & Documentation](https://www.physionet.org/content/capslpdb/1.0.0/)
* [Google Drive](https://drive.google.com/drive/u/0/folders/18ekfirfShLYpxpLoBYhQiKe25c-XYSJO)

To load the data to HDFS, I used: `wget -r -N -c -np https://physionet.org/files/capslpdb/1.0.0/ | zcat | hdfs dfs -put -/user/$USER/data/sleep`
