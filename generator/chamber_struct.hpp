#ifndef CHAMBER_STRUCT_H
#define CHAMBER_STRUCT_H

#include "plane_transform.hpp"

namespace chamber_struct
{
    using plane_transform::vec3_t;
    using plane_transform::plane_t;
    using plane_transform::line_t;

    class chamber_t {
    public:
        chamber_t(): pt_ori(0, 0, 0),
        pt_off(0, 0, 0), pt_rot(0, 0, 0), chamber_norm_dir(0, 0, 1)
        {
        }

        ~chamber_t() {
        }

        void set_origin(const vec3_t &o) {
            pt_ori = o;
        }
        void set_offset(const vec3_t &o) {
            pt_off = o;
        }
        void set_rotation(const vec3_t &r) {
            pt_rot = r;
        }

        vec3_t detect(const vec3_t& source, const double &kx, const double &ky, vec3_t *true_hit=nullptr, TRandom *gen=nullptr)
        {
            // here we do translate first, then rotate
            // the rotate sequence is (see plane_transform.hpp) : R = RzRyRx

            // translate the chamber origin
            vec3_t new_origin = pt_ori + pt_off;

            // before the translation, the plane equation: z - pt_ori.z = 0;
            // after translation, the new plane equation: z - new_origin.z = 0;
            plane_t trans_plane(0, 0, 1, -new_origin.z);

            // rotate the plane around the new origin
            plane_t rotated_plane = trans_plane.rotate(pt_rot, new_origin);

            // get the intersection point between the track and the new rotated plane
            vec3_t track_dir(kx, ky, 1);
            line_t track(source, track_dir);
            vec3_t intersect = rotated_plane.intersect_point(track);

            if(true_hit != nullptr)
                *true_hit = intersect;

            // get the relative position in the new coord
            double new_x = intersect.x - new_origin.x;
            double new_y = intersect.y - new_origin.y;

            if(gen != nullptr) {
                new_x = gen -> Gaus(new_x, 0.2);
                new_y = gen -> Gaus(new_y, 0.2);
            }

            // we thought we don't have offset, so the z coord we get from the detector 
            // is still the old one
            double new_z = pt_ori.z;

            return vec3_t(new_x, new_y, new_z);
        }

    private:
        // chamber position
        vec3_t pt_ori;
        // chamber offset
        vec3_t pt_off;
        // chamber rotation
        vec3_t pt_rot;


        // each chamber is a 2D plane, and this direction defines the normal direction of the plane
        // the default chamber is a plane perpendicular to the Z axis, and its default normal
        // vector is (0, 0, 1)
        vec3_t chamber_norm_dir;
    };
};

#endif
