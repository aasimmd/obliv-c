// client is party 2
// server is party 1
// client provides the inputs
// server provides the weights
int party_id;

#define CORDIC_ITERATIONS 10
// activation function types
// none - 0
// relu - 1
// sigmoid - 2
// tanh - 3

typedef struct {
    // common information prior computation
    int input_shape, no_inputs;
    int no_layers, **shapes;
    int *activations;
    char *weights_file, *inputs_file;

    // common results
    // no_outputs = no_inputs
    int output_shape;
    int **outputs;
} protocolIO;

void read_weights(char *filename, int ****weights, int ***biases, int ***shapes, int *no_layers, int **activations);
void read_inputs(char *filename, int ***inputs, int *input_shape, int *no_inputs);
void neuralnet(void *args);