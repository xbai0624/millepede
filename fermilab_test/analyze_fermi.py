
import sys, os
module_path = os.path.abspath("../core")
if module_path not in sys.path:
    sys.path.insert(0, module_path)

import millepede
import load_fermi_data
import torch

'''
starting_params = torch.tensor([
        [   1.1102,    10.4407,   0,     0,     0,      0],
        [   1.3370,    10.3426,   0,     0,     0,      0],
        [   2.2778,    13.3165,   0,     0,     0,      0],
        [   1.7097,    14.6965,   0,     0,     0,      0],
        ])
'''

# global parameters
millepede.N_on_T = 4
#millepede.global_params = starting_params
millepede.global_params = torch.zeros(millepede.N_on_T, 6)
millepede.global_params_delta = torch.zeros(millepede.N_on_T, 6)

millepede.nBatch = 1000
millepede.NITER = 20
millepede.step_size = 1.0
millepede.regularization_lambda = 1e-6

millepede.USE_MOMENTUM = True
millepede.eta = 0.98
millepede.global_params_delta_prev = torch.zeros(millepede.N_on_T, 6)

print("global parameter dimension: ", millepede.global_params.shape)
print("delta global parameter dim: ", millepede.global_params_delta.shape)

# load tracks
print("total tracks: ", len(millepede.total_tracks))
millepede.total_tracks = load_fermi_data.load_fermi_data()
print("total tracks: ", len(millepede.total_tracks))


# do the alignment
x_data = []
y_data = []
for iiter in range(0, millepede.NITER):
    print("......................... iteration {} ..........................".format(iiter))
    chisq = millepede.one_iteration(iiter*millepede.nBatch, millepede.nBatch)

    millepede.print_tensor(millepede.global_params)
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
if millepede.USE_MOMENTUM:
    file_name = "chi2_step_size_{}_momentum_eta_{}_regularization_lambda_{}.txt".format(millepede.step_size, millepede.eta, millepede.regularization_lambda)
else:
    file_name = "chi2_step_size_{}_no_momentum_regularization_lambda_{}.txt".format(millepede.step_size, millepede.eta, millepede.regularization_lambda)
with open(file_name, 'w') as file:
    file.write("step_size = {}, momentum_eta = {}, regularization_lambda = {}\n".format(millepede.step_size, millepede.eta, millepede.regularization_lambda))
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

