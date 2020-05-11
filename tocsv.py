# set up workspace.
import pandas as pd
import numpy as np
from pyedflib import highlevel # https://github.com/holgern/pyedflib
import glob, os, pickle, re, sys, multiprocessing, random, platform, resource
from joblib import Parallel, delayed

if platform.system() == 'Linux':
    savetopath = '/project2/msca/bchamberlain/bigdata-2020-project/csv/'
    if not os. path. isdir(savetopath): os.mkdir(savetopath)
    os.chdir('/project2/msca/bchamberlain/bigdata-2020-project/')
    #soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    #resource.setrlimit(resource.RLIMIT_AS, (14000, hard))
else:
    os.chdir('.')
    savetopath = 'csv/' 

ncores = multiprocessing.cpu_count()
hasfiles = [re.search('^([^.]+)[.]', i).group(1) for i in os.listdir('edf') if re.match('.+[.]edf$', i)]
donefiles = np.unique([re.search('^(done|err)-(.+$)', i).group(2) for i in [i for i in os.listdir(savetopath) if re.search('^(done|err)-(.+$)', i)]])
dofiles = [i for i in hasfiles if i not in donefiles]

#dofiles = np.random.choice(dofiles, size=10, replace=False)
if len(dofiles) >= 10:
    dofiles = np.random.choice(dofiles, size=10, replace=False)

# function to convert and EDF file to multiple CVS.
def edf2csv(fileid):
    
    try:

        global savetopath
    
        filepath = 'edf/' + fileid + '.edf'
        #print('Reading: ' + filepath)
        signals, signal_headers, header = highlevel.read_edf(filepath)
    
        signal_headers = pd.DataFrame(signal_headers)
        signal_headers.to_csv(savetopath + fileid + '-headers.csv')
        
        for irate in signal_headers.sample_rate.unique():
    
            #print('Building: ' + fileid + '-' + str(irate))
            isignals = [i for i in range(len(signals)) if signal_headers.sample_rate[i] == irate]
            x = pd.DataFrame()
    
            for i in isignals:
                x[ signal_headers.label[i] ] = signals[i]            
    
            filepath = savetopath + 'signal-' + str(irate) + '-' + fileid + '.csv'
            #x.head().to_csv(filepath)
            x.to_csv(filepath)
    
            print('Finished: ' + fileid)
            with open(savetopath + "done-" + fileid,"w") as file:
                file.write("Done \n") 
                
    except:
        
        print('Failed: ' + fileid + ': ' + str(sys.exc_info()))
        with open(savetopath + "err-" + fileid + '.txt', "w") as file:
            file.write(str(sys.exc_info()) + "Done \n") 
        

Parallel(n_jobs = ncores)(delayed(edf2csv)(i) for i in dofiles)

print('DONE')