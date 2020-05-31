# set up workspace.
import pandas as pd
import numpy as np
import glob, os, pickle, re, sys, multiprocessing, random, platform
from joblib import Parallel, delayed
import pyarrow as pa
import pyarrow.parquet as pq
import pyedflib

dofiles = pd.read_csv('../out/selected-files.csv').file.values

if platform.system() == 'Linux':
    savetopath = '/project2/msca/bchamberlain/bigdata-2020-project/out/'
    edfpath = '/project2/msca/bchamberlain/bigdata-2020-project/edf/'
else:
    os.chdir('.')
    savetopath = '../out/'
    edfpath = '../edf/'
    # just a few to test.
    #dofiles = dofiles[0:5]

usecores = multiprocessing.cpu_count() - 1
if not os. path.isdir(savetopath): os.mkdir(savetopath)
dosignals = pd.read_csv(savetopath + 'selected-signals.csv')

# function to convert and EDF file to multiple CVS.
# file = dofiles[4]
def getsignals(file):

    edf = pyedflib.EdfReader(edfpath + file + '.edf')
    
    info = pd.DataFrame({
        'label': edf.getSignalLabels(),
        'sample_rate': edf.getSampleFrequencies()
    })
    info['freq_index'] = range(info.shape[0])
    info = info.merge(dosignals, on = 'label')
    
    for isample_rate in info.choose_sample_rate.unique():
        
        df = pd.DataFrame()
        
        for index, row in info[info.choose_sample_rate == isample_rate].iterrows():

            everyrow = int(row.sample_rate / row.choose_sample_rate)
            df[row.label] = edf.readSignal(row.freq_index)[0::everyrow][0:row.groupminrowcount]
            
        pq.write_table(pa.Table.from_pandas(df), '../out/' + file + '-' + str(isample_rate) + '.parquet')
    

reads = Parallel(n_jobs = usecores)(delayed(getsignals)(i) for i in dofiles)
