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
# For math exp fix this
for i in range(len(clean_output)):
    clean_output[i] = clean_output[i]/10000
    if clean_output[i] >= 600:
        clean_output[i] = 600.0
    elif clean_output[i] <= -600:
        clean_output[i] = -600.0
print(clean_output)

outputs = []
for _ in range(no_outputs):
    row = clean_output[:output_shape]
    outputs.append(row)
    clean_output = clean_output[output_shape:]
# print(outputs)

if nntype == ISOLET:
    classes = ["UNK", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
            "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
elif nntype == MNIST:
    classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
probabilities = []
true_results = [5, 0, 4, 1, 9, 2, 1, 3, 1, 4, 3, 5, 3, 6, 1, 7, 2, 8, 6, 9, 4, 0, 9, 1, 1, 2, 4, 3, 2, 7, 3, 8, 6, 9, 0, 5, 6, 0, 7, 6, 1, 8, 7, 9, 3, 9, 8, 5, 9, 3, 3, 0, 7, 4, 9, 8, 0, 9, 4, 1, 4, 4, 6, 0, 4, 5, 6, 1, 0, 0, 1, 7, 1, 6, 3, 0, 2, 1, 1, 7, 9, 0, 2, 6, 7, 8, 3, 9, 0, 4, 6, 7, 4, 6, 8, 0, 7, 8, 3, 1]
argmax = lambda x: x.index(max(x))
metrics = []
predictions = []
for index, prediction in enumerate(outputs):
    # print("Prediction for input", index+1)
    sfsum = sum(map(math.exp, prediction))
    probs = [math.exp(x)/sfsum for x in prediction]
    # print(probs)
    probabilities.append(probs)

    # for x, y in zip(probs, classes):
    #     print(y, ":", x)
    pred_index = argmax(probs)
    predictions.append(pred_index)
    print("True result:", true_results[index])
    print("Predicted result:", pred_index)
    metrics.append(pred_index == true_results[index])

print(predictions)
accuracy = sum(metrics)/len(metrics) * 100.0
print("Accuracy:",accuracy)