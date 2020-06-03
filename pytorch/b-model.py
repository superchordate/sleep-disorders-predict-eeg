import torch
from torch.autograd import Variable
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential, MaxPool1d, Module, Softmax, BatchNorm1d, Dropout, Conv1d, Sigmoid
from torch.optim import Adam, SGD

# https://www.analyticsvidhya.com/blog/2019/10/building-image-classification-models-cnn-pytorch/
# see more complicated eeg at https://github.com/aliasvishnu/EEGNet/blob/master/EEGNet-PyTorch.ipynb
# more at https://github.com/topics/eeg-classification
class Net(Module):
    def __init__(self):
        super(Net, self).__init__()

        self.cnn_layers = Sequential(
                
            # convolutional layer
            Conv1d(in_channels = 9, out_channels = 1, kernel_size = 50, stride = 5, padding = 1),
            BatchNorm1d(num_features = 1),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 10, stride = 3),
            Dropout(.5),
                
            # convolutional layer
            Conv1d(in_channels = 1, out_channels = 8, kernel_size = 50, stride = 5, padding = 1),
            BatchNorm1d(num_features = 8),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 100, stride = 10),
            Dropout(.5),
            
            # convolutional layer
            Conv1d(in_channels = 8, out_channels = 4, kernel_size = 50, stride = 1, padding = 0),
            BatchNorm1d(num_features = 4),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 10, stride = 3),
            Dropout(.5),
            
            # final convolutional layer to compress to 2 channels (the number of possible classes).
            Conv1d(in_channels = 4, out_channels = 2, kernel_size = 10, stride = 1, padding = 0),
            #BatchNorm1d(num_features = 2),
            
            # linear to map to our 1 output.
            # sigmoid will create output between 0 and 1
            Linear(in_features = 13, out_features = 1),
            Sigmoid(),
        )
        
    # Defining the forward pass
    def forward(self, x):
        x = self.cnn_layers(x)
        return x
    
net = Net()
criterion = CrossEntropyLoss()
optimizer = Adam(net.parameters())
if torch.cuda.is_available():
    net = net.cuda()
    criterion = criterion.cuda()
    

# CUDA for PyTorch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.backends.cudnn.benchmark = True
max_epochs = 3 # should be 70%.

for epoch in range(max_epochs + 1):
    
    i = 0
    
    # Training
    for local_batch, local_labels, file in train:

        i += 1
        local_labels = local_labels.view(local_labels.size(0), 1)
        
        if torch.cuda.is_available():
            local_batch = local_batch.cuda()
            local_labels = local_labels.cuda()

        # Model computations
        optimizer.zero_grad()
        outputs = net(local_batch)
        loss = criterion(outputs, local_labels)
        loss.backward()
        optimizer.step()
        
        # print statistics
        # prediction is the index of hte maximum.
        predictions = np.array([int(i) for i in outputs.max(dim = 1)[1]])
        labels = np.array([int(i) for i in local_labels])
        
        #if any(~np.isin(predictions, [0,1])): raise Exception('bad prediction')
        
        print(
            'epoch %s; batch %s of %s; true: %s of %s; loss: %s; train accuracy: %s' % (
            epoch, 
            i, len(train), 
            sum(labels), len(labels),
            round(loss.item(), 3),
            round(np.mean(labels == predictions),2)
        ))
        
        del local_batch, local_labels, predictions, labels, file
        
    # Check validation set after each epoch.
    for local_batch, local_labels, file in validate:
        
        if torch.cuda.is_available():
            local_batch = local_batch.cuda()
            local_labels = local_labels.cuda()
        
        local_labels = local_labels.view(local_labels.size(0), 1)
        outputs = net(local_batch)
        predictions = np.array([int(i) for i in outputs.max(dim = 1)[1]])
        labels =  np.array([int(i) for i in local_labels])
        
        if any(~np.isin(predictions, [0,1])): raise Exception('bad prediction')
        
        print(
            'true: %s of %s; test accuracy: %s' % (
            sum(labels), len(labels),
            round(np.mean(labels == predictions),2)
        ))
        
        del local_batch, local_labels, predictions, labels
    