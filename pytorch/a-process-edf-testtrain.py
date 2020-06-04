# set up workspace.
import pandas as pd
import numpy as np
import glob, os, pickle, re, sys, multiprocessing, random, platform
import pyarrow as pa
import pyarrow.parquet as pq
import pyedflib # pip install git+https://github.com/superchordate/pyedflib
from joblib import Parallel, delayed
from glob import glob
              
# options
docuts = False
cutsize = 100 * 1000
cutcount = 20
doparquet = True # False will do CSV

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
# file = 'ins8'

# clear files.
if '.\\holdout\\' in glob("./*/"):
    for i in ['validate', 'holdout', 'train']: 
        for j in os.listdir(i): os.remove(i + '/' + j)
    del i, j
else:
    os.makedir('holdout')
    os.makedir('validate')
    os.makedir('train')

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
        
        if docuts:

            for i in range(cutcount):
                
                startat = random.randint(0, df.shape[0] - cutsize - 1)
                cut = df.iloc[startat:(startat+cutsize ), ]
                if cut.shape[1] != 9:
                    raise Exception('bad size at ' + file)
                    
                if doparquet: 
                    pq.write_table(pa.Table.from_pandas(cut), '../pytorch/' + traintest + '/' + file + '-' + str(isample_rate) + '-' + str(i) + '.parquet')
                else:
                    cut.to_csv('../pytorch/' + traintest + '/' + file + '-' + str(isample_rate) + '-' + str(i) + '.csv', index = False)

        else:

            if doparquet: 
                pq.write_table(pa.Table.from_pandas(df), '../pytorch/' + traintest + '/' + file + '-' + str(isample_rate) + '.parquet')
            else: 
                df.to_csv('../pytorch/' + traintest + '/' + file + '-' + str(isample_rate) + '.csv', index = False)
                
    

Parallel(n_jobs = usecores)(delayed(getsignals)(i) for i in dofiles)
