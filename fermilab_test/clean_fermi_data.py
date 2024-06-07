import load_raw_fermi_data

total_tracks = load_raw_fermi_data.load_fermi_data()

for track in total_tracks:
    for hit in track:
        print("{:8.4f} {:8.4f} {:8.2f}".format(hit.x, hit.y, hit.z), end="    ")
    print("\n", end="")

# remove all tracks with larger chi2

import ROOT
from ROOT import TH1F, TCanvas, TFile

from text_parser import vec3_t
from track_fitter import fitter, projector
fit = fitter()
project = projector()

# degree of freedom
dof = 4

hchi2 = TH1F("hchi2_reduced", "h_chi2/dof", 400, 0, 50)
hxres = [
        TH1F("hxres0", "h_xres_gem0", 1000, -1, 1),
        TH1F("hxres1", "h_xres_gem1", 1000, -1, 1),
        TH1F("hxres2", "h_xres_gem2", 1000, -1, 1),
        TH1F("hxres3", "h_xres_gem3", 1000, -1, 1),
        ]
hyres = [
        TH1F("hyres0", "h_yres_gem0", 1000, -1, 1),
        TH1F("hyres1", "h_yres_gem1", 1000, -1, 1),
        TH1F("hyres2", "h_yres_gem2", 1000, -1, 1),
        TH1F("hyres3", "h_yres_gem3", 1000, -1, 1)
        ]

# inclusive resolution
resolution = [0.03272, 0.03016, 0.03596, 0.0345, 0.03578, 0.03426, 0.03278, 0.03092]
# exclusive resolution
#resolution = [0.07172, 0.06644, 0.06608, 0.06362, 0.06587, 0.06314, 0.07171, 0.06787]

for track in total_tracks:
    direction, cross_point, chi2 = fit.solve(track, resolution)
    #print(chi2)
    hchi2.Fill(chi2/dof)

    # get resolution
    for i in range(len(track)):
        # get the exclusive resolution
        cp_track =list(track)
        cp_track.remove(track[i])
        v, xpoint, c2 = fit.solve(cp_track)
        zi = track[i].z
        pt = project.solve(xpoint, v, zi)
        dx = pt.x - track[i].x
        dy = pt.y - track[i].y

        hxres[i].Fill(dx)
        hyres[i].Fill(dy)


canvas = TCanvas("c", "c", 800, 600);
hchi2.Draw()

canvas.SetLogy()
canvas.Update();
canvas.Draw()

input("enter to continue to cut.")

chi2_cut = 0.08

with open("fermi_tracks.txt", "w") as f:
    for track in total_tracks:
        _, _, chi2 = fit.solve(track)
        if chi2 > chi2_cut:
            continue

        for hit in track:
            f.write("{:8.4f} {:8.4f} {:8.2f}".format(hit.x, hit.y, hit.z))
        f.write("\n")
f.close();

froot = TFile("results.root", "recreate");
hchi2.Write();
for i in range(4):
    ROOT.gStyle.SetOptFit(1111)
    hxres[i].Fit("gaus", "", "",  -0.2, 0.2)
    hxres[i].Write()
for i in range(4):
    ROOT.gStyle.SetOptFit(1111)
    hyres[i].Fit("gaus", "", "", -0.2, 0.2)
    hyres[i].Write()

froot.Close()
