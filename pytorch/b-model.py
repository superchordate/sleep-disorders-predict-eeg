import torch
from torch.autograd import Variable
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential, MaxPool1d, Module, Softmax, BatchNorm1d, Dropout, Conv1d
from torch.optim import Adam, SGD

# https://www.analyticsvidhya.com/blog/2019/10/building-image-classification-models-cnn-pytorch/
# see more complicated eeg at https://github.com/aliasvishnu/EEGNet/blob/master/EEGNet-PyTorch.ipynb
# more at https://github.com/topics/eeg-classification
class Net(Module):
    def __init__(self):
        super(Net, self).__init__()

        self.cnn_layers = Sequential(
            # convolutional reduce 9 channels to 4
            Conv1d(in_channels = 9, out_channels = 18, kernel_size = 1000, stride = 350, padding = 0),
            #BatchNorm1d(num_features = 18),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 100, stride = 50),
            # convolutional reduce 9 channels to 4
            Conv1d(in_channels = 18, out_channels = 2, kernel_size = 10, stride = 5, padding = 0),
            #BatchNorm1d(num_features = 2),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 10, stride = 5),
            Linear(in_features = 5, out_features = 1),
            # sigmoid will create output 0-1
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
max_epochs = 100

for epoch in range(max_epochs):
    
    i = 0
    
    # Training
    for local_batch, local_labels in dataloader:

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
        labels =  np.array([int(i) for i in local_labels])
        print(
            'epoch %s; batch %s of %s; true : %s; loss: %s; accuracy: %s' % (
            epoch, i, 
            len(dataloader), 
            sum(labels), 
            round(loss.item(), 3),
            np.mean(labels == predictions)
        ))
        
        #print(labels)
        #print(outputs)
        #print(predictions)
        
        del local_batch, local_labels, predictions, labels