// memory-block size to be alloc'd
#define ALLOC 10
// size of matrix side, nxn for now
#define MATLEN 3

// global variable for party identification
int party_id;

// public information, used for comm between files
typedef struct {
    char *src; // file to read data from
    int m1, n1; // dimensions of matix 1 (server)
    int m2, n2; // dimensions of matix 1 (client)
    // Multiplication happens as M1 x M2
    // resulting operation is (m1,n1)x(m2,n2)
    // implying n1 == m2
    // Result matrix is (m1, n2)
    float **result;
    int res_m, res_n; // dimensions of result
    // res_m = m1
    // res_n = n2
} protocolIO;

double time_track;


// Define public functions
void matmul(void *args);
void load_data(protocolIO *io, float ***m1, float ***m2, int party);
void check_mem(float **m1, float **m2, int party);