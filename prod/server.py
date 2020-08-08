import subprocess
import time
import sys


if len(sys.argv) < 4:
    print("""
    Wrong usage, provide int/float arg
    Please provide type of neural network
    Also provide version information of neural network
    Example usage python3 server.py int <nn-type> <version-info>
    """)
    exit()

if sys.argv[1] == "float":
    exec_name = "./fserver"
elif sys.argv[1] == "int":
    exec_name = "./iserver"
else:
    print(f"Illegal option {sys.argv[1]}")
    exit()
dtype = sys.argv[1]

nntype = sys.argv[2].lower()
vinfo = sys.argv[3].lower()
weights_file = f"data/weights/{nntype}/{vinfo}-{dtype}.dat"

start = time.time()
subprocess.run([exec_name, 'localhost:8080', '1', weights_file])
end = time.time()
# if not stdout:
#     stdout = b""
# if not stderr:
#     stderr = b""

# print(stdout.decode().strip())
# print(stderr.decode().strip())

print("Total time taken:", end-start, "s")