#include <stdio.h>
#include <stdlib.h>
#include <obliv.h>
#include <string.h>
#include "util.h"
#include "dbg.h"

#include "mmul.h"

void check_mem(float **m1, float **m2, int party)
{
    if(party == 1)
    {
        // check if m1 is valid
        if(m1 == NULL)
        {
            log_err("Memory alloc failed for pickachu\n");
            clean_errno();
            exit(1);
        }
    }
    else if(party == 2)
    {
        // check if m2 is valid
        if(m2 == NULL)
        {
            log_err("Memory alloc failed for client\n");
            clean_errno();
            exit(1);
        }
    }
}

void load_data(protocolIO *io, float ***m1, float ***m2, int party)
{
    // m1 and m2 are pointers to the matrix
    // needed because their locations in memory can be changed here
    FILE *input_file = fopen(io->src, "r");
    if (input_file == NULL)
    {
        log_err("File %s not found \n", io->src);
        clean_errno();
        exit(1);
    }

    // The input files are in this format
    // the size of the matrix is stored at the top
    /*
    m n 
    x11, x12, x13, ... x1n
    ...
    ...
    xm1, xm2, xm3, ... xmn
    */

    // m and n are the dimensions of the input matrix
    int *m, *n;
    float ***matrix;
    if(party == 1)
    {
        m = &(io->m1);
        n = &(io->n1);
        matrix = m1;
    }
    else if(party == 2)
    {
        m = &(io->m2);
        n = &(io->n2);
        matrix = m2;
    }
    // m is no of rows
    // n is no of cols
    *m = 0;
    *n = 0;

    int memsize = ALLOC;
    double tmp; // temporary store between file and matrix
    int check; // error check while reading
    fscanf(input_file, "%d %d", m, n);
    *matrix = calloc(*m, sizeof **matrix);
    // for(int i=0; i<*m; i++)
    // {
    //     printf("%d ", (*matrix)[i]);
    // }
    // putchar('\n');
    check_mem(*m1, *m2, party);
    float **x;
    for(int i=0; i<*m; i++)
    {
        (*matrix)[i] = calloc(*n, sizeof *(*matrix)[i]);
        // x = (*matrix)[i];
        // printf("snap: %d\n", x);
        // for(int k=0; k<*n; k++)
            // printf("%d ", (*matrix)[i][k]);
        // putchar('\n');
        for(int j=0; j<*n; j++)
        {
            check = fscanf(input_file, "%lf", &tmp);
            if(check != 1)
            {
                log_err("Could not read value at %d %d", i, j);
                clean_errno();
                exit(1);
            }
            // printf("lolol\n");
            // printf("%d %d %d %d %lf\n", i, j, *m, *n, tmp);
            (*matrix)[i][j] = (float)(tmp);
        }
    }
    // printf("LMAOOOOO\n");
    // exit(1);

    log_info("Loading %d x %d values\n", *m, *n);
    fclose(input_file);
}

int main(int argc, char *argv[])
{
    // command line args:
    // ./matmul hostname:port [1|2] input_file
    printf("Matrix multiplication\n");
    if(argc == 4)
    {
        const char *remote_host = strtok(argv[1], ":");
        const char *port = strtok(NULL, ":");
        ProtocolDesc pd;
        protocolIO io;

        // Make connection between two shells
        // Modified ocTestUtilTcpOrDie() function from obliv-c/test/oblivc/common/util.c
        log_info("Connecting to %s on port %s ...\n", remote_host, port);
        if(argv[2][0] == '1') {
            if(protocolAcceptTcp2P(&pd,port)!=0) {
                log_err("TCP accept from %s failed\n", remote_host);
                exit(1);
            }
        } else {
            if(protocolConnectTcp2P(&pd,remote_host,port)!=0) {
                log_err("TCP connect to %s failed\n", remote_host);
                exit(1);
            }
        }

        // Final initializations before entering protocol
        party_id = (argv[2][0]=='1'? 1 : 2);
        setCurrentParty(&pd, party_id); // only checks for a '1'
        io.src = argv[3]; // filename
        // lap = wallClock();


        io.result = calloc(ALLOC, sizeof(float *));
        for(int i=0; i<ALLOC; i++)
        {
            io.result[i] = calloc(ALLOC, sizeof(float));
        }

        time_track = wallClock();

        execYaoProtocol(&pd, matmul, &io);

        double runtime = wallClock() - time_track;

        cleanupProtocol(&pd);

        printf("Ran in %lf s time\n", runtime);

        // Print resultant matrix
        printf("Resultant of size: %d + %d\n", io.res_m, io.res_n);
        for(int i=0; i<io.res_m; i++)
        {
            for(int j=0; j<io.res_n; j++)
            {
                printf("%lf ", io.result[i][j]);
            }
            putchar('\n');
        }
    }
    else
    {
        log_info("Usage: %s <hostname:port> <1|2> <filename>\n" 
                 "\tHostname usage:\n" 
                 "\tlocal -> 'localhost' remote -> IP address or DNS name\n", argv[0]);
    }
    return 0;
}