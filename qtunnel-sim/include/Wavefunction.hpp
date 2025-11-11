#pragma once
#include <vector>
#include <complex>
#include "Grid.hpp"

class Wavefunction {
public:
    int Nx, Ny;
    std::vector<std::complex<double>> psi;

    Wavefunction(int Nx_, int Ny_);

    void initializeGaussian(const Grid& grid,
                            double x0, double y0,
                            double sigmaX, double sigmaY,
                            double kx0, double ky0);
};
