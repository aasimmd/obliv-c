# Presentation ready code

## TODO:
1. Take more CLAs from oblivc, reduce compilation
2. Get PCA matrix and dataset
3. Change input procedure to depend only on projection matrix
4. Make large python file (lpf) that handles all connections.
5. Connect lpf with web-app

## Info:
The structure of the data directory is:  
```
.
├── inputs
│   ├── isolet
│   │   ├── projection-matrix.npy
│   │   ├── v0-float.dat
│   │   ├── v0-int.dat
│   │   ├── v0-pruned-float.dat
│   │   └── v0-pruned-int.dat
│   ├── lenet
│   │   ├── projection-matrix.npy
│   │   ├── v0-float.dat
│   │   └── ...
│   └── sports
│       └── ...
└── weights
    ├── isolet
    │   ├── v0-float.dat
    │   └── ...
    ├── lenet
    │   ├── v0-float.dat
    │   └── ...
    └── sports
        └── v0-pruned-xs-float.dat
```
The file names are of the format **version**-**dtype**.dat  
The projection matrices required to prep the inputs are also present.

## Usage:
1. Run the server, for example:  
`python3 server.py int isolet v0-pruned`
2. Run the client, for example:  
`python3 client.py int isolet v0-pruned`  

The structure is `<python> [server/client] dtype nntype version`