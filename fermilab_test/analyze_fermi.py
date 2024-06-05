
import sys, os
module_path = os.path.abspath("../core")
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import pede
import load_fermi_data
import torch

#'''
starting_params = torch.tensor([
        [   1.1102,    10.4407,   0,     0,     0,      0],
        [   1.3370,    10.3426,   0,     0,     0,      0],
        [   2.2778,    13.3165,   0,     0,     0,      0],
        [   1.7097,    14.6965,   0,     0,     0,      0],
        ])
#'''

# global parameters
pede.N_on_T = 4
pede.global_params = starting_params
#pede.global_params = torch.zeros(pede.N_on_T, 6)
pede.global_params_delta = torch.zeros(pede.N_on_T, 6)

pede.nBatch = 1000
pede.NITER = 20
pede.step_size = 1.0
pede.regularization_lambda = 1e-6

pede.USE_MOMENTUM = True
pede.eta = 0.98
pede.global_params_delta_prev = torch.zeros(pede.N_on_T, 6)

print("global parameter dimension: ", pede.global_params.shape)
print("delta global parameter dim: ", pede.global_params_delta.shape)

# load tracks
print("total tracks: ", len(pede.total_tracks))
pede.total_tracks = load_fermi_data.load_fermi_data()
print("total tracks: ", len(pede.total_tracks))


# do the alignment
x_data = []
y_data = []
for iiter in range(0, pede.NITER):
    print("......................... iteration {} ..........................".format(iiter))
    chisq = pede.one_iteration(iiter*pede.nBatch, pede.nBatch)

    pede.print_tensor(pede.global_params)
    print("chi square = ", chisq)
    y_data.append(chisq)
    x_data.append(iiter)



#................................. program ends here..........................................
# for show purpose
import matplotlib.pyplot as plt
plt.ion() # enable interactive mode
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data, 'b-')

# save chi2 to a text file
if pede.USE_MOMENTUM:
    file_name = "chi2_step_size_{}_momentum_eta_{}_regularization_lambda_{}.txt".format(pede.step_size, pede.eta, pede.regularization_lambda)
else:
    file_name = "chi2_step_size_{}_no_momentum_regularization_lambda_{}.txt".format(pede.step_size, pede.eta, pede.regularization_lambda)
with open(file_name, 'w') as file:
    file.write("step_size = {}, momentum_eta = {}, regularization_lambda = {}\n".format(pede.step_size, pede.eta, pede.regularization_lambda))
    formated_str = '  '.join(f"{number:.4f}" for number in y_data)
    file.write(formated_str)

#line.set_xdata(x_data)
#line.set_ydata(y_data)
ax.relim()
ax.autoscale_view()
fig.canvas.draw()
fig.canvas.flush_events()                                                                                               
                                                                                                                        
# keep the plot after the loop ends                                                                                     
plt.ioff()                                                                                                              
plt.show()       

