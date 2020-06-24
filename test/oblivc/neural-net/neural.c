#include<stdio.h>
#include<stdlib.h>


void read_weights(char *filename, float ****weights, float ***biases, int ***shapes, int *no_layers);
void read_inputs(char *filename, float ***inputs, int *input_shape, int *no_inputs);

int main()
{
	float ***weights, **biases, **inputs;
	int no_layers, **shapes, no_inputs, input_shape;
	read_weights("weights.dat", &weights, &biases, &shapes, &no_layers);
	read_inputs("inputs.dat", &inputs, &input_shape, &no_inputs);
	printf("All inputs fetched\n");

	// Print out inputs for prettiness
	printf("n:%d\n",no_inputs);
	printf("l:%d\n",no_layers);
	printf("Layer shapes:\n");
	for(int i=0; i<no_layers; i++)
		printf("%d,%d ",shapes[i][0], shapes[i][1]);
	putchar('\n');
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
