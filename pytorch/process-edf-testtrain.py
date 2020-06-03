# set up workspace.
import pandas as pd
import numpy as np
import glob, os, pickle, re, sys, multiprocessing, random, platform
from joblib import Parallel, delayed
import pyarrow as pa
import pyarrow.parquet as pq
import pyedflib

dofiles = pd.read_csv('../out/selected-files.csv').file.values

# for testing, we want 5 with disorder and 5 without
disorder = 'nfle'
files_disorder = np.array([i for i in dofiles if re.match(disorder, i)])
files_other = np.array([i for i in dofiles if not re.match(disorder, i)])

# validation files.
validatefiles = np.concatenate((
    files_disorder[ np.random.choice(range(len(files_disorder)), 3, replace = False) ],
    files_other[ np.random.choice(range(len(files_other)), 5, replace = False) ]
))
files_disorder = files_disorder[ ~np.isin(files_disorder, validatefiles)]
files_other = files_other[ ~np.isin(files_other, validatefiles)]

# holdout files.
holdoutfiles = np.concatenate((
    files_disorder[ np.random.choice(range(len(files_disorder)), 3, replace = False) ],
    files_other[ np.random.choice(range(len(files_other)), 5, replace = False) ]
))

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
# file = 'ins1'
def getsignals(file):
    
    if file in validatefiles:
        traintest = 'validate'
    elif file in holdoutfiles:
        traintest = 'holdout'
    else:
        traintest = 'train'
    
    edf = pyedflib.EdfReader(edfpath + file + '.edf')
    
    info = pd.DataFrame({
        'label': edf.getSignalLabels(),
        'sample_rate': edf.getSampleFrequencies()
    })
    info['freq_index'] = range(info.shape[0])
    info = info.merge(dosignals, on = 'label')
    
    #for isample_rate in info.choose_sample_rate.unique():
    for isample_rate in [128]:
        
        df = pd.DataFrame()
        
        for index, row in info[info.choose_sample_rate == isample_rate].iterrows():

            everyrow = int(row.sample_rate / row.choose_sample_rate)
            df[row.label] = edf.readSignal(row.freq_index)[0::everyrow][0:row.groupminrowcount]
                
        # take 50 random cuts length 100000.
        cutsize = 100 * 1000
        cutcount = 20
        for i in range(cutcount):
            
            startat = random.randint(0, df.shape[0] - cutsize - 1)
            cut = df.iloc[startat:(startat+cutsize ), ]
            if cut.shape[1] != 9:
                raise Exception('bad size at ' + file)
                
            pq.write_table(pa.Table.from_pandas(cut), '../pytorch/splits/' + traintest + '/' + file + '-' + str(isample_rate) + '-' + str(i) + '.parquet')
    

Parallel(n_jobs = usecores)(delayed(getsignals)(i) for i in dofiles)
