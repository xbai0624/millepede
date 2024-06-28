import torch
import time

if torch.backends.mps.is_available():
    device = torch.device('mps')
else:
    device = torch.device('cpu')

print(device)

def one_test(ntrack = 4000):
    high = 10
    low = 5
    dimA = 12 * ntrack
    dimB = 4 * ntrack + 36

    A = low + (high-low)*torch.rand(dimA, dimB)
    B = low + (high-low)*torch.rand(dimB, 1)

    t1 = time.time()
    C = torch.matmul(A, B)
    t2 = time.time()

    cpu_used_time = t2 - t1
    print("cpu used time {}".format(t2-t1))

    t3 = time.time()
    A_g = A.to(device)
    B_g = B.to(device)

    t4 = time.time()
    C = torch.matmul(A_g, B_g)
    t5 = time.time()
    D = C.cpu()

    d_time = t5-t4

    print("gpu time used (NOT include time for moving data from ram to GPU): {} seconds.".format(d_time))
    print("gpu time used (include time for moving data from ram to GPU): {} seconds.".format(t5-t3))

    gpu_used_time = t5 - t3

    return cpu_used_time, gpu_used_time

x_data = []
cpu_data = []
gpu_data = []

for i in range(1000, 10000, 1000):
    x_data.append(i)
    c, g = one_test(i)
    cpu_data.append(c)
    gpu_data.append(g)


import matplotlib.pyplot as plt
plt.plot(x_data, cpu_data, label="CPU")
plt.plot(x_data, gpu_data, label="GPU")

plt.xlabel("Number of Total Tracks")
plt.ylabel("Time Cost")

plt.legend(fontsize=14)

plt.show()
