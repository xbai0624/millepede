#!/opt/homebrew/bin/python3

import torch
import time

from track_fitter import N_on_T, fitter, projector, solver
from text_parser import vec3_t, track_parser
from ref import alignment_result

# load tracks
print("loading tracks, please wait...")
start_time = time.time();
parser = track_parser()
total_tracks = parser.tracks
end_time = time.time();
print("tracks loading completed, total time used : {:.4f} seconds.".format(end_time - start_time))
# a general tool for local track fit
fitter = fitter()
projector = projector()
solver = solver()

# convention of global_params [[d1x, d1y, d1z, a1x, a1y, a1z], 
#                              [d2x, d2y, d2z, a2x, a2y, a2z],
#                              ...]
global_params = torch.zeros(N_on_T, 6)
#global_params = alignment_result*(-1.0)
global_params_delta = torch.zeros(N_on_T, 6)
print("global parameter dimension: ", global_params.shape)
print("delta global parameter dim: ", global_params_delta.shape)

# we use 1000 tracks for each single fit, and a total of 1,000,000 tracks
# so we will have 1000 iterations
nBatch = 1000
NITER = 200
step_size = 0.02
regularization_lambda = 2e-6
# fix this layer (reference layer)
iFixLayerIndex = 0

# parameter for mementum
USE_MOMENTUM = True
eta = 0.9
global_params_delta_prev = torch.zeros(N_on_T, 6)


# a function to print pytorch tensors, the original print function for it is too ugly
def print_tensor(A):
    for row in A:
        formated_row = ["{:{}.{}f}".format(elem, 12, 6) for elem in row]
        print("[", "   ".join(formated_row), "]")
    print("\n")


# transform based on current global parameters
#     in the generator, I do translation first, and then do rotation
#     so to reverse that, here I do rotation first, then do translation
#     for the rotation, in generator R = RzRyRx, so in here we do R = RxRyRz
def transform_point(p, ilayer):
    rotation = torch.tensor([[1, -global_params[ilayer, 5].item(), global_params[ilayer, 4].item()],
                            [global_params[ilayer, 5].item(), 1, -global_params[ilayer, 3].item()],
                            [-global_params[ilayer, 4].item(), global_params[ilayer, 3].item(), 1]])

    translation = torch.tensor([[global_params[ilayer, 0].item()],
                               [global_params[ilayer, 1].item()],
                               [global_params[ilayer, 2].item()]])
    res = torch.matmul(rotation, p)
    res = res + translation
    return res

def one_iteration(start, n_batch):
    # update the global params
    global global_params, global_params_delta, global_params_delta_prev, regularization_lambda
    global_params = global_params - global_params_delta

    # prepare the big matrix A
    A = torch.zeros(nBatch*N_on_T*2, nBatch*4+6*N_on_T)
    print("A size: ", A.shape)

    # prepare the r vector (difference between track projection and measurement)
    r = torch.zeros(nBatch*N_on_T*2, 1)
    print("r size: ", r.shape)

    # for show purpose, this is a sum of chi2 over 1000 tracks
    chi_square = 0

    # fill A and r
    # 
    # loop for track
    for j in range(0, n_batch):
        original_track = total_tracks[start+j]
        assert len(original_track) == N_on_T
        transformed_track = []

        # transform track using current global params
        ilayer = 0
        for p in original_track:
            v = torch.tensor([[p.x], [p.y], [p.z]])
            v = transform_point(v, ilayer)
            v = vec3_t(v[0,0].item(), v[1,0].item(), v[2,0].item())
            transformed_track.append(v)
            ilayer += 1

        '''
        for i in range(0, ilayer):
            print("z = {:8.4f} {:8.4f}, x = {:8.4f} {:8.4f}, y = {:8.4f} {:8.4f}".format(
                original_track[i].z, transformed_track[i].z,
                original_track[i].x, transformed_track[i].x,
                original_track[i].y, transformed_track[i].y,
                ))
        input("check transformation")
        '''

        # perform a local fit
        direction, cross_point, chi2 = fitter.solve(transformed_track)
        chi_square += chi2
        # since direction is a unit vector, we need to get the true kx and ky
        kx = direction.x / direction.z
        ky = direction.y / direction.z
        bx = cross_point.x
        by = cross_point.y

        '''
        print(" transformed track chi2 = {:.4f}".format(chi2))
        _, _, chi2_o = fitter.solve(original_track)
        print(" original track chi2 = {:.4f}".format(chi2_o))
        input("enter to continue...")
        '''

        #print("track :", j)
        # fill A
        for i in range(0, N_on_T):
            # dx
            row = j*N_on_T*2 + 2*i; col_global = 6*i; col_local = 6*N_on_T + j*4
            #print("row: ", row, "col: ", col+6)
            A[row, col_global+0] = 1; A[row, col_global+1] = 0; A[row, col_global+2] = -kx
            A[row, col_global+3] = -kx * original_track[i].y
            A[row, col_global+4] = original_track[i].z + kx*original_track[i].x
            A[row, col_global+5] = -original_track[i].y
            A[row, col_local+0] = -transformed_track[i].z
            A[row, col_local+1] = -1
            # dy
            row = row + 1
            A[row, col_global+0] = 0; A[row, col_global+1] = 1; A[row, col_global+2] = -ky
            A[row, col_global+3] = -(original_track[i].z + ky * original_track[i].y)
            A[row, col_global+4] = ky*original_track[i].x
            A[row, col_global+5] = original_track[i].x
            A[row, col_local+2] = -transformed_track[i].z
            A[row, col_local+3] = -1

        # fill r
        for i in range(0, N_on_T):
            z = transformed_track[i].z
            intersection = projector.solve(cross_point, direction, z)
            r_offset = j*2*N_on_T + 2*i
            #print("r_offset = ", j, i, r_offset)

            # must be measured - projected; need to match the A matrix
            r[r_offset, 0] = transformed_track[i].x - intersection.x
            r[r_offset+1, 0] = transformed_track[i].y - intersection.y

    print(A.size())
    print(r.size())
    #r.zero_()
    #print_tensor(r)
    #input("enter to continue...")

    AT = A.T
    print(AT.size())
    A2 = torch.matmul(AT, A)
    print(A2.size())

    # regularization A2
    A2 = A2 + regularization_lambda * torch.eye(A2.size(0))

    B = torch.matmul(AT, r)
    print(B.size())
    #print_tensor(B)
    #input("enter to continue...")

    # set fix layer
    # 1) set the corresponding B elements to 0
    b_start = 6 * iFixLayerIndex
    for i_fix_layer in range(0, 6):
        B[b_start + i_fix_layer, 0] = 0
    # 2) set the corresponding A2 part to unit matrix
    #    make the correpsonding block to a unitary matrix, this way we can
    #    assure that the dx, dy, dz, dax, day, daz for the layer will have 0 solution in each iteration
    for i_fix in range (0, 6):
        for j_fix in range(0, 6):
            if i_fix == j_fix:
                A2[b_start + i_fix, b_start + j_fix] = 1
            else:
                A2[b_start + i_fix, b_start + j_fix] = 0

    # solve for the improvement
    #s = torch.linalg.solve(A2, B)
    s = solver.svd(A2, B)
    #s = solver.lin(A2, B)
    print("solution: ", s.size())
    #print(s)

    #print_tensor(A2)
    #print_tensor(B)
    #input("enter to continue...")

    # save the improvement for global parameters
    g_s = s[:6*N_on_T]
    print(g_s.size())

    # reshape it
    global step_size
    global_params_delta = (g_s.reshape(N_on_T, 6) * step_size)

    # update with momentum
    if USE_MOMENTUM:
        global_params_delta = eta * global_params_delta_prev + (1.- eta)*global_params_delta
        global_params_delta_prev = global_params_delta

    print("improvements = :")
    print_tensor(global_params_delta)
    print("current results = :")
    #print_tensor(global_params)
    print("actual results = :")
    #print_tensor(alignment_result)

    #global_params = global_params + global_params_delta
    #print_tensor(global_params)
    
    return chi_square
 

# for show purpose
y_data = []
x_data = []

for iiter in range(0, NITER):
    print(".................. iteration {} ....................".format(iiter))
    chisq = one_iteration(iiter*nBatch, nBatch)
    #input("enter to continue...")

    print_tensor(global_params)
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
if USE_MOMENTUM:
    file_name = "chi2_step_size_{}_momentum_eta_{}_regularization_lambda_{}.txt".format(step_size, eta, regularization_lambda)
else:
    file_name = "chi2_step_size_{}_no_momentum_regularization_lambda_{}.txt".format(step_size, eta, regularization_lambda)
with open(file_name, 'w') as file:
    file.write("step_size = {}, momentum_eta = {}, regularization_lambda = {}\n".format(step_size, eta, regularization_lambda))
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




