
file1 = "../core/chi2_step_size_0.02_momentum_eta_0.9_regularization_lambda_1e-06.txt"
file2 = "../core/chi2_step_size_0.02_no_momentum_regularization_lambda_0.9.txt"


data1 = []
data2 = []

with open(file1, 'r') as f1:
    lines = f1.readlines()
    data1 = [float(s) for s in lines[1].split()]

with open(file2, 'r') as f2:
    lines = f2.readlines()
    data2 = [float(s) for s in lines[1].split()]

x_axis = []
for i in range(len(data1)):
    x_axis.append(i)

import matplotlib.pyplot as plt
plt.plot(x_axis, data1, label="with momentum")
plt.plot(x_axis, data2, label="no momentum")

plt.xlabel("iteration")
plt.ylabel("$\sum\chi^2$ per 1000 tracks")
plt.title("$\chi^2$ evolution")

plt.legend(fontsize=14)

plt.savefig("../chi2_evolution1.png", dpi=300)
plt.show()
