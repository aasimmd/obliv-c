import subprocess
import time
import math


MNIST = 1
ISOLET = 2
nntype = ISOLET

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
true_results = [18,  6, 23,  9, 11, 24,  2,  2,  1, 17, 18, 12,  2, 18,  6, 26,  6, 4, 17, 22,  3,  5, 13, 13,  6, 22, 21, 19, 14, 18,  1, 20, 10, 14, 17, 17, 15,  1,  4, 24, 15, 16, 25, 21, 22, 24, 16, 11, 11,  4, 18, 5,  2, 26,  9, 22, 23, 12, 13, 18, 12, 13, 10, 24, 22, 26,  2, 25, 11, 19, 11, 17, 15,  2, 12, 23,  6,  8, 11, 13,  9,  9, 12, 23,  6, 20, 18,  2,  4, 14,  7, 26, 21,  2, 17, 23, 22, 19, 13,  2]
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