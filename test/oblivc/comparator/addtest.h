int party_id;

#define ITERATIONS 100000

typedef struct {
    // common information between the parties
    float result;
    int iresult;

    // secret information
    float val;
    int ival;
} protocolIO;

void iteradder(void* args);
void intiteradder(void* args);