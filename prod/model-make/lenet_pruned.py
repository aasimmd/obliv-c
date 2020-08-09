from utils.m_build import *
from utils.m_prune import *
from utils.extra import *

import tensorflow as tf
import numpy as np

#####################################################################################################################################################
#Parameters to change: 
nodes_per_layer = [300, 100, 10]
base_model_epochs = 8
activation_function = 'sigmoid'
jump = 1e+4
activations = [1, 1, 0]
pruned_model_epochs = 6
pruning_batch_size = 128
sparsity = [0.92, 0.91, 0.74]
percentage_weights_to_remove = [0.70, 0.70]
prune_per_layer = True
#####################################################################################################################################################


# Building and training pruned model

with open('processed_data/lenet_train_data_pca.npz', 'rb') as red:
  data = np.load(red)
  x_train = data['features']
  y_train = data['labels']

with open('processed_data/lenet_test_data_pca.npz', 'rb') as red:
  data = np.load(red)
  x_test = data['features']
  y_test = data['labels']


model = build_model(nodes_per_layer, activation_function)

model = train(model, base_model_epochs, x_train, y_train)

base_model_accuracy, _ = test(model, x_test, y_test)

pruned_model = normal_prune_per_layer(model, pruned_model_epochs, pruning_batch_size, sparsity, nodes_per_layer, activation_function, x_train, y_train)

pruned_model_accuracy, _ = test(pruned_model, x_test, y_test)

new_weights,new_biases = remove_weights(pruned_model, percentage_weights_to_remove, prune_per_layer)

with open("datfiles/pruned_lenet_float_inputs.dat", "w") as wire:
    write_inputs(wire,x_test)

with open("datfiles/pruned_lenet_int_inputs.dat", "w") as wire:
    x_slice = approx_inputs(x_test, jump)
    write_inputs(wire,x_slice)

with open("datfiles/pruned_lenet_float_weights.dat", "w") as wire:
    write_params(wire,new_weights,new_biases, activations)

with open("datfiles/pruned_lenet_int_weights.dat", "w") as wire:
    final_weights, final_biases = approx_params(new_weights, new_biases, jump)
    write_params(wire,final_weights,final_biases, activations)
