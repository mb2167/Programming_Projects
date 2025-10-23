#include "Grid.hpp"

Grid::Grid(int Nx_, int Ny_, double Lx_, double Ly_)
    : Nx(Nx_), Ny(Ny_), Lx(Lx_), Ly(Ly_) {
    dx = Lx / Nx;
    dy = Ly / Ny;
    x.resize(Nx);
    y.resize(Ny);

    for (int i = 0; i < Nx; ++i) x[i] = -Lx / 2.0 + i * dx;
    for (int j = 0; j < Ny; ++j) y[j] = -Ly / 2.0 + j * dy;
}
