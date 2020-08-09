import tensorflow as tf 
import numpy as np
import pandas as pd 


def approx_params(weights, biases, jump):
    for i in range((len(weights))):
        weights[i] = (weights[i]*jump).astype("int32")
        biases[i] = (biases[i]*jump).astype("int32")

    return weights, biases

def approx_inputs(x_slice, jump):
    x_slice = (x_slice*jump).astype("int32")
    return x_slice

def write_params(wire, weights, biases, activations):
    n_layers = len(weights)
    wire.write(f'{n_layers}\n')
    for i in range(n_layers):
        wi = weights[i]
        writer = " ".join(map(str, wi.shape))
        wire.write(writer+"\n")
        for wt in wi:
            writer = " ".join(map(str, wt))
            wire.write(writer+"\n")
        bi = biases[i]
        writer = " ".join(map(str, bi))
        wire.write(writer+"\n")
        wire.write(f'{activations[i]}\n')


def write_inputs(wire, x_slice):
    writer = " ".join(map(str, x_slice.shape))
    wire.write(writer+"\n")
    for cut in x_slice:
        writer = " ".join(map(str, cut))
        wire.write(writer+"\n")