#pragma once
#include <vector>

class Grid {
public:
    int Nx, Ny;
    double Lx, Ly, dx, dy;
    std::vector<double> x, y;

    Grid(int Nx_, int Ny_, double Lx_, double Ly_);
};
