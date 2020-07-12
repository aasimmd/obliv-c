import subprocess
import time
import sys


start = time.time()
subprocess.run(['./a.out', 'localhost:8080', '1'])
end = time.time()
# if not stdout:
#     stdout = b""
# if not stderr:
#     stderr = b""

# print(stdout.decode().strip())
# print(stderr.decode().strip())

print("time taken:", end-start, "s")