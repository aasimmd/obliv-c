int party_id;

typedef struct {
    // common information between the parties
    int compared;

    // secret information
    int val;
} protocolIO;

void comparator(void* args);