#!/usr/bin/python3
import subprocess


proc = subprocess.Popen(['./a.out', 'localhost:8080', '2'],
stdin=subprocess.PIPE,
stdout=subprocess.PIPE
)

# input_val = int(input("Enter your value:"))
input_val = 1e+5
# print("passing in the value:", input_val)

# subprocess format
# stdout_val, stderr_value = proc.communicate(stdin_value)

stdin_val = str(input_val).encode()
output_val, err_value = proc.communicate(stdin_val)

# expected output val = {1, 0, -1}
print(output_val.decode().strip())