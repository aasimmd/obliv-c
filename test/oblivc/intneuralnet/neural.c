#include<stdio.h>
#include<obliv.h>

#include "neural.h"

int main(int argc, char *argv[])
{
    ProtocolDesc pd;
    protocolIO io;

    if(argc==3)
    {
        const char *remote_host = strtok(argv[1], ":");
        const char *port = strtok(NULL, ":");

        // Make connection between two shells
        // Modified ocTestUtilTcpOrDie() function from obliv-c/test/oblivc/common/util.c
        if(argv[2][0] == '1') {
            if(protocolAcceptTcp2P(&pd,port)!=0) {
                printf("TCP accept from %s failed\n", remote_host);
                exit(1);
            }
        } else {
            if(protocolConnectTcp2P(&pd,remote_host,port)!=0) {
                printf("TCP connect to %s failed\n", remote_host);
                exit(1);
            }
        }
    }
    else
    {
        printf("Incorrect usage\n");
        exit(1);
    }
    // printf("Connection passed\n");

    party_id = (argv[2][0]=='1'? 1 : 2);
    setCurrentParty(&pd, party_id); // only checks for a '1'

    // printf("Starting protocol execution\n");
    execYaoProtocol(&pd, neuralnet, &io);
    cleanupProtocol(&pd);

    // explore the results
    int ox, oy;
    ox = io.no_inputs;
    oy = io.output_shape;
    printf("%d %d\n", ox, oy);
    // printf("Outputs:\n");
    for(int x=0; x<ox; x++)
    {
        for(int y=0; y<oy; y++)
        {
            printf("%f ", io.outputs[x][y]);
        }
        putchar('\n');
    }

    return 0;
}

void read_weights(const char *filename, long long ****weights, long long ***biases, int ***shapes, int *no_layers, int **activations)
{
	FILE *fptr = fopen(filename, "r");
	fscanf(fptr, "%d", no_layers);
	*shapes = calloc(*no_layers, sizeof **shapes);
	*weights = calloc(*no_layers, sizeof **weights);
	*biases = calloc(*no_layers, sizeof **biases);
    *activations = calloc(*no_layers, sizeof **activations);
	for(int l=0; l<*no_layers; l++)
	{
		int m,n;
		(*shapes)[l] = calloc(2, sizeof ***shapes);
		// read dimensions
		fscanf(fptr, "%d %d", &((*shapes)[l][0]), &((*shapes)[l][1]));
		// allocate space for dimensions
		m = (*shapes)[l][0];
		n = (*shapes)[l][1];
		(*weights)[l] = calloc(m, sizeof *((*weights)[l]));
		for(int x=0; x<m; x++)
			(*weights)[l][x] = calloc(n, sizeof *((*weights)[l][x]));
		(*biases)[l] = calloc(n, sizeof *((*biases)[l]));
		// read all inputs
		for(int x=0; x<m; x++)
		{
			for(int y=0; y<n; y++)
			{
				fscanf(fptr, "%lld", &(*weights)[l][x][y]);
			}
		}
		for(int x=0; x<n; x++)
			fscanf(fptr, "%f", &(*biases)[l][x]);
        
        // read the activation function
        fscanf(fptr, "%d", &((*activations)[l]));
	}
	fclose(fptr);
}

void read_inputs(const char *filename, long long ***inputs, int *input_shape, int *no_inputs)
{
	FILE *fptr = fopen(filename, "r");

	// read dimensions
	fscanf(fptr, "%d %d", no_inputs, input_shape);
	int x = *no_inputs, y = *input_shape;

	// allocate space
	*inputs = calloc(x, sizeof **inputs);
	for(int i=0; i<x; i++)
		(*inputs)[i] = calloc(y, sizeof *((*inputs)[i]));

	// read inputs
	for(int i=0; i<x; i++)
	{
		for(int j=0; j<y; j++)
			fscanf(fptr, "%lld", &(*inputs)[i][j]);
	}

	fclose(fptr);
}