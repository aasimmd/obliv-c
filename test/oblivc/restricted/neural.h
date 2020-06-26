// client is party 2
// server is party 1
// client provides the inputs
// server provides the weights
int party_id;

#define weights_file "isolet_weights.dat"
#define inputs_file "isolet_inputs.dat"
#define CORDIC_ITERATIONS 10
// activation function types
// none - 0
// relu - 1
// sigmoid - 2

typedef struct {
    // common information prior computation
    int input_shape, no_inputs;
    int no_layers, **shapes;
    int *activations;

    // common results
    // no_outputs = no_inputs
    int output_shape;
    float **outputs;
} protocolIO;

void read_weights(char *filename, float ****weights, float ***biases, int ***shapes, int *no_layers, int **activations);
void read_inputs(char *filename, float ***inputs, int *input_shape, int *no_inputs);
void neuralnet(void *args);