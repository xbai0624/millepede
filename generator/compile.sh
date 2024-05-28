g++ -std=c++17 -g -O2 -I./ -I${ROOTSYS}/include $(root-config --glibs) -o gen main.cpp
