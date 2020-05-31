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
            Conv1d(in_channels = 9, out_channels = 18, kernel_size = 100, stride = 50, padding = 0),
            #BatchNorm1d(num_features = 18),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 100, stride = 50),
            # convolutional reduce 9 channels to 4
            Conv1d(in_channels = 18, out_channels = 2, kernel_size = 100, stride = 50, padding = 0),
            #BatchNorm1d(num_features = 2),
            ReLU(inplace = True),
            MaxPool1d(kernel_size = 10, stride = 5),
            Linear(in_features = 3, out_features = 1),
        )
        
    # Defining the forward pass
    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        return x
    
net = Net()
criterion = CrossEntropyLoss()
optimizer = Adam(net.parameters())
    

# CUDA for PyTorch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.backends.cudnn.benchmark = True
max_epochs = 100
        
# Loop over epochs
for epoch in range(max_epochs):
    
    i = 0
    
    # Training
    for local_batch, local_labels in dataloader:

        i += 1
        
        # Transfer to GPU
        # breaks
        #local_batch, local_labels = local_batch.to(device), local_labels.to(device)

        # Model computations
        optimizer.zero_grad()
        outputs = net(local_batch)
        loss = criterion(outputs, local_labels)
        loss.backward()
        optimizer.step()
        
        # print statistics
        print('epoch %s; %s of %s; loss: %s' % (epoch, i, len(dataloader), loss.item()))
        #running_loss += loss.item()
        #if i % 2000 == 1999:    # print every 2000 mini-batches
        #print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
        #running_loss = 0.0