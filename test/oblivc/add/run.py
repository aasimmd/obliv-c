import subprocess
import threading
import logging
import random
import time
import sys

# Utility variables
MEAN = 0
STDEV = 0.5
RANDOM_SPEC = (MEAN, STDEV)

# Global threading utils
# This lock is to ensure ordered output
PRINT_LOCK = threading.Lock()
RUN_LOCK = threading.Lock()


def server(stdinput,result_holder):
    # Runs the server process
    # Assume stdinput can be converted to a string
    # stdinput must be the full input to the executable
    RUN_LOCK.acquire()
    proc = subprocess.Popen(['./a.out', 'localhost:8080', '1'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
    )
    RUN_LOCK.release()
    # Prepare stdinput in stages
    # Convert to str and encode
    stdinput = str(stdinput)
    logging.info("Server input %s", stdinput)
    logging.info("Server starting")
    stdinput = stdinput.encode()

    # communicate is a blocking function
    stdoutput, stderror = proc.communicate(stdinput)
    with PRINT_LOCK:
        print(stdoutput.decode())

def client(stdinput,results_holder):
    # Runs the server process
    # Assume stdinput can be converted to a string
    # stdinput must be the full input to the executable
    # Sleep to ensure this starts later
    RUN_LOCK.acquire()
    proc = subprocess.Popen(['./a.out', 'localhost:8080', '2'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
    )
    RUN_LOCK.release()
    # Prepare stdinput in stages
    # Convert to str and encode
    stdinput = str(stdinput)
    logging.info("Client input %s", stdinput)
    logging.info("Client starting")
    stdinput = stdinput.encode()

    # communicate is a blocking function
    stdoutput, stderror = proc.communicate(stdinput)
    with PRINT_LOCK:
        print(stdoutput.decode())

def input_prep():
    # Prepares an input that is ready to be fed
    # Can replace this one with int/matrix if necessary
    rand_input = random.gauss(*RANDOM_SPEC)
    return rand_input


def output_cleaner(output):
    # Write according to output given by executable
    value = output.split()[-1]
    try:
        value = float(value)
    except ValueError:
        print("Invalid output")
        value = None
    return value

def main():
    results={}
    a=5681
    b=7332
    for i in range(1):
        server_thread = threading.Thread(target=server,
        args=(a,results))
        client_thread = threading.Thread(target=client,
        args=(b,results))

        server_thread.start()
        client_thread.start()

        # Join ensures the threads don't finish after main
        server_thread.join()
        client_thread.join()

if __name__ == "__main__":
    # Logging specifics
    # Remove if date/time is unnecessary
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
    datefmt="%H:%M:%S")

    main()
