# set up workspace.
import pandas as pd
import numpy as np
from pyedflib import highlevel # https://github.com/holgern/pyedflib
import os, re, sys

taskid = int(sys.argv[1])

edfpath = '/project2/msca/bchamberlain/bigdata-2020-project/edf/'
outpath = '/project2/msca/bchamberlain/bigdata-2020-project/edfinfo/'

hasfiles = [re.search('^([^.]+)[.]', i).group(1) for i in os.listdir(edfpath) if re.match('.+[.]edf$', i)]
startedfiles = np.unique([re.search('^(.+)-started$', i).group(1) for i in [i for i in os.listdir(outpath) if re.search('^(.+)-started$', i)]])
okfiles = [i for i in hasfiles if i not in startedfiles]

if(len(okfiles) > taskid + 1):

    dofile = okfiles[taskid]

    try:

        with open(outpath + dofile + "-started","w") as file:
            file.write("task-" + str(taskid) + " \n")

        filepath = edfpath + dofile + '.edf'
        signals, signal_headers, header = highlevel.read_edf(filepath)

        info = pd.DataFrame(signal_headers)
        info['rowcount'] = [len(signals[i]) for i in range(len(signals))]
        info['file'] = dofile

        info.to_csv(outpath + dofile + '-info.csv', index = False)
                
    except:

        with open(outpath + dofile + "err", "w") as file:
            file.write(str(sys.exc_info()) + "Done \n") 