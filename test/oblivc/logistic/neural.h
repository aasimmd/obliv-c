int party_id;

// Maximum iterations possible at current stage
#define MAXCORDIC 13

typedef struct {
    // common information between the parties
    float compressed;
    int cordic_iterations;

    // secret information
    float val;
} protocolIO;

void mysticalc(void* args);
void sigmoid(protocolIO *, obliv float, obliv float *);