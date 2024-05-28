#ifndef PLANE_TRANSFORM_HPP
#define PLANE_TRANSFORM_HPP

#include <ostream>
#include <iomanip>
#include <TMath.h>

namespace plane_transform
{
    struct vec3_t {
        double x, y, z;

        vec3_t() {
            x = 0, y = 0, z = 0;
        }

        vec3_t(double a1, double a2, double a3) {
            x = a1, y = a2, z = a3;
        }

        vec3_t(const vec3_t &v) {
            x = v.x, y = v.y, z = v.z;
        }

        double & operator()(int i) {
            if(i==0) return x;
            else if(i==1) return y;
            else return z;
        }

        double operator*(const vec3_t &v) const {
            return x*v.x + y*v.y + z*v.z;
        }

        vec3_t operator*(double p) const {
            double t1 = x*p, t2 = y*p, t3 = z*p;
            vec3_t v(t1, t2, t3);
            return v;
        }

        vec3_t operator+(const vec3_t &v) const {
            double t1 = x + v.x, t2 = y + v.y, t3 = z + v.z;
            vec3_t res(t1, t2, t3);
            return res;
        }

        double length() const {
            double r2 = x*x + y*y + z*z;
            r2 = TMath::Sqrt(r2);
            return r2;
        }

        vec3_t unit() const {
            double r = length();
            double t1 = x/r, t2 = y/r, t3 = z/r;
            vec3_t res(t1, t2, t3);
            return res;
        }
    };

    std::ostream& operator<<(std::ostream& os, const vec3_t &v)
    {
        os<<std::setfill(' ')<<std::setw(8)<<std::fixed<<std::setprecision(2)<<v.x<<std::endl;
        os<<std::setfill(' ')<<std::setw(8)<<std::fixed<<std::setprecision(2)<<v.y<<std::endl;
        os<<std::setfill(' ')<<std::setw(8)<<std::fixed<<std::setprecision(2)<<v.z<<std::endl;
        os<<std::endl;

        return os;
    }

    struct mat3_t {
        double arr[3][3];

        mat3_t()
        {
            for(int i=0; i<3; i++)
                for(int j=0; j<3; j++)
                    arr[i][j] = 0;
        }

        double& operator()(int i, int j) {
            return ((*this).arr)[i][j];
        }

        mat3_t operator*(mat3_t& m) {
            mat3_t res;
            for(int i=0; i<3; i++)
            {
                for(int j=0; j<3; j++) {
                    for(int k=0; k<3; k++) res(i, j) += (*this)(i, k) * m(k, j);
                }
            }
            return res;
        }

        vec3_t operator*(vec3_t & v) {
            vec3_t res;
            for(int i=0; i<3; i++)
            {
                for(int k=0; k<3; k++)
                    res(i) += (*this)(i, k) * v(k);
            }
            return res;
        }
    };

    std::ostream& operator<<(std::ostream& os, const mat3_t &m)
    {
        for(int i=0; i<3; i++) {
            for(int j=0; j<3; j++) {
                os<<std::setfill(' ')<<std::setw(8)<<std::fixed<<std::setprecision(2)<<m.arr[i][j];
            }
            os<<std::endl;
        }
        return os;
    }

    struct line_t {
        vec3_t anchor_point;
        vec3_t dir;

        line_t(const vec3_t &p, const vec3_t &d)
            : anchor_point(p), dir(d.unit())
        {}
    };

    std::ostream& operator<<(std::ostream& os, const line_t &l)
    {
        os<<"anchor point: "<<l.anchor_point<<std::endl
            <<"direction: "<<l.dir<<std::endl;
        return os;
    }

    struct plane_t {
        // here we define a plane:
        // A*x + B*y +C*z + D = 0
        double A, B, C, D;

        plane_t(): A(0), B(0), C(0), D(0)
        {}

        plane_t(double a1, double a2, double a3, double a4)
            : A(a1), B(a2), C(a3), D(a4)
        {}

        // rotate this plane using Euler angles, here we choose
        // XYZ convention, R = R''(Z)*R'(Y)*R(X)
        // rotation angles ax, ay, az must be in radiant
        // and
        // rotate plane around a fixed on-plane point (x0, y0, z0)
        plane_t rotate(double ax, double ay, double az, vec3_t p0) const
        {
            mat3_t Rx, Ry, Rz;
            Rx(0, 0) = 1;
            Rx(1, 1) = TMath::Cos(ax), Rx(1, 2) = -TMath::Sin(ax);
            Rx(2, 1) = TMath::Sin(ax), Rx(2, 2) = TMath::Cos(ax);

            Ry(0, 0) = TMath::Cos(ay), Ry(0, 2) = TMath::Sin(ay);
            Ry(1, 1) = 1;
            Ry(2, 0) = -TMath::Sin(ay), Ry(2, 2) = TMath::Cos(ay);

            Rz(0, 0) = TMath::Cos(az), Rz(0, 1) = -TMath::Sin(az);
            Rz(1, 0) = TMath::Sin(az), Rz(1, 1) = TMath::Cos(az);
            Rz(2, 2) = 1;

            vec3_t normal_vector(A, B, C);
            vec3_t new_normal_vector = Rx*normal_vector;
            new_normal_vector = Ry*new_normal_vector;
            new_normal_vector = Rz*new_normal_vector;

            plane_t t;
            t.A = new_normal_vector(0);
            t.B = new_normal_vector(1);
            t.C = new_normal_vector(2);
            t.D = -(new_normal_vector * p0);

            return t;
        }

        plane_t rotate(const vec3_t &v, vec3_t p0) const {
            return rotate(v.x, v.y, v.z, p0);
        }

        vec3_t intersect_point(const line_t &l)
        {
            vec3_t plane_norm(A, B, C);
            vec3_t line_dir(l.dir);

            double denom = plane_norm * line_dir;
            double numerator = plane_norm * l.anchor_point + D;
            double d = - numerator/denom;

            vec3_t res = line_dir * d;
            res = res + l.anchor_point;
            return res;
        }
    };

    std::ostream& operator<<(std::ostream &os, const plane_t &p)
    {
        os<<p.A<<"*x + "<<p.B<<"*y + "<<p.C<<"*z + "<<p.D<<" = 0"
            <<std::endl;
        return os;
    }
};

#endif
