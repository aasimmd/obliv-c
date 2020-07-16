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

print("Total time taken:", end-start, "s")

clean_output = stdout.decode().strip().split()
# print(clean_output)

no_outputs = int(clean_output[0])
output_shape = int(clean_output[1])
clean_output = clean_output[2:]
clean_output = list(map(float, clean_output))
# For math exp fix this
for i in range(len(clean_output)):
    if clean_output[i] > 600:
        clean_output[i] = 600.0
    elif clean_output[i] < -600:
        clean_output[i] = -600.0
print(clean_output)

outputs = []
for _ in range(no_outputs):
    row = clean_output[:output_shape]
    outputs.append(row)
    clean_output = clean_output[output_shape:]
# print(outputs)

if nntype == ISOLET:
    classes = ["UNK", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    true_results = [16, 21, 9, 22, 25, 15, 24, 25, 21, 2, 14, 26, 12, 5, 5, 17, 21, 9, 26, 21, 25, 4, 22, 16, 20, 9, 10, 13, 3, 13, 22, 14, 18, 12, 26, 24, 6, 14, 22, 6, 7, 11, 4, 19, 22, 13, 19, 8, 16, 17, 19, 6, 18, 4, 9, 15, 10, 4, 10, 26, 2, 13, 5, 16, 25, 13, 6, 14, 11, 3, 26, 20, 10, 9, 16, 17, 13, 16, 17, 17, 16, 14, 5, 11, 7, 10, 3, 22, 24, 1, 1, 9, 4, 18, 20, 14, 4, 1, 13, 12]
elif nntype == MNIST:
    classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    true_results = [7, 2, 1, 0, 4, 1, 4, 9, 5, 9, 0, 6, 9, 0, 1, 5, 9, 7, 3, 4, 9, 6, 6, 5, 4, 0, 7, 4, 0, 1, 3, 1, 3, 4, 7, 2, 7, 1, 2, 1, 1, 7, 4, 2, 3, 5, 1, 2, 4, 4, 6, 3, 5, 5, 6, 0, 4, 1, 9, 5, 7, 8, 9, 3, 7, 4, 6, 4, 3, 0, 7, 0, 2, 9, 1, 7, 3, 2, 9, 7, 7, 6, 2, 7, 8, 4, 7, 3, 6, 1, 3, 6, 9, 3, 1, 4, 1, 7, 6, 9]
probabilities = []
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
    print(f"True vs Pred: {true_results[index]: <3} | {pred_index: <3}")
    metrics.append(pred_index == true_results[index])

print(predictions)
accuracy = sum(metrics)/len(metrics) * 100.0
print("Accuracy:",accuracy)