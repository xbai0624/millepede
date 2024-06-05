
file1 = "../core/chi2_step_size_0.02_momentum_eta_0.9_regularization_lambda_1e-06.txt"
file2 = "./gmres_output.txt"


data1 = []
x_axis1 = []
data2 = []
x_axis2 = []

with open(file1, 'r') as f1:
    lines = f1.readlines()
    data1 = [float(s) for s in lines[1].split()]

with open(file2, 'r') as f2:
    lines = f2.readlines()
    data2 = [float(s) for s in lines[1].split()]

for i in range(len(data1)):
    x_axis1.append(i)

for i in range(len(data2)):
    x_axis2.append(i)

import matplotlib.pyplot as plt
plt.plot(x_axis1, data1, label="SVD minimizer")
plt.plot(x_axis2, data2, label="GMRES minimizer")

plt.xlabel("iteration")
plt.ylabel("$\sum\chi^2$ per 1000 tracks")
plt.title("$\chi^2$ evolution")

plt.legend(fontsize=14)

plt.savefig("../minimizer_compare.png", dpi=300)
plt.show()
