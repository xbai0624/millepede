{
    TFile *f = new TFile("../fermilab_test/results.root");

    TH1F *h = (TH1F*)f->Get("hchi2_reduced");

    TCanvas *c = new TCanvas("c", "c", 800, 600);
    gPad -> SetFrameLineWidth(2);
    //gPad -> SetGridx();
    h -> SetLineWidth(2);
    h -> GetXaxis() -> SetRangeUser(0, 9);
    h -> GetXaxis() -> SetTitle("#chi^{2} / DOF");
    h -> GetXaxis() -> CenterTitle();
    h -> SetTitle("#chi^{2} / DOF");
    h -> Draw();
}
