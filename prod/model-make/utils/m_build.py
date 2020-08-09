import numpy as np
import tensorflow as tf

def build_model(nodes_per_layer, activation_func):
    model_layers = []
    
    for i in range(len(nodes_per_layer)):
        if(i != (len(nodes_per_layer)-1)):
            model_layers.append(tf.keras.layers.Dense(nodes_per_layer[i], activation=activation_func))
            model_layers.append(tf.keras.layers.Dropout(0.3))
    
    model_layers.append(tf.keras.layers.Dense(nodes_per_layer[len(nodes_per_layer)-1]))

    model = tf.keras.models.Sequential(model_layers)

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])

    return model


def train(model, epochs, x_train, y_train):
    history = model.fit(x_train, y_train, epochs=epochs, verbose=0)
    
    return model


def test(model, x_test, y_test):
    model_test_loss , model_test_accuracy = model.evaluate(x_test,  y_test, verbose=0)
    
    return model_test_accuracy, model_test_loss 

