import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from tqdm import tqdm
import random
import math
import operator
import matplotlib.pyplot as plt
import numpy as np
use_cuda = torch.cuda.is_available()