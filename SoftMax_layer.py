import numpy as np
from math import *

def Softmax(z):
    """Input an vector,
    output its softmax vector.
     """
    exp_sum = sum([exp(z_i) for z_i in z])
    return np.array([exp(z_k)/exp_sum for z_k in z])

def Crossentropy():

