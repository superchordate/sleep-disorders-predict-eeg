import platform, os, re, multiprocessing
import pandas as pd
from joblib import Parallel, delayed

ncores = multiprocessing.cpu_count()
    
if platform.system() == 'Linux':
    savetopath = '/scratch/midway2/bchamberlain/bigdata-2020-project/csv/'
    if not os. path. isdir(savetopath): os.mkdir(savetopath)
    os.chdir('/scratch/midway2/bchamberlain/bigdata-2020-project/')
    usecores = ncores - 2
else:
    os.chdir('.')
    savetopath = 'csv/' 
    usecores = ncores - 2

dofiles = [i for i in os.listdir(savetopath) if re.search('^signal-', i)]

def getinfo(file):
    
    global savetopath
        
    dt = pd.read_csv(savetopath + file)
    
    return {
        'file': file,
        'fileid': re.search('^signal-[0-9]+-([^-]+)[.]', file).group(1),
        'freq': re.search('^signal-([0-9]+)', file).group(1),
        'rows': dt.shape[0],
        'cols': dt.shape[1],
        'size_gb': round(os.path.getsize(savetopath + file)/(1024*1024*1024),2)
    }    
    

fileinfo = pd.DataFrame(
    Parallel(n_jobs = usecores)(delayed(getinfo)(i) for i in dofiles)
)
fileinfo.to_csv('log/file-info.csv')
