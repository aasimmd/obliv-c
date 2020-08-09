import numpy as np
import pandas as pd
import tensorflow as tf

def prep_isolet():
    df = pd.read_csv('raw_data/isolet_csv.csv')

    df = df.sample(frac=1).reset_index(drop=True)

    Y = df['class']

    Y = Y.str.replace("'" , "")

    Y = np.array(Y)
    Y = Y.astype(float)

    X = df.drop(columns='class')
    
    train_samples = 5000
    
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=train_samples, test_size=2797)

    x_train = np.array(x_train)
    x_test = np.array(x_test)

    x_train = x_train.reshape((5000,-1))
    x_test = x_test.reshape((2797,-1))

    return x_train, x_test, y_train, y_test


def prep_lenet():
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train, x_test = x_train / 255.0, x_test / 255.0

    x_train = x_train.reshape((60000, -1))

    x_test = x_test.reshape((10000, -1))

    return x_train, x_test, y_train, y_test


def prep_sports():
    with open('raw_data/sports-data.npz', 'rb') as red:
        data = np.load(red)
        features = data['features']
        labels = data['labels']

    f = pd.DataFrame(features)

    l = pd.DataFrame(labels)

    l.rename(columns={0:5625})

    df = pd.concat([f,l] , axis=1)

    df = df.sample(frac=1)

    y = df.iloc[:,-1]

    x = df.iloc[:, :-1]

    train_samples = 7500

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=train_samples, test_size=1620)

    x_train = np.array(x_train)
    x_test = np.array(x_test)

    x_train = x_train.reshape((7500,-1))
    x_test = x_test.reshape((1620,-1))

    y_train = np.array(y_train)
    y_test = np.array(y_test)

    x_train = np.tanh(x_train)
    x_test = np.tanh(x_test)

    return x_train, x_test, y_train, y_test

def prep_pca(x_train, x_test, n_comp, name='wonka'):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    # standardizing training data
    scaler.fit(x_train)

    # Apply transform on training and test data
    train_data = scaler.transform(x_train)
    test_data = scaler.transform(x_test)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=n_comp , svd_solver='full')

    pca.fit(train_data)

    train_data = pca.transform(train_data)
    test_data = pca.transform(test_data)

    with open(f'proj-mat-{name}.npy', 'wb') as wire:
        np.save(wire, pca.components_)
    
    print(x_train.shape, 'to', train_data.shape)
    print(x_test.shape, 'to', test_data.shape)

    x_train = train_data
    x_test = test_data

    return x_train, x_test