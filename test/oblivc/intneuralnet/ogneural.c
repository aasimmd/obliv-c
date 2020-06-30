#include<stdio.h>
#include<stdlib.h>


void read_weights(char *filename, float ****weights, float ***biases, int ***shapes, int *no_layers);
void read_inputs(char *filename, float ***inputs, int *input_shape, int *no_inputs);
void matmul(float **mat1, float **mat2, float ***op, int m1, int n1, int m2, int n2);
void add_bias(float **output, float *bias, int no_outputs, int len);
void feedforward(float **inputs, float ***weights, float **biases, int **shapes, int no_layers, int no_inputs, int input_shape, float ***outputs);

int main()
{
	float ***weights, **biases, **inputs, **outputs;
	int no_layers, **shapes, no_inputs, input_shape;
	read_weights("weights.dat", &weights, &biases, &shapes, &no_layers);
	read_inputs("inputs.dat", &inputs, &input_shape, &no_inputs);
	printf("All data fetched\n");

	// Print out inputs for prettiness
	// printf("n:%d\n",no_inputs);
	// printf("l:%d\n",no_layers);
	printf("Input vector shape: %d & %d\n", no_inputs, input_shape);
	printf("Layer shapes:\n");
	for(int i=0; i<no_layers; i++)
		printf("%d,%d ",shapes[i][0], shapes[i][1]);
	putchar('\n');

	// Perform feed forward
	feedforward(inputs, weights, biases, shapes, no_layers, no_inputs, input_shape, &outputs);
	

	printf("Output shape: %d & %d\n", no_inputs, shapes[no_layers-1][1]);
	printf("Output vector:\n");
	for(int x=0; x<no_inputs; x++)
	{
		for(int y=0; y<shapes[no_layers-1][1]; y++)
		{
			printf("%f ", outputs[x][y]);
		}
		putchar('\n');
	}
	return 0;
}

void read_weights(char *filename, float ****weights, float ***biases, int ***shapes, int *no_layers)
{
	FILE *fptr = fopen(filename, "r");
	fscanf(fptr, "%d", no_layers);
	*shapes = calloc(*no_layers, sizeof **shapes);
	*weights = calloc(*no_layers, sizeof **weights);
	*biases = calloc(*no_layers, sizeof **biases);
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
				fscanf(fptr, "%f", &(*weights)[l][x][y]);
			}
		}
		for(int x=0; x<n; x++)
			fscanf(fptr, "%f", &(*biases)[l][x]);
	}
	fclose(fptr);
}

void read_inputs(char *filename, float ***inputs, int *input_shape, int *no_inputs)
{
	FILE *fptr = fopen("inputs.dat", "r");

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
			fscanf(fptr, "%f", &(*inputs)[i][j]);
	}

	fclose(fptr);
}

void matmul(float **mat1, float **mat2, float ***op, int m1, int n1, int m2, int n2)
{
	// Multiply the matrices and store it in output
	// Output is uninitialzed, allocate memory accordingly
	
	// Create a temporary array so that the call can be used as matmul(x, op, op);
	*op = calloc(m1, sizeof **op);
	for(int x=0; x<m1; x++)
		(*op)[x] = calloc(n2, sizeof *((*op)[x]));

	float tmpsum;
	for(int x=0; x<m1; x++)
	{
		for(int y=0; y<n2; y++)
		{
			tmpsum = 0;
			for(int z=0; z<n1; z++)
				tmpsum += mat1[x][z]*mat2[z][y];
			(*op)[x][y] = tmpsum;
		}
	}
}

void add_bias(float **output, float *bias, int no_outputs, int len)
{
	for(int x=0; x<no_outputs; x++)
	{
		for(int y=0; y<len; y++)
			output[x][y] += bias[y];
	}
}

void feedforward(float **inputs, float ***weights, float **biases, int **shapes, int no_layers, int no_inputs, int input_shape, float ***outputs)
{
	// inputs will be freed and realloced here, make sure it is a dynamic array
	int opx, opy;
	for(int l=0; l<no_layers; l++)
	{
		matmul(inputs, weights[l], outputs, no_inputs, input_shape, shapes[l][0], shapes[l][1]);
		opx = no_inputs;
		opy = shapes[l][1];
		input_shape = opy;
		add_bias(*outputs, biases[l], opx, opy);
		printf("Layer %d done\n", l+1);
		
		// Free and realloc inputs
		for(int x=0; x<no_inputs; x++)
			free(inputs[x]);
		free(inputs);
		inputs = calloc(opx, sizeof *inputs);
		for(int x=0; x<opx; x++)
		{
			inputs[x] = calloc(opy, sizeof *inputs[x]); 
			for(int y=0; y<opy; y++)
				inputs[x][y] = (*outputs)[x][y];
		}
		// printf("Successfully transferred %d\n", l+1);
	}
}
