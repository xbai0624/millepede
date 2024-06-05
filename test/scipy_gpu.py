import torch
import numpy as np
from scipy.sparse.linalg import LinearOperator

class GPUOperator(LinearOperator):
    def __init__(self, A):
        self.A = A
        self.shape = A.shape
        self.dtype = np.dtype(A.cpu().numpy().dtype)

    def _matvec(self, x):
        x_torch = torch.from_numpy(x).to(self.A.device)
        Ax = torch.mv(self.A, x_torch)
        return Ax.cpu().numpy()

# Create a large dense matrix A and vector b in PyTorch
device = torch.device("cpu" if torch.backends.mps.is_available() else "cpu")
#device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
A = torch.rand(1000, 1000, device=device)
b = torch.rand(1000, device=device)

# Create the GPU operator
A_op = GPUOperator(A)

from scipy.sparse.linalg import cg, gmres, bicgstab, minres, qmr

# Convert b to NumPy array for SciPy solver
b_np = b.cpu().numpy()

# Solve using SciPy's CG method with the custom GPU operator
#x_np, info = cg(A_op, b_np)
# gmres
x_np, info = gmres(A_op, b_np)
# bicgstab
#x_np, info = bicgstab(A_op, b_np)
# minres
#x_np, info = minres(A_op, b_np)
# qmr
#x_np, info = qmr(A_op, b_np)

# Convert the solution back to a PyTorch tensor
x = torch.from_numpy(x_np).to(device)
print("CG Solution:", x)
