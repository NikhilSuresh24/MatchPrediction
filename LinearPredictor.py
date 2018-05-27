import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch import optim

from tqdm import tqdm
from sklearn.model_selection import train_test_split
import random
import math
import operator
import matplotlib.pyplot as plt
import numpy as np
use_cuda = torch.cuda.is_available()

#from https://discuss.pytorch.org/t/list-of-nn-module-in-a-nn-module/219/2
class ListModule(nn.Module):
    def __init__(self, *args):
        super(ListModule, self).__init__()
        idx = 0
        for module in args:
            self.add_module(str(idx), module)
            idx += 1

    def __getitem__(self, idx):
        if idx < 0 or idx >= len(self._modules):
            raise IndexError('index {} is out of range'.format(idx))
        it = iter(self._modules.values())
        for i in range(idx):
            next(it)
        return next(it)

    def __iter__(self):
        return iter(self._modules.values())

    def __len__(self):
        return len(self._modules)

class Net(nn.Module):
    def __init__(self, input_size : int, hidden_sizes : list):
        super(Net, self).__init__()
        self.input_size = input_size
        hidden_sizes.append(1)
        self.hidden_sizes = hidden_sizes
        self.num_hidden = len(hidden_sizes)
        layers = []

        for idx, val in enumerate(self.hidden_sizes):
            layers.append(nn.Linear(self.input_size, val) if idx == 0 else nn.Linear(self.hidden_sizes[idx - 1], val))

        self.layers = ListModule(*layers)
    
    def forward(self, input):
        res = F.relu(self.layers[0](input))
        for idx, layer in enumerate(self.layers):
            if idx != 0:
                res = F.relu(layer(res))
        return res

def train(net, optimizer, criterion, X, y, num_epochs=1, print_every=500):  
    for epoch in range(num_epochs):
        for idx, val in enumerate(X):
            optimizer.zero_grad() #init gradient to 0
            prediction = net(Variable(torch.from_numpy(val).float()))
            loss = criterion(prediction, Variable(torch.FloatTensor([y[idx]])))
            loss.backward(retain_graph=True) #backpropagation
            optimizer.step() #apply gradients to weights

            if idx % print_every == 0:
                print("epoch %d/%d iteration %d/%d loss: %d" % (epoch, num_epochs, idx, X.shape[0], loss.item()))
    
    return loss.item()

def test(net, X, y, criterion, isBaseMetric=False):
    loss = 0
    for idx, val in tqdm(enumerate(X)):
        prediction = net(Variable(torch.from_numpy(val).float()))
        avg_score = np.array(np.sum(y)/y.shape[0])
        loss +=  criterion(Variable(torch.from_numpy(avg_score).float()), Variable(torch.FloatTensor([y[idx]]))) if isBaseMetric else criterion(prediction, Variable(torch.FloatTensor([y[idx]])))

    loss_avg = loss.item()/len(X)
    return loss_avg
    
X = np.load("matchData.npz")['x']
y = np.load("matchData.npz")['y']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
input_size = 36
hidden1 = 20
hidden2 = 8
hidden3 = 2
hidden = [hidden1, hidden2, hidden3]
net = Net(input_size, hidden)
optimizer = optim.Adam(net.parameters())
criterion = nn.MSELoss()
final_loss = train(net, optimizer, criterion, X_train, y_train)
baseMetric = test(net, X_test, y_test, criterion, True)
loss_avg = test(net, X_test, y_test, criterion)
print(baseMetric, loss_avg)
torch.save(net, 'netweights.pt')
    