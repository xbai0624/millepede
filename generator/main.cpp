/* 
 * all units in centimeter
 *
 */

#include <iostream>
#include <iomanip>
#include <fstream>

#include <TRandom.h>
#include <TMath.h>
#include <TH2F.h>
#include <TFile.h>

#include "plane_transform.hpp"
#include "chamber_struct.hpp"

const double mm = 0.1;
const double deg = 3.1415926/180.;
const int NTracks = 1000000;

void unit_tests();

int main(int argc, char* argv[])
{
    // set up the tracker system
    static const int NTrackers = 6;

    // units in centimeter
    const double ZTrackers[NTrackers] = {10, 30, 50, 70, 90, 110};

    /*
    // pre-set offset and rotation
    // units in mm
    const double mm = 0.1;
    const double dx[NTrackers] = {0.8, 1.2, -0.6, -3, 2, -1};
    const double dy[NTrackers] = {1.2, -3, 2, 5, -4, 6};
    const double dz[NTrackers] = {5, 10, 7, -7, -9, 4};

    // units in degree
    const double deg = 3.1415926/180.;
    const double ax[NTrackers] = {0.2, 0.3, -1, 1.2, -0.5, 0.7};
    const double ay[NTrackers] = {1.5, 0.5, 1.2, -0.9, 0.7, 1.2};
    const double az[NTrackers] = {-0.8, 0.4, -0.76, 0.1, 1.3, -1.4};
    */

    /*
    // pre-set offset and rotation
    // units in mm
    const double mm = 0.1;
    const double dx[NTrackers] = {0, 1.2, -0.6, -3, 2, -1};
    const double dy[NTrackers] = {0, -3, 2, 5, -4, 6};
    const double dz[NTrackers] = {0, 10, 7, -7, -9, 4};

    // units in degree
    const double deg = 3.1415926/180.;
    const double ax[NTrackers] = {0, 0.3, -1, 1.2, -0.5, 0.7};
    const double ay[NTrackers] = {0, 0.5, 1.2, -0.9, 0.7, 1.2};
    const double az[NTrackers] = {0, 0.4, -0.76, 0.1, 1.3, -1.4};
    */

    // pre-set offset and rotation
    // units in mm
    const double mm = 0.1;
    const double dx[NTrackers] = {0, 1.2, -0.6, -3, 2, -1};
    const double dy[NTrackers] = {0, -3, 2, 5, -4, 6};
    const double dz[NTrackers] = {0, 10, 7, -7, -9, 4};

    // units in degree
    const double deg = 3.1415926/180.;
    const double ax[NTrackers] = {0, 0, 0, 0, 0, 0};
    const double ay[NTrackers] = {0, 0, 0, 0, 0, 0};
    const double az[NTrackers] = {0, 0, 0, 0, 0, 0};

    /*
    // pre-set offset and rotation
    // units in mm
    const double dx[NTrackers] = {0, 0, 0, 0, 0, 0};
    const double dy[NTrackers] = {0, 0, 0, 0, 0, 0};
    const double dz[NTrackers] = {0, 0, 0, 0, 0, 0};

    // units in degree
    const double ax[NTrackers] = {0, 0, 0, 0, 0, 0};
    const double ay[NTrackers] = {0, 0, 0, 0, 0, 0};
    const double az[NTrackers] = {0, 0, 0, 0, 0, 0};
    */

    chamber_struct::chamber_t gem[NTrackers];
    for(int i=0; i<NTrackers; i++)
    {
        plane_transform::vec3_t ori(0, 0, ZTrackers[i]);
        gem[i].set_origin(ori);

        plane_transform::vec3_t off(dx[i]*mm, dy[i]*mm, dz[i]*mm);
        gem[i].set_offset(off);

        plane_transform::vec3_t rot(ax[i]*deg, ay[i]*deg, az[i]*deg);
        gem[i].set_rotation(rot);
    }

    // 2d raw hit distribution
    TH2F *h_gem[NTrackers];
    for(int i=0; i<NTrackers; i++) {
        h_gem[i] = new TH2F(Form("gem_%d", i), Form("gem_%d", i), 500, -20, 20, 500, -20, 20);
    }

    // save all tracks to a txt file
    std::fstream file("tracks.txt", std::fstream::out);
    // save true tracks to a text file (those tracks are detected if the chambers were not transformed)
    std::fstream true_file("true_tracks.txt", std::fstream::out);

    // generate tracks
    const double max_angle = 5.0 * deg;
    double k = TMath::Tan(max_angle);
    double target_a = 1.2; // all tracks originates from a 1.2cmx1.2cm target area, target is located at 0
    TRandom *gen = new TRandom(0);

    for(int i=0; i<NTracks; i++)
    {
        double ax = gen->Uniform(-k, k);
        double ay = gen->Uniform(-k, k);

        //if(ax < 5*deg && ax > -5*deg) continue;
        //if(ay < 5*deg && ay > -5*deg) continue;

        double kx = TMath::Tan(ax);
        double ky = TMath::Tan(ay);

        double x = gen -> Uniform(-target_a, target_a);
        double y = gen -> Uniform(-target_a, target_a);

        plane_transform::vec3_t src(x, y, 0);
        plane_transform::vec3_t trk_pts[NTrackers];
        plane_transform::vec3_t true_trk_pts[NTrackers];

        plane_transform::vec3_t true_track;

        for(int t = 0; t<NTrackers; t++) {
            trk_pts[t] = gem[t].detect(src, kx, ky, &true_track, gen);
            true_trk_pts[t] = true_track;

            h_gem[t] -> Fill(trk_pts[t].x, trk_pts[t].y);
        }

        for(int t=0; t<NTrackers; t++){
            file<<std::setfill(' ')<<std::setw(12)<<std::fixed<<std::setprecision(6)<<trk_pts[t].x;
            file<<std::setfill(' ')<<std::setw(12)<<std::fixed<<std::setprecision(6)<<trk_pts[t].y;
            file<<std::setfill(' ')<<std::setw(12)<<std::fixed<<std::setprecision(6)<<trk_pts[t].z;

            true_file<<std::setfill(' ')<<std::setw(12)<<std::fixed<<std::setprecision(6)<<true_trk_pts[t].x;
            true_file<<std::setfill(' ')<<std::setw(12)<<std::fixed<<std::setprecision(6)<<true_trk_pts[t].y;
            true_file<<std::setfill(' ')<<std::setw(12)<<std::fixed<<std::setprecision(6)<<true_trk_pts[t].z;
        }
        file<<std::endl;
        true_file<<std::endl;
    }

    file.close();

    TFile *f_result = new TFile("hits_2d.root", "recreate");
    for(int i=0; i<NTrackers; i++)
        h_gem[i] -> Write();
    f_result -> Close();

    //unit_tests();
}



void unit_tests()
{
    std::cout<<"------------- unit teset ----------------"<<std::endl;
    plane_transform::mat3_t t;
    t(0, 0) = 4, t(0, 1) = 2, t(0, 2) = 3;
    t(1, 0) = 1, t(1, 1) = 5, t(1, 2) = 8;
    t(2, 0) = 7, t(2, 1) = 4, t(2, 2) = 6;
    std::cout<<t<<std::endl;
    plane_transform::vec3_t v;
    v(0) = 4, v(1) = 2, v(2) = 3;
    std::cout<<v<<std::endl;

    plane_transform::vec3_t res = t * v;
    std::cout<<res<<std::endl;

    plane_transform::mat3_t mr = t * t;
    std::cout<<mr<<std::endl;
    std::cout<<t<<std::endl;
    std::cout<<"------------- unit teset ----------------"<<std::endl;

    plane_transform::plane_t p1;
    p1.C = 1; p1.D = -4;
    std::cout<<p1<<std::endl;

    plane_transform::vec3_t coord(0, 0, 4);
    double a = 3.1415926 / 2.;
    plane_transform::plane_t p2 = p1.rotate(0, a, 0, coord);
    std::cout<<p2<<std::endl;

    std::cout<<"------------- unit teset ----------------"<<std::endl;
    plane_transform::plane_t pln2(1, 1, 1, 4);
    plane_transform::vec3_t anchor_point(0, 0, 0), dir(1, 1, 1);
    plane_transform::line_t l1(anchor_point, dir);
    plane_transform::vec3_t intersect = pln2.intersect_point(l1);
    std::cout<<intersect<<std::endl;
}
