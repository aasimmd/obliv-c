import subprocess
import time
import math


MNIST = 1
ISOLET = 2
nntype = MNIST

proc = subprocess.Popen(['./a.out', 'localhost:8080', '2'],
stdin=subprocess.PIPE,
stdout=subprocess.PIPE
)

start = time.time()
stdout, stderr = proc.communicate()
end = time.time()
if not stdout:
    stdout = b""
if not stderr:
    stderr = b""

# print(stdout.decode().strip())
# print(stderr.decode().strip())

print("time taken:", end-start, "s")

clean_output = stdout.decode().strip().split()
# print(clean_output)

no_outputs = int(clean_output[0])
output_shape = int(clean_output[1])
clean_output = clean_output[2:]
clean_output = list(map(float, clean_output))

outputs = []
for _ in range(no_outputs):
    row = clean_output[:output_shape]
    outputs.append(row)
    clean_output = clean_output[output_shape:]
print(outputs)

if nntype == ISOLET:
    classes = ["UNK", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
elif nntype == MNIST:
    classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
probabilities = []
true_results = [5, 0, -1, -1, -1]
for index, prediction in enumerate(outputs):
    print("Prediction for input", index+1)
    sfsum = sum(map(math.exp, prediction))
    probs = [math.exp(x)/sfsum for x in prediction]
    # print(probs)
    probabilities.append(probs)

    for x, y in zip(probs, classes):
        print(y, ":", x)
    print("True result:", true_results[index])