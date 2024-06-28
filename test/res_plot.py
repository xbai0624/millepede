#file1 = "../fermilab_test/chi2_step_size_1.0_momentum_eta_0.1_regularization_lambda_1e-06_method_gmres_epoch_10.txt"
file1 = "../fermilab_test/chi2_step_size_0.1_no_momentum_regularization_lambda_0.9_method_1e-06_epoch_gmres.txt"
#file1 = "../fermilab_test/chi2_step_size_1.0_momentum_eta_0.9_regularization_lambda_1e-06_method_gmres_epoch_10.txt"

data1 = []
x_axis1 = []

with open(file1, 'r') as f1:
    lines = f1.readlines()
    data1 = [float(s) for s in lines[1].split()]

for i in range(len(data1)):
    x_axis1.append(i)

import matplotlib.pyplot as plt
plt.plot(x_axis1, data1, label="SGD with momentum")

plt.xlabel("Iteration", fontsize=16)
plt.xlim(0, 70)
plt.ylabel("$\sum\chi^2$ per 2000 tracks", fontsize=16)
plt.title("$\chi^2$ evolution", fontsize=18)

plt.legend(fontsize=18)

plt.savefig("../fermilab_beamtest_data.png", dpi=300)
plt.show()
