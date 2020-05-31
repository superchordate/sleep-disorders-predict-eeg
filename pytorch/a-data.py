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
        x = x.iloc[range(50000, x.shape[0]-50000), ]
        x = StandardScaler().fit_transform(x)
        
        y = (1 if re.match('.+' + self.disorder, self.files[idx]) else 0)
        
        x = torch.tensor(np.transpose(np.array(x))).float()
        y = torch.tensor(np.array(y)).long()  

        return x, y

# I get errors whenever I set num_workers != 0
usecores = multiprocessing.cpu_count() - 1

dataset = EEGDataset('train', 'nfle')
dataloader = DataLoader(
    # I've moved all the 128 files into the train/ folder, but you can use a different folder if you like.
    # the folder should contain all the parquet files.
    dataset, 
    #batch_size = int(round(len(dataset)/10,0)), 
    batch_size = 10, 
    shuffle = True, num_workers = 0
)
