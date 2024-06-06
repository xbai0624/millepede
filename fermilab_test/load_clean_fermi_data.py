import load_raw_fermi_data

total_tracks = load_raw_fermi_data.load_fermi_data()

# remove all tracks with larger chi2

from track_fitter import fitter
fitter = fitter()

# degree of freedom
dof = 4

chi2_cut = 0.08


# clean up data
def load_fermi_data():
    res = []
    for track in total_tracks:
        _, _, chi2 = fitter.solve(track)
        if chi2 > chi2_cut:
            continue

        res.append(track)
    print("total tracks: ", len(res))
    return res

#load_fermi_data()
