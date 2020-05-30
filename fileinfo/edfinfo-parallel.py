# set up workspace.
import pandas as pd
import numpy as np
from pyedflib import highlevel # https://github.com/holgern/pyedflib
import glob, os, pickle, re, sys, multiprocessing, random, platform
 #import resource
from joblib import Parallel, delayed

os.chdir('..')
edfpath = 'edf/'

ncores = multiprocessing.cpu_count()
dofiles = [re.search('^([^.]+)[.]', i).group(1) for i in os.listdir('edf') if re.match('.+[.]edf$', i)]

def edfinfo(dofile):

    try:

        filepath = edfpath + dofile + '.edf'
        signals, signal_headers, header = highlevel.read_edf(filepath)

        info = pd.DataFrame(signal_headers)
        info['rowcount'] = [len(signals[i]) for i in range(len(signals))]
        info['file'] = dofile

        return info
                
    except:

        print(sys.exc_info())

out = Parallel(n_jobs = ncores)(delayed(edfinfo)(i) for i in dofiles)
pd.concat(out).to_csv('../out/edfinfo.csv', index = False)
