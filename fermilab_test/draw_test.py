
import load_fermi_data
import ROOT

h = []
for i in range(4):
    h.append(ROOT.TH2F(ROOT.Form(f"h{i}"), ROOT.Form(f"h{i}"), 200, -100, 100, 200, -100, 100))

all_tracks = load_fermi_data.load_fermi_data()

for track in all_tracks:
    for i in range(4):
        print(track[i])
        h[i].Fill(track[i].x, track[i].y)

f = ROOT.TFile("hists.root", "recreate")
for ih in h:
    ih.Write()
f.Close()
