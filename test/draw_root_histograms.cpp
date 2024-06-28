#include <TCanvas.h>
#include <TH1F.h>
#include <TStyle.h>
#include <TFile.h>

void draw_root_histograms() {
    TFile *f = new TFile("../fermilab_test/results.root");
    TH1F *hxres[4];
    TH1F *hyres[4];
    for(int i=0; i<4; i++) {
        hxres[i] = (TH1F*)f->Get(Form("hxres%d", i));
        hyres[i] = (TH1F*)f->Get(Form("hyres%d", i));

        hxres[i] -> GetXaxis() -> SetLabelSize(0.05);
        hxres[i] -> GetYaxis() -> SetLabelSize(0.05);
        hyres[i] -> GetXaxis() -> SetLabelSize(0.05);
        hyres[i] -> GetYaxis() -> SetLabelSize(0.05);

        hxres[i] -> SetLineWidth(2);
        hyres[i] -> SetLineWidth(2);

        hxres[i] -> GetXaxis() -> SetRangeUser(-0.4, 1.0);
        hyres[i] -> GetXaxis() -> SetRangeUser(-0.4, 1.0);
 
    }

    // Create a canvas and divide it into a 2x2 grid
    TCanvas *c1 = new TCanvas("c1", "Canvas", 1300, 850);
    c1->Divide(4, 2, 0, 0); // No margin between pads

    double margin = 0.06;
    double xwidth = (1 - 2*0.05) / 4;
    double ywidth = (1 - 2*0.05) / 2;
    double x1 = 0, y1 = 0, x2 = 0, y2 = 0;

    gStyle -> SetOptFit(1111);

    //
    TLatex resoLatex;
    resoLatex.SetTextColor(2);
    resoLatex.SetTextSize(0.1);
    string resoX[4] = {"#sigma = 71 um", "#sigma = 66 um", "#sigma = 66 um", "#sigma = 72 um"};
    string resoY[4] = {"#sigma = 66 um", "#sigma = 64 um", "#sigma = 63 um", "#sigma = 68 um"};

    // Draw the xresolution histograms in the respective pads
    c1->cd(1);
    x1 = margin, y1 = 0.5;
    x2 = x1 + xwidth, y2 = y1 + ywidth;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hxres[0]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoX[0].c_str());

    c1->cd(2);
    x1 = margin + xwidth, y1 = 0.5;
    x2 = x1 + xwidth, y2 = y1 + ywidth;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hxres[1]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoX[1].c_str());


    c1->cd(3);
    x1 = margin + 2 * xwidth, y1 = 0.5;
    x2 = x1 + xwidth, y2 = y1 + ywidth;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hxres[2]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoX[2].c_str());


    c1->cd(4);
    x1 = margin + 3 * xwidth, y1 = 0.5;
    x2 = x1 + xwidth, y2 = y1 + ywidth;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hxres[3]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoX[3].c_str());


    // Draw the yresolution histograms in the respective pads
    c1->cd(5);
    x1 = margin, y1 = margin;
    x2 = x1 + xwidth, y2 = 0.5;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hyres[0]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoY[0].c_str());


    c1->cd(6);
    x1 = margin + xwidth, y1 = margin;
    x2 = x1 + xwidth, y2 = 0.5;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hyres[1]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoY[1].c_str());


    c1->cd(7);
    x1 = margin + 2 * xwidth, y1 = margin;
    x2 = x1 + xwidth, y2 = 0.5;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hyres[2]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoY[2].c_str());


    c1->cd(8);
    x1 = margin + 3 * xwidth, y1 = margin;
    x2 = x1 + xwidth, y2 = 0.5;
    gPad->SetPad(x1, y1, x2, y2);
    gPad -> SetFrameLineWidth(2);
    hyres[3]->Draw();
    resoLatex.DrawLatexNDC(0.5, 0.2, resoY[3].c_str());


    // Add common x and y axis titles
    c1->cd();
    TLatex latex;
    latex.SetTextSize(0.03);
    latex.SetTextAlign(22); // Center alignment
    latex.DrawLatexNDC(0.5, 0.04, "residue (mm)");
    latex.SetTextAngle(90);
    latex.DrawLatexNDC(0.04, 0.5, "");

    // Update the canvas
    c1->Update();

    TPaveStats *stx[4];
    TPaveStats *sty[4];
    for(int i=0; i<4; i++) {
        stx[i] = (TPaveStats*)hxres[i] -> GetListOfFunctions()->FindObject("stats");
        stx[i] -> SetX1NDC(0.4);
        stx[i] -> SetY1NDC(0.4);
        stx[i] -> SetX2NDC(1.0);
        stx[i] -> SetY2NDC(1.0);

        sty[i] = (TPaveStats*)hyres[i] -> GetListOfFunctions()->FindObject("stats");
        sty[i] -> SetX1NDC(0.4);
        sty[i] -> SetY1NDC(0.4);
        sty[i] -> SetX2NDC(1.0);
        sty[i] -> SetY2NDC(1.0);
    }

    c1 -> Modified();
    c1 -> Update();

}


