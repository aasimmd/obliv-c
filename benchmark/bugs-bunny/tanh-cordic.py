import math
import random


cordic_iters = 0
def tanh(z):
    inv2 = [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 
    0.00390625, 0.001953125, 0.0009765625, 0.00048828125, 0.000244140625, 0.0001220703125]
    tang = [0.5493061, 0.2554128, 0.1256572, 0.0625816, 0.0312602, 
    0.0156263, 0.0078127, 0.0039063, 0.0019531, 0.0009766, 0.0004883, 0.0002441, 0.0001221]
    aval = [0.866025404, 0.838525492, 0.831948719, 0.83032223, 0.8299167, 0.829815386, 
    0.829790061, 0.82978373, 0.829782148, 0.829781752, 0.829781653, 0.829781628, 0.829781622]

    x = 1.0
    y = 0.0
    z = -z

    repeat = False
    i = 1
    while i <= cordic_iters:
        if i == 1 or i == 4 or i == 13:
            reps = 2
        else:
            reps = 1
        
        for _ in range(reps):
            if z < 0:
                d = -1
            else:
                d = 1
            x_ = x + y*d*inv2[i-1]
            y_ = y + x*d*inv2[i-1]
            z_ = z - d*tang[i-1]
            x = x_
            y = y_
            z = z_

        i += 1

    x = x/aval[cordic_iters-1]
    y = y/aval[cordic_iters-1]

    return -y/x

def getprec(x):
    ctr = 0
    while x < 1:
        ctr += 1
        x *= 10
    return ctr

err = 0.0
n = 100
stdev = 1000
prec = 0.0
for i in range(n):
    val = random.gauss(0, stdev)
    g = tanh(val)
    h = math.tanh(val)
    prec += getprec(abs(g-h))
    err += ((g-h)/h)**2
err = math.sqrt(err)/n

print("Iterations  :", cordic_iters)
print("Stdev from 0:", stdev)
print("RMS error   :", round(err, 5))
print("Precision   :", prec/n)
print("")
            