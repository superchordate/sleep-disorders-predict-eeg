from torch.utils.data import Dataset, DataLoader
import os, re
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import multiprocessing

class EEGDataset(Dataset):

    def __init__(self, root_dir, disorder):
        self.files = [root_dir + '/' + x for x in os.listdir(root_dir) if re.match('.+128', x)]
        self.root_dir = root_dir
        self.disorder = disorder

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        x = pd.read_parquet(self.files[idx])
        if x.shape[1] != 9: raise Exception('bad shape at ' + self.files[idx])
        # 3133440 x 9
        #x = x.iloc[range(4000, x.shape[0]-500000), ]
        x = StandardScaler().fit_transform(x)
        
        y = (1 if re.match('.+' + self.disorder, self.files[idx]) else 0)
        
        x = torch.tensor(np.transpose(np.array(x))).float()
        y = torch.tensor(np.array(y)).long()  

        return x, y, self.files[idx]

# I get errors whenever I set num_workers != 0
usecores = multiprocessing.cpu_count() - 1

disorder = 'nfle'
train = EEGDataset('splits/train', disorder )
train = DataLoader(
    # I've moved all the 128 files into the train/ folder, but you can use a different folder if you like.
    # the folder should contain all the parquet files.
    train, 
    #batch_size = int(round(len(dataset)/10,0)), 
    batch_size = 32, 
    shuffle = True, num_workers = 0
)

validate = EEGDataset('splits/validate', disorder )
validate = DataLoader(
    validate, 
    batch_size = len(validate), shuffle = False, num_workers = 0
)

holdout = EEGDataset('splits/holdout', disorder )
holdout = DataLoader(
    holdout, 
    batch_size = len(holdout), shuffle = False, num_workers = 0
)
