int party_id;

#define ITERATIONS 100000

typedef struct {
    // common information between the parties
    int sum;

    // secret information
    int val;
} protocolIO;

void adder(void* args);
