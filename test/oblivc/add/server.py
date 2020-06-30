#!/usr/bin/python3
import subprocess


proc = subprocess.Popen(['./a.out', 'localhost:8080', '1'],
stdin=subprocess.PIPE,
stdout=subprocess.PIPE
)

input_val = int(input("Enter a number : "))
# print("passing in the value:", input_val)

# subprocess format
# stdout_val, stderr_value = proc.communicate(stdin_value)

stdin_val = str(input_val).encode()
output_val, err_value = proc.communicate(stdin_val)

print(output_val)
