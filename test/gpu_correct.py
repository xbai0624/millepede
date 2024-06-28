import torch
import time

if torch.backends.mps.is_available():
    gpu_device = torch.device('mps')
else:
    gpu_device = torch.device('cpu')

cpu_device = torch.device('cpu')

device = cpu_device

print(device)

high = 10
low = 5

ntrack = 9450
dimA = 12 * ntrack
dimB = 4 * ntrack + 36


#A = torch.zeros(dimA, dimB, device=device)
#B = torch.zeros(dimB, 1, device=device)

#A = low + (high-low)*torch.rand(dimA, dimB, device=device)
#B = low + (high-low)*torch.rand(dimB, 1, device=device)

A = torch.rand(dimA, dimB, device=device)
B = torch.rand(dimB, 1, device=device)

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

print("gpu used time {}".format(t2-t1))

