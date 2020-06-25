## Neural network feed forward
The weights and the structure of the model is in weights.dat  
The input data is in inputs.dat
Make standalone neural-network as (need to change weights for this)
```
gcc -Wall ogneural.c -o neuralnet
```
and run
```
./neuralnet
```
(check below for oblivious neural network)

### Structure of weights
l -> No of layers  
// l entries below like this
m n -> dimensions of weights, m: no of neurons in previous layer, n: no of neurons in current layer  
// m rows below, with n entries each  
n values : The bias vector for the current layer  
a -> The activation function  
The activation functions available now are:  
0. None
1. Relu

### Structure of inputs
x, t -> x: No of inputs, t: No of values per input  
// x entries below  
t values for the input vector

## Oblivious neural network 
run
```
make
```
Execute ```./a.out localhost:8090 1``` on server  
And  
Execute ```./a.out localhost:8090 2``` on client  
Currently it fetches values from weights.dat and inputs.dat