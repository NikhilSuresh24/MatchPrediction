import os
import numpy as np
import torch
import torch.nn as nn

import pyro
from pyro.distributions import Normal
from pyro.infer import SVI, Trace_ELBO
from pyro.optim import Adam
# for CI testing
smoke_test = ('CI' in os.environ) # is there a CI path 
pyro.enable_validation(True)

#Bayesian Regression code adapted from http://pyro.ai/examples/bayesian_regression.html

#set up of unit normal priors
mean = torch.zeros((1,1)) 
sd = torch.ones((1,1))
prior = Normal(mean, sd)

#create distribution of regressors from prior
regressor_distribution = pyro.random_module("regression_module", regression_model, prior)
#sample a regressor from the distribution
sampled_regressor = regressor_distribution() 

def model(data, input_size):
    weight_mean, weight_sd = torch.zeros((36, 1)), 10 * torch.ones((36, 1)) 
    bias_mean, bias_sd = torch.zeros(1), 10 * torch.ones(1)
    w_prior = Normal(weight_mean, weight_sd)
    b_prior = Normal(bias_mean, bias_sd)
    priors = {'linear.weight': w_prior, 'bias': b_prior}

    priors_distribution = pyro.random_module("module", regression_model, priors)
    sampled = priors_distribution()
    
        



X = np.load("matchData.npz")['x']
y = np.load("matchData.npz")['y']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)