import subprocess
import random

# write a random matrix to the file
mat_size = (4,2)
matrix = []
for _ in range(mat_size[0]):
    row = [round(random.random(), 3) for x in range(mat_size[1])]
    matrix.append(row)

with open('m2.dat', 'w') as wire:
    wire.write(" ".join(map(str, mat_size))+"\n")
    for row in matrix:
        print(row)
        wire.write(" ".join(map(str, row))+"\n")
subprocess.run(['./a.out', 'localhost:8080', '2', 'm2.dat'])