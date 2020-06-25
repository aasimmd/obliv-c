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

    party_id = (argv[2][0]=='1'? 1 : 2);
    setCurrentParty(&pd, party_id); // only checks for a '1'
    scanf("%d", &(io.val));

    execYaoProtocol(&pd, comparator, &io);
    cleanupProtocol(&pd);

    //print result
    printf("%d", io.compared);
    // if(io.compared == -1)
    //     printf("client is greater\n");
    // else if(io.compared == 1)
    //     printf("server is greater\n");
    // else
    //     printf("They are equal\n");

    
    return 0;
}