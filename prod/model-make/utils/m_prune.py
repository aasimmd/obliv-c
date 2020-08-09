import tempfile
import os
import numpy as np
import tensorflow_model_optimization as tfmot
import tensorflow as tf


tf.keras.backend.set_floatx('float64')

def normal_prune_whole(model, epochs, batch_size, sparsity, x_train, y_train):
    
    prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude

    # 10% of training set will be used for validation set
    validation_split = 0.1  

    train_size = x_train.shape[0] * (1 - validation_split)
    end_step = np.ceil(train_size / batch_size).astype(np.int32) * epochs

    pruning_params = {'pruning_schedule' : tfmot.sparsity.keras.PolynomialDecay(initial_sparsity=0.00, final_sparsity=sparsity[0], begin_step=0, end_step=end_step) }

    model_for_pruning = prune_low_magnitude(model, **pruning_params)

    model_for_pruning.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

    logdir = tempfile.mkdtemp()

    callbacks = [tfmot.sparsity.keras.UpdatePruningStep(),tfmot.sparsity.keras.PruningSummaries(log_dir=logdir), ]

    try:
        history = model_for_pruning.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=validation_split, verbose=0)

    except (RuntimeError, tf.errors.InvalidArgumentError) as e:
        history = model_for_pruning.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=validation_split, verbose=0, callbacks=callbacks)
    
    return model_for_pruning


def normal_prune_per_layer(model, epochs, batch_size, sparsity_per_layer, nodes_per_layer, activation_func, x_train, y_train):
    
    prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude

    # 10% of training set will be used for validation set
    validation_split = 0.1

    train_size = x_train.shape[0] * (1 - validation_split)
    end_step = np.ceil(train_size / batch_size).astype(np.int32) * epochs

    layer_pruning_params = []

    for i in range(len(nodes_per_layer)):
        layer_pruning_params.append({'pruning_schedule' : tfmot.sparsity.keras.PolynomialDecay(initial_sparsity=0.00, final_sparsity=sparsity_per_layer[i], begin_step=0, end_step=end_step)})

    model_layers = []

    for i in range(len(nodes_per_layer)):
        if(i != (len(nodes_per_layer)-1)):
            model_layers.append(prune_low_magnitude(tf.keras.layers.Dense(nodes_per_layer[i], activation=activation_func), **layer_pruning_params[i]))
        else:
            model_layers.append(prune_low_magnitude(tf.keras.layers.Dense(nodes_per_layer[i] ), **layer_pruning_params[i]))



    model_for_pruning = tf.keras.models.Sequential(model_layers)

    model_for_pruning.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

    logdir = tempfile.mkdtemp()

    callbacks = [ tfmot.sparsity.keras.UpdatePruningStep(), tfmot.sparsity.keras.PruningSummaries(log_dir=logdir), ]

    try:
        history = model_for_pruning.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=validation_split, verbose=2)

    except (RuntimeError, tf.errors.InvalidArgumentError) as e:
        history = model_for_pruning.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=validation_split, callbacks=callbacks, verbose=2)
    
    return model_for_pruning


def remove_weights(model, percentage_per_layer, pruned_per_layer = True):

    weights = []
    biases = []

    if(pruned_per_layer):
        for i in range(0, len(model.weights), 5):
            weights.append(model.get_weights()[i])
            biases.append(model.get_weights()[i+1])
    else:
        for i in range(0, len(model.weights), 6):
            weights.append(model.get_weights()[i])
            biases.append(model.get_weights()[i+1])

    for i in range(len(weights)-1, 0, -1):
        zeros_count_layer = []
        for j in range(weights[i-1].shape[1]):
            zeros_count_layer.append(np.count_nonzero(weights[i-1][:,j]==0))
        
        zeros_count_layer_indices = np.argsort(zeros_count_layer)

        layer_indices_to_del = zeros_count_layer_indices[-(int(len(zeros_count_layer_indices)* percentage_per_layer[i-1])):]

        weights[i] = np.delete(weights[i], layer_indices_to_del, axis=0)

        weights[i-1] = np.delete(weights[i-1], layer_indices_to_del, axis=1)
        
        biases[i-1] = np.delete(biases[i-1], layer_indices_to_del)

    return weights, biases
