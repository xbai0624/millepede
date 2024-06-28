import torch
import time



if torch.backends.mps.is_available():
    gpu_device = torch.device('mps')
else:
    gpu_device = torch.device('cpu')

cpu_device = torch.device('cpu')

print(gpu_device)

high = 10
low = 5

ntrack = 4000
dimA = 12 * ntrack
dimB = 4 * ntrack + 36

#A = low + (high-low)*torch.rand(10, 10)
#B = low + (high-low)*torch.rand(10, 10)

A = low + torch.zeros(dimA, dimB)
B = low + torch.zeros(dimB, 1)

#A = low + torch.zeros(5000, 5000)
#B = low + torch.zeros(5000, 1)

#A = low + (high-low)*torch.rand(dimA, dimB)
#B = low + (high-low)*torch.rand(dimB, 1)


memory_used = A.numel() * A.element_size() / (1024 * 1024)
print("used {} MB.".format(memory_used))

print(A.size())
print(B.size())
print(A)
print(B)

t1 = time.time()
C = torch.matmul(A, B)
t2 = time.time()
print("C = ")
print(C)
print(C[0,0].item())

print("cpu used time {}".format(t2-t1))

t3 = time.time()
A_g = A.to(gpu_device)
B_g = B.to(gpu_device)

t4 = time.time()
C = torch.matmul(A_g, B_g)
t5 = time.time()

#D = C.to(cpu_device)
print("D = ")
print(C)

print(C[0,0].item())

d_time = t5-t4

print("gpu time used (NOT include time for moving data from ram to GPU): {} seconds.".format(d_time))
print("gpu time used (include time for moving data from ram to GPU): {} seconds.".format(t5-t3))


print(C.size())
