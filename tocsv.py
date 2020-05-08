import pandas as pd
import numpy as np
from pyedflib import highlevel # https://github.com/holgern/pyedflib
import glob, os, pickle, re, sys
    
datapath = '.' 
savetopath = 'csv/' 
#datapath = '/home/bchamberlain/bigdataproj/'
#savetopath = '/scratch/midway2/bigdataproj/csv/'

os.chdir(datapath)

try:
    doneids = pickle.load(open("doneids", "rb"))
except:
    doneids = []

def edf2csv(fileid):

    global savetopath

    filepath = 'edf/' + fileid + '.edf'
    print('Reading: ' + filepath)
    signals, signal_headers, header = highlevel.read_edf(filepath)

    signal_headers = pd.DataFrame(signal_headers)
    signal_headers.to_csv(savetopath + fileid + '-headers.csv')
    
    for irate in signal_headers.sample_rate.unique():

        print('Building: ' + fileid + '-' + str(irate))
        isignals = [i for i in range(len(signals)) if signal_headers.sample_rate[i] == irate]
        x = pd.DataFrame()

        for i in isignals:
            x[ signal_headers.label[i] ] = signals[i]            

        filepath = savetopath + fileid + '-' + str(irate) + '-signal.csv'
        print('Saving: ' + filepath)
        x.to_csv(filepath)

        print('')

    return fileid


for file in [i for i in os.listdir('edf') if re.match('.+[.]edf$', i)]:
    
    fileid = file.replace('.edf', '')
    
    if fileid not in doneids:
        try:
            doneids.append(edf2csv(file.replace('.edf', '')))
        except:
            print('Failed at: ' + fileid + ': ', sys.exc_info()[0])
            
    pickle.dump(doneids, open("doneids", "wb"))
