import subprocess
import threading
import logging
import random
import time
import math


# Utility variables
MEAN = 0
STDEV = 0.5
RANDOM_SPEC = (MEAN, STDEV)

# Global threading utils
# This lock is to ensure ordered output
PRINT_LOCK = threading.Lock()
RUN_LOCK = threading.Lock()


def server(stdinput, result_holder):
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
    
    # Acquire locks
    with PRINT_LOCK:
        result_holder["server"] = stdoutput.decode().strip()
        # logging.info("Server output")
        # print(stdoutput.decode().strip())
    # Release lock


def client(stdinput, result_holder):
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
    
    # Acquire locks
    with PRINT_LOCK:
        # logging.info("Client output")
        # print(stdoutput.decode().strip())
        result_holder["client"] = stdoutput.decode().strip()
    # Release lock


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


def sigmoid(z):
    return 1/(1+math.exp(-z))


def main():
    server_input = input_prep()
    client_input = input_prep()

    # An output holder, reqd while using threading
    results = {}
    results["server"] = 0
    results["client"] = 0

    server_thread = threading.Thread(target=server,
    args=(server_input,results))
    client_thread = threading.Thread(target=client,
    args=(client_input,results))

    server_thread.start()
    client_thread.start()

    # Join ensures the threads don't finish after main
    server_thread.join()
    client_thread.join()

    # Dissect the result
    server_out = output_cleaner(results["server"])
    client_out = output_cleaner(results["client"])

    # print(server_input, client_input)
    sigmoid_in = server_input + client_input
    print("true output", sigmoid(sigmoid_in))
    print("server:", server_out)
    print("client:", client_out)


if __name__ == "__main__":
    # Logging specifics
    # Remove if date/time is unnecessary
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
    datefmt="%H:%M:%S")

    main()