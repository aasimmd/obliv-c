int party_id;

typedef struct {
    // common information between the parties
    float compressed;

    // secret information
    float val;
} protocolIO;

void mysticalc(void* args);
void sigmoid(protocolIO *, obliv float, obliv float *);