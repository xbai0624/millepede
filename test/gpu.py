import torch
import time

if torch.backends.mps.is_available():
    device = torch.device('mps')
else:
    device = torch.device('cpu')

print(device)

high = 10
low = 5

A = low + (high-low)*torch.rand(12000, 120000)
B = low + (high-low)*torch.rand(120000, 12000)

memory_used = A.numel() * A.element_size() / (1024 * 1024)
print("used {} MB.".format(memory_used))

print(A.size())
print(B.size())

t1 = time.time()

C = torch.matmul(A, B)

#A_g = A.to(device)
#B_g = B.to(device)
#C = torch.matmul(A_g, B_g)

t2 = time.time()

d_time = t2-t1

print("time used: {} seconds.".format(d_time))

print(C.size())
